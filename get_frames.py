# -*- coding: utf-8 -*-
# ----
# Extract image frames from a video
# ----

import os
from moviepy.editor import *

def extract_frames(movie, imgdir, fps):
  '''
  Extract image frames from a video
  '''
  
  clip = VideoFileClip(movie)
  duration = int(clip.duration)
  times = []
  for i in range(duration):
    if(i%fps == 0):
      times.append(i)

  print('Getting {} frames'.format(len(times)))
  for t in times:
    imgpath = os.path.join(imgdir, '{}.jpg'.format(t))
    clip.save_frame(imgpath, t)