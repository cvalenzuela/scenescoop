# -*- coding: utf-8 -*-
# ----
# Run the img2text model
# ----

import json
from subprocess import call
from os import path, path, makedirs
from time import time
import shutil

def im2text(temp_dir, transcript_dir, name, imgs_batches, amount):
  """
  Run img2txt over a sequence of images
  """
  print('Running the model on {} images'.format(amount))

  original_results = path.join(temp_dir, str(time()) + '.txt')
  #original_results = path.join(temp_dir,'demo.txt') # debug

  # run the model and save to temp file. runs in batchs of 100 images
  for batch in imgs_batches:
    if path.exists(original_results):
      temp_file = open(original_results, "a+")
    else:
      temp_file = open(original_results, "w+")
    call(["models/im2txt/bazel-bin/im2txt/run_inference", "--checkpoint_path", "models/im2txt/checkpoints/model.ckpt-3000000", "--vocab_file", "models/im2txt/checkpoints/word_counts.txt", "--input_files", batch], stdout=temp_file)
    temp_file.close()

  # filter the results and leave just frame number and description
  temp_file = open(original_results, "r+")
  temp_content = temp_file.read()
  temp_content = temp_content.split('\n')

  description_sequence = [4*i + 1 for i in range(amount)]
  captions = []
  frames = []
  for i in range(len(temp_content)):
    if (i == 0 or i%4 == 0):
      f = temp_content[i].split(" ")[-1].split('.')[0]
      if (len(f) > 0):
        frames.append(f)
    elif (i in description_sequence):
      c = " ".join(((temp_content[i].split(' '))[3:-1])).split('.')[0]
      if(len(c) > 1):
        captions.append(c)

  # make an object with caption : [frames]
  content = {}
  for i in range(len(frames)):
    if (captions[i] in content):
      content[captions[i]].append(int(frames[i]))
    else:
      content[captions[i]] = [int(frames[i])]

  # order the frames for every captions
  for c in content:
    content[c] = sorted(content[c])

  # make a new file with timeline of images
  transcript = path.join(transcript_dir, name + ".json")
  with open(transcript, 'w+') as outfile:
    json.dump(content, outfile)
    
  temp_file.close()

  # Remove the temp folder
  shutil.rmtree(temp_dir)
  makedirs(temp_dir)

  return content