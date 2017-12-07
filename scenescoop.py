# -*- coding: utf-8 -*-
# ----
# Scenescoop
# ----

import argparse
from os import getcwd, path
from glob import glob
from time import time

from get_frames import extract_frames
from run_model import im2text
from make_movie import make_movie

CWD = getcwd()
TEMP_DIR = path.join(CWD, 'temp')
OUTPUT_DIR = path.join(CWD, 'outputs')
TRANSCRIPT_DIR = path.join(CWD, 'transcripts')
FPS = 1

def main(options):
  '''
  Video to img2text
  '''
  if(options.video is not None):
    # 1) Extract frames
    extract_frames(options.video, TEMP_DIR, FPS)

    # 2) Run model with images. Send batches of 100.
    imgs = glob(TEMP_DIR + '/*.jpg')
    amount = len(imgs)
    batches = [[]]
    for i in range(len(imgs)):
      if (i is not 0 and i%100 == 0):
        batches.append([imgs[i]])
      else:
        batches[-1].append(imgs[i])

    imgs_batches = []
    for batch in batches:
      imgs_batches.append(','.join(batch))
  
    # 3) Run model
    model = im2text(TEMP_DIR, TRANSCRIPT_DIR, options.name, imgs_batches, amount)
    if (options.api):
      return model

  if(options.input_data is not None):
    # 4) Make a movie
    make_movie(OUTPUT_DIR, options.input_data, options.input_seconds, options.transform_src, options.transform_data, False)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Storiescoop')
  parser.add_argument('--video', type=str, help='Video Source to transform')
  parser.add_argument('--name', type=str, help='Name of the video', default=str(time()))
  parser.add_argument('--input_data', type=str, help='Input Video. Must be a json file.')
  parser.add_argument('--input_seconds', type=str, help='Input Video Seconds to create transformation. Example: 1,30')
  parser.add_argument('--transform_src', type=str, help='Transform Video Source.')
  parser.add_argument('--transform_data', type=str, help='Transform Video Data. Must be a json file.')
  parser.add_argument('--api', type=str, help='API Request', default=False)
  args = parser.parse_args()
  main(args) 