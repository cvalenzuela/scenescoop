frames = [510, 2678, 2716, 2726, 2828, 2830, 2833, 2841, 2847, 2848, 2852, 2854, 3723, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3731, 3732, 3733, 3734, 3779, 3852, 3857, 3874, 3876, 3877, 3878, 3879, 3934, 3936, 3937, 3938, 3939, 3941, 4021, 4070, 4071, 4110, 4111, 4236, 4237, 4240, 4242, 4248, 4250, 4251, 4415, 4635, 4716, 4824, 4889, 5036, 5085, 5441, 5443, 5444, 5445, 5446]


# group frames in scenes
scenes = []
for i in range(len(frames)):
  if (i == 0):
    scenes.append([frames[i]])
  else:
    if(frames[i] - scenes[-1][-1]  < 2):
      scenes[-1].append(frames[i])
    else:
      scenes.append([frames[i]])

# get the largest continuous scene
largest = []
for scene in scenes:
  if (len(scene) > len(largest)):
    largest = scene

print(largest)