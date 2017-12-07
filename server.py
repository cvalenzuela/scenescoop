# -*- coding: utf-8 -*-
# ----
# Server
# ----

import os
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from werkzeug import secure_filename
import subprocess
import socket
from glob import glob
from argparse import Namespace
from os import getcwd, path

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
  '''
  Main Route
  '''
  return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload():
  '''
  Upload a video
  '''
  file = request.files['file']
  # Check if the file is one of the allowed types/extensions
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['INPUT_VIDEOS_PATH'], request.form["name"])
    file.save(file_path)
    return analyze_video(file_path, filename)
  else:
    return jsonify(status="400", content='Not a valid file')

@app.route('/make', methods=['POST'])
def create_output():
  '''
  Create a new video given the input video and a user selected film in the database.
  '''

  input_data = "{}/{}.json".format(TRANSCRIPTS_VIDEOS_PATH, request.form["name"])
  duration = "0,{}".format(int(float(request.form["duration"])))
  movie = glob(VIDEOS_PATH + '/{}.*'.format(request.form["movie"]))[0]
  movie_data = glob(TRANSCRIPTS_VIDEOS_PATH + '/{}.*'.format(request.form["movie"]))[0]

  movie = make_movie(OUTPUT_VIDEOS_PATH, input_data, duration, movie, movie_data, True)
  return jsonify(status="200", movie=movie)

def analyze_video(file, name):
  '''
  Call Scenescoop with the uploaded video
  '''
  args = Namespace(video=file, name=name, input_data=None, api=True)
  scene_content = scenescoop(args)
  content = ''
  maxframes = 0
  for description in scene_content:
    if(len(scene_content[description]) > maxframes):
      content = description
      maxframes = len(scene_content[description]) 

  return jsonify(status="200", scene_content=scene_content, content=content, maxframes=maxframes)

def allowed_file(filename):
  '''
  For a given file, return whether it's an allowed type or not
  '''
  return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

if __name__ == "__main__":
    app.run(host=ip, port=8080, debug=True, threaded=True)