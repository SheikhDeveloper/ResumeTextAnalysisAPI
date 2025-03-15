# A simple API on Flask with a model (NBC) that analyzes TF-iDF representation of the resume text and predicts whether it is substantive.  

## About the project

The project is a simple API on Flask with a model (NBC) that analyzes TF-iDF representation of the resume text and predicts whether it is substantive. It was created for the [case competition from Changellenge](https://changellenge.com/championships/changellenge-cup-it-2025/?utm_source=cl-site&utm_medium=main&utm_campaign=slider) for the B2B analytics case solution from team HotimIT.

## How to use it

1. Clone this repo
2. `pip install -r requirements.txt`
3. `python3 server.py`

## About the model

The model is trained using the [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) representation of the resume text.

The [dataset](./train/texts.csv) for the model was created using the example phrases from the Internet

The model itself represents the [Naive Bayes Classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) on the Multinomial distribution of the features, with the smoothing parameter set to 1.0 (see [scikit-learn documentation](https://scikit-learn.org/stable/modules/naive_bayes.html#multinomial-naive-bayes))

## About the API

The API is made with [Flask](https://flask.palletsprojects.com/) and [Flask-RESTX](https://flask-restx.readthedocs.io/en/stable/).

It helps you to predict whether the resume is substantive or not.

The description of the API can be found [here](./model.yaml)
