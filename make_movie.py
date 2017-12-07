# -*- coding: utf-8 -*-
# ----
# Make a video with given frames
# Uses spacy and annoy to get closet semantic similarity between two videos
# Reference: https://github.com/aparrish/plot-to-poem/blob/master/plot-to-poem.ipynb
# ----

import json
import moviepy.editor as mp
from time import time

import random
import sys
import textwrap
import spacy
from annoy import AnnoyIndex
import numpy as np

nlp = spacy.load('en')

def make_movie(output_dir, input_data, seconds, transform_video, transform_data, api):
  '''
  Make a movie with the given parameters
  '''
  t = AnnoyIndex(300, metric='angular')

  with open(input_data) as infile:
    input_data = json.load(infile)

  with open(transform_data) as infile:
    transform_data = json.load(infile)
  
  # get best description for the given input seconds
  seconds = seconds.split(',')
  START = int(seconds[0])
  END = int(seconds[1])
  DURATION = END - START
  seconds_range = [i for i in range(START, END)]

  # get the original descriptions for the input video in the given seconds
  best_match = {}
  for description in input_data:
    for frame in input_data[description]:
      if (frame in seconds_range):
        if (description in best_match):
          best_match[description] = best_match[description] + 1
        else:
          best_match[description] = 1
  
  best_description_for_scene = ''
  times = 0
  for n in best_match:
    if (best_match[n] > times):
      times = best_match[n]
      best_description_for_scene = n
  
  # using the best description get the closet semantic meaning in the transform data
  closest_meaning = nearest_neighbor(transform_data, best_description_for_scene, t)
  print('Original scene is {}. Closest meaning found: {}'.format(best_description_for_scene, closest_meaning))
  # get a largest sequence of frames from that description
  closet_meaning_frames = transform_data[closest_meaning]

  # from that description, group frames in scenes
  scenes = []
  for i in range(len(closet_meaning_frames)):
    if (i == 0):
      scenes.append([closet_meaning_frames[i]])
    else:
      if(closet_meaning_frames[i] - scenes[-1][-1]  < 2):
        scenes[-1].append(closet_meaning_frames[i])
      else:
        scenes.append([closet_meaning_frames[i]])

  # get the largest continuous scene
  largest_continuous_scene = []
  for scene in scenes:
    if (len(scene) > len(largest_continuous_scene)):
      largest_continuous_scene = scene

  start_frame = largest_continuous_scene[0]
  end_frame = largest_continuous_scene[-1]
  frames_duration = end_frame - start_frame
  if (frames_duration == 0):
    start_frame = start_frame - 1
    end_frame = end_frame + 1

  # create the video
  clip = mp.VideoFileClip(transform_video).subclip(start_frame,end_frame)
  composition = mp.concatenate([clip])
  video_name = "/{}.mp4".format(str(time()))
  composition.write_videofile(output_dir + video_name)
  if (api == True):
    return {"name": video_name, "scene_closest_meaning": closest_meaning}

def meanvector(text):
  '''
  Average of the word vectors in a sentence
  '''
  s = nlp(text)
  vecs = [word.vector for word in s \
            if word.pos_ in ('NOUN', 'VERB', 'ADJ', 'ADV', 'PROPN', 'ADP') \
            and np.any(word.vector)] # skip all-zero vectors
  if len(vecs) == 0:
    raise IndexError
  else:
    return np.array(vecs).mean(axis=0)


def nearest_neighbor(data, input, t): 
  '''
  Creates an Annoy index for fast nearest-neighbor lookup
  '''
  i = 0
  map_i_to_description = {}
  for item in data:
    try:
      t.add_item(i, meanvector(item))
      map_i_to_description[i] = item
      i += 1
    except IndexError:
      continue
  
  t.build(50)
  nearest = t.get_nns_by_vector(meanvector(input), n=10)[0]
  return map_i_to_description[nearest]
