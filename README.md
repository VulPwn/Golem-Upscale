# Golem-Upscale
Image Resolution Upscaling using SRGAN on Golem

Golem Upscale can be run just by placing an image in the data folder and running requestor.py or by running the accompanied flask app.

The project uses the model created by the SRGAN-tensorflow team to upscale the resolution of images by 4x. I wanted to add other features to the app, 
such as increasing the resolution of video or gifs, or to scale images more reliably up to or past 4k, but ultimately I ran out of time to implement those features
and finish on time.

The project sends individual images to different providers to process the images in parallel. I believe it would be trivial to refactor this project 
to upscale video this way by increasing the batch size per provider and/or by batching and compressing the frames before sending the frames to providers.
