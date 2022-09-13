# download BERT_LARGE model
python download.py # this will download the model to ./bert_large_model and run the test

# start the tensorflow serving
docker run -p 8501:8501 --mount type=bind,source=/home/fy/Desktop/gsl_dev/Serverless-sample-apps/python/bert_large_model,target=/models/bert_large_model -e MODEL_NAME=bert_large_model -t tensorflow/serving &

# run the test
python client.py