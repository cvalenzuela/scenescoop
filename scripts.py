# get frames and run model over video
python main.py --video videos/her.mkv --name her2 

# transform a video
python main.py --input_data transcripts/food.json --input_seconds 0,5 --transform_src videos/samsara.avi --transform_data transcripts/samsara.json