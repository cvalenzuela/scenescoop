# -*- coding: utf-8 -*-
# ----
# Server
# ----

import os
import requests
from flask import Flask, request, send_from_directory, jsonify, Response
from celery import Celery
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask_cors import CORS
from werkzeug import secure_filename
import subprocess
import socket
from glob import glob
from argparse import Namespace
from os import getcwd, path
from random import choice

from scenescoop import main as scenescoop
from make_scene import make_scene

from credentials import account_sid, auth_token, number, movies
client = Client(account_sid, auth_token)
NGROK_URL = '784cfa3c.ngrok.io'

CWD = getcwd()

#VIDEOS_PATH = path.join(CWD, 'videos') # movies to generate content from
VIDEOS_PATH = '/Volumes/25DEVOE/MOVIES/READY'
INPUT_VIDEOS_PATH = path.join(CWD, 'static', 'videos', 'inputs')
OUTPUT_VIDEOS_PATH = path.join(CWD, 'static', 'videos', 'outputs')
TRANSCRIPTS_VIDEOS_PATH = path.join(CWD, 'transcripts')
PORT = 7676

# Initialize the Flask application
app = Flask(__name__, static_url_path="")
CORS(app)
ip = socket.gethostbyname('localhost') # socket.gethostname()

# path to the upload directory
app.config['INPUT_VIDEOS_PATH'] = 'static/videos/inputs/'
app.config['OUTPUT_VIDEOS_PATH'] = 'static/videos/outputs/'
app.config['ALLOWED_EXTENSIONS'] = set(['MOV', 'mov', 'avi', 'mp4', 'mkv'])
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Celery configuration
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def async_scenescoop(file_path, video_name, client_number, MessageSid, MediaSid):
  """
  Run an async version of scenescoop
  """
  # Start Scenescoop analyze
  print('Analyzing Video')
  content = analyze_video("{}.mp4".format(file_path), video_name, False)

  # Make a new movie
  input_data = "{}/{}.json".format(TRANSCRIPTS_VIDEOS_PATH, video_name)
  duration = "0,5"
  movie = choice(glob(VIDEOS_PATH + '/*'))
  movie_name = movie.split('/')[-1]
  movie_data = "{}/{}.json".format(TRANSCRIPTS_VIDEOS_PATH, movie_name)
  for m in movies:
    if(m["file"] == movie_name):
      movie_name = m["name"]

  print('Making a new scene with', input_data, duration, movie, movie_data)
  scene = make_scene(OUTPUT_VIDEOS_PATH, input_data, duration, movie, movie_data, True)
  
  # Once the scene is created, send it.
  message = client.api.account.messages.create(
    to=client_number,
    from_=number,
    body="{} from {}.".format(scene["scene_closest_meaning"].capitalize().rstrip(), movie_name),
    media_url=["http://{}/videos/outputs/{}".format(NGROK_URL, scene["name"])],
    status_callback="http://{}/deleteMedia".format(NGROK_URL) 
  )

  # Delete the original media from Twilio's server
  delete_media_file(MessageSid, MediaSid)

@app.route("/")
def main():
  """
  Main Route
  """
  return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload():
  """
  Upload a video
  """
  file = request.files['file']
  keys = request.form.to_dict()

  if "name" in keys:
    name = keys["name"]
  else:
    name = file.filename

  # Check if the file is one of the allowed types/extensions
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['INPUT_VIDEOS_PATH'], str(name))
    file.save(file_path)
    return analyze_video(file_path, filename, True)
  else:
    return jsonify(status="400", content='Not a valid file')

@app.route('/make', methods=['POST'])
def create_output():
  """
  Create a new video given the input video and a user selected film in the database.
  """

  input_data = "{}/{}.json".format(TRANSCRIPTS_VIDEOS_PATH, request.form["name"])
  duration = "0,{}".format(int(float(request.form["duration"])))
  movie = "{}/{}".format(VIDEOS_PATH, request.form["movie"]) # videos/movie.mp4
  movie_data = "{}/{}.json".format(TRANSCRIPTS_VIDEOS_PATH, request.form["movie"]) # transcripts/movie.mp4.json

  scene = make_scene(OUTPUT_VIDEOS_PATH, input_data, duration, movie, movie_data, True)
  return jsonify(status="200", scene=scene)

def analyze_video(file, name, api):
  """
  Call Scenescoop analyze with a video
  """
  args = Namespace(video=file, name=name, input_data=None, api=True)
  scene_content = scenescoop(args)
  content = ''
  maxframes = 0
  for description in scene_content:
    if(len(scene_content[description]) > maxframes):
      content = description
      maxframes = len(scene_content[description]) 
  
  if(api):
    return jsonify(status="200", scene_content=scene_content, content=content, maxframes=maxframes)
  else:
    return content  

def allowed_file(filename):
  """
  For a given file, return whether it's an allowed type or not
  """
  return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# =========
# The next part is just needed for the MMS interaction
# =========
@app.route("/mms", methods=['GET', 'POST'])
def mms_reply():
    """
    Respond to incoming mms using Twilio.
    """
    print('New MMS')
    client_number = request.form["From"]
    MessageSid = request.form["MessageSid"]
    video_url = request.form["MediaUrl0"]
    MediaSid = video_url.split('/')[-1]
    media_content_type = request.form["MediaContentType0"]

    file_path = os.path.join(app.config['INPUT_VIDEOS_PATH'], str(MessageSid))
    video_name = str(MessageSid) + '.mp4'

    # Download the video
    video_response = requests.get(video_url, stream=True)
    video_response.raise_for_status() # Throw an error for bad status codes
    with open("{}.mp4".format(file_path), 'wb') as handle:
      for block in video_response.iter_content(1024):
        handle.write(block)

    # Call Scenescoop async 
    async_scenescoop.apply_async(args=[file_path, video_name, client_number, MessageSid, MediaSid])
    
    # Send an empty response message
    resp = MessagingResponse()
    #resp.message("Got it, now wait...")

    return str(resp)

@app.route("/deleteMedia", methods=['POST'])
def delete_media():
  """
  Delete content that the server sent via Twilio
  """
  return Response("{}", status=200, mimetype='application/json')
  message_status = request.form["MessageStatus"]

  if (message_status == 'delivered'):
    MessageSid = request.form["MessageSid"]
    MediaSid = request.form["MediaUrl0"].split('/')[-1]
    delete_media_file(MessageSid, MediaSid)

def delete_media_file(MessageSid, MediaSid):
  """
  Delete a media from Twilio
  """
  delete_content = client.messages(MessageSid).media(MediaSid).delete()
  if (delete_content == True):
    print("Content deleted", MessageSid, MediaSid)
  else:
    print("Content NOT deleted")

if __name__ == "__main__":
    app.run(host=ip, port=PORT, debug=True, threaded=True)