from transformers import AutoModelForSequenceClassification, AutoTokenizer



model = AutoModelForSequenceClassification.from_pretrained("javidjamae/autotrain-movie-sentiment-86557143111", token=access_token)

tokenizer = AutoTokenizer.from_pretrained("javidjamae/autotrain-movie-sentiment-86557143111", token=access_token)

inputs = tokenizer("I love AutoTrain", return_tensors="pt")

outputs = model(**inputs)
