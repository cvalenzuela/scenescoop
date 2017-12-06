# Scenescoop

Scenescoop is a tool to get similar semantic scenes from a pair of videos. Basically, you input a video and get a scene that has a similar meaning in another video.

This project is inspired by [Thingscoop](https://github.com/agermanidis/thingscoop) made by [@agermanidis](https://github.com/agermanidis).

![description](img.png)

## How it works

Scenescoop uses the [im2text](https://github.com/tensorflow/models/tree/master/research/im2txt) tensorflow model on a frame by frame basis over the input and transfer video. It then uses [Spacy](https://spacy.io/) to  average the word vectors in a sentence and [Annoy](https://github.com/spotify/annoy) to create an index for fast nearest-neighbor lookup. (based on [@aparrish](https://github.com/aparrish) [Plot to poem](https://github.com/aparrish/plot-to-poem/blob/master/plot-to-poem.ipynb))

## Demos
 
TODO

## Live Web App

Soon

## Mobile App

Soon

## Usage

Get frames and run model over video
```
python main.py --video videos/moonrisekingdom.mp4 --name moonrisekingdom
```

Transform a video
```
python main.py --input_data transcripts/street.json --input_seconds 0,5 --transform_src videos/her.avi --transform_data transcripts/her.json
```

Get the pretrained model from [here](https://drive.google.com/open?id=1tSTzD21qXXOiXlfgJllgXNZ9lREy6yij)

## License

MIT