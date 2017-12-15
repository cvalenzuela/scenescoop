# -*- coding: utf-8 -*-
# ----
# Server
# ----

import os
import mimetypes
from flask import Flask, request, send_from_directory, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from flask_cors import CORS
from werkzeug import secure_filename
import subprocess
import socket
from glob import glob
from argparse import Namespace
from os import getcwd, path
from urllib.request import urlretrieve

from scenescoop import main as scenescoop
from make_movie import make_movie

CWD = getcwd()

VIDEOS_PATH = path.join(CWD, 'videos') # movies to generate content from
INPUT_VIDEOS_PATH = path.join(CWD, 'static', 'videos', 'inputs')
OUTPUT_VIDEOS_PATH = path.join(CWD, 'static', 'videos', 'outputs')
TRANSCRIPTS_VIDEOS_PATH = path.join(CWD, 'transcripts')

# Initialize the Flask application
app = Flask(__name__, static_url_path="")
CORS(app)
ip = socket.gethostbyname('localhost') # socket.gethostname()

# path to the upload directory
app.config['INPUT_VIDEOS_PATH'] = 'static/videos/inputs/'
app.config['OUTPUT_VIDEOS_PATH'] = 'static/videos/outputs/'
app.config['ALLOWED_EXTENSIONS'] = set(['MOV', 'mov', 'avi', 'mp4', 'mkv'])

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
    return analyze_video(file_path, filename)
  else:
    return jsonify(status="400", content='Not a valid file')

@app.route('/make', methods=['POST'])
def create_output():
  """
  Create a new video given the input video and a user selected film in the database.
  """

  input_data = "{}/{}.json".format(TRANSCRIPTS_VIDEOS_PATH, request.form["name"])
  duration = "0,{}".format(int(float(request.form["duration"])))
  movie = glob(VIDEOS_PATH + '/{}.*'.format(request.form["movie"]))[0]
  movie_data = glob(TRANSCRIPTS_VIDEOS_PATH + '/{}.*'.format(request.form["movie"]))[0]

  movie = make_movie(OUTPUT_VIDEOS_PATH, input_data, duration, movie, movie_data, True)
  return jsonify(status="200", movie=movie)

def analyze_video(file, name):
  """
  Call Scenescoop with the uploaded video
  """
  args = Namespace(video=file, name=name, input_data=None, api=True)
  scene_content = scenescoop(args)
  content = ''
  maxframes = 0
  for description in scene_content:
    if(len(scene_content[description]) > maxframes):
      content = description
      maxframes = len(scene_content[description]) 

  return jsonify(status="200", scene_content=scene_content, content=content, maxframes=maxframes)

@app.route("/mms", methods=['GET', 'POST'])
def mms_reply():
    """
    Respond to incoming mms.
    """
    client_number = request.form["From"]
    video_from_client = request.form["MediaUrl0"]
    media_content_type = request.form["MediaContentType0"]
    urlretrieve(video_from_client, "file_name")

    # for (media_url, mime_type) in media_files:
    #     file_extension = mimetypes.guess_extension(mime_type)
    #     media_sid = os.path.basename(urlparse(media_url).path)
    #     content = requests.get(media_url).text
    #     filename = '{sid}{ext}'.format(sid=media_sid, ext=file_extension)

    #     mms_media = MMSMedia(
    #         filename=filename,
    #         mime_type=mime_type,
    #         media_sid=media_sid,
    #         message_sid=message_sid,
    #         media_url=media_url,
    #         content=content)
    #     mms_media.save()
    # message_sid = request.POST.get('MessageSid', '')
    # from_number = request.POST.get('From', '')
    # num_media = int(request.POST.get('NumMedia', 0))

    # media_files = [(request.POST.get("MediaUrl{}".format(i), ''),
    #                 request.POST.get("MediaContentType{}".format(i), ''))
    #                for i in range(0, num_media)]

    # print("message_sid", message_sid)
    # print("from_number", from_number)
    # print("num_media", num_media)
    # print("media_files", media_files)
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

def allowed_file(filename):
  """
  For a given file, return whether it's an allowed type or not
  """
  return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

if __name__ == "__main__":
    app.run(host=ip, port=7676, debug=True, threaded=True)