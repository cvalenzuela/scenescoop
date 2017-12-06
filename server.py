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

# Initialize the Flask application
app = Flask(__name__, static_url_path="")
CORS(app)
ip = socket.gethostbyname('localhost') # socket.gethostname()

# path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['MOV', 'mov', 'avi', 'mp4', 'mkv'])

@app.route("/")
def main():
  '''
  Main Route
  '''
  return app.send_static_file('index.html')

@app.route('/video', methods=['POST'])
def upload():
  '''
  Upload Route
  '''
  print(request.form)
  file = request.files['file']
  # Check if the file is one of the allowed types/extensions
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename) # Make the filename safe, remove unsupported chars
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], '{}.mov'.format(request.form["name"])))

  return jsonify(status="got text", text="result", title="title")

def allowed_file(filename):
  '''
  For a given file, return whether it's an allowed type or not
  '''
  return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

if __name__ == "__main__":
    app.run(host=ip, port=8080, debug=True, threaded=True)