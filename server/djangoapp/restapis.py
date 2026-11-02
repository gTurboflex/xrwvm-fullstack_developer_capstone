import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    response = requests.get(backend_url.rstrip('/') + '/' + endpoint.lstrip('/'), params=kwargs, timeout=15)
    response.raise_for_status()
    return response.json()

def analyze_review_sentiments(text):
    response = requests.get(sentiment_analyzer_url.rstrip('/') + '/analyze/' + requests.utils.quote(text), timeout=15)
    response.raise_for_status()
    return response.json()

def post_review(data_dict):
    response = requests.post(backend_url.rstrip('/') + '/insert_review', json=data_dict, timeout=15)
    response.raise_for_status()
    return response.json()
