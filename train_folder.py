# This is a script to train a bunch of videos and leave it running for ever

import os
from glob import glob
import argparse
from argparse import Namespace
from os import getcwd, path

from scenescoop import main as scenescoop

def start(options):
  # get all the videos in the input folder
  videos = glob(options.input+'/*.*')

  # run scenescoop on every video
  for video in videos:
    name = video.split('/')[-1]
    args = Namespace(video=video, name=name, input_data=None, api=True)
    scenescoop(args)
    # once ready, move to the ready folder
    os.rename(video, options.move + '/' + name)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Train a bunch of videos and leave it running for ever')
  parser.add_argument('--input', type=str, help='Source folder containg the videos')
  parser.add_argument('--move', type=str, help='Ready Folder. Where the input videos will move once they are done.')
  args = parser.parse_args()
  start(args) 
