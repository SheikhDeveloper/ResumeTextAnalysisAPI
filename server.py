import json
from model_manager import ModelManager
from flask import Flask, request, make_response
import requests
from tf_idf_vectorize import Vectorizer
import sys

sys.modules['tf_idf_vectorize'] = sys.modules[__name__]
sys.modules['__main__'].Vectorizer = Vectorizer

app = Flask(__name__)

URL = 'https://true.tabs.sale/fusion/v1/'

datasheet_id = 'dstt21vbXFvXvoqE9H'

with open('token.env') as f:
    token = f.read().strip()

def get(url, path, headers=None, body=None, params=None):
    if headers is None:
        headers = {}
    url = url + path
    return requests.get(url, headers=headers, params=params).json()

@app.route('/resume_analysis/predict', methods=['GET'])
def predict():
    '''
    @brief: Analyzes the resume texts' contents and predicts whether they are substantive or not
            and sends the result to the True Tabs
    '''
    if request.method == 'GET':
        print("Request received.")
        model_manager = ModelManager()
        json_resp = get(URL, 'datasheets/' + datasheet_id + '/records', headers={'Authorization': 'Bearer ' + token})
        if json_resp['code'] != 200:
            response = make_response(json_resp['message'])
            response.status_code = 400
            return response
        print("Successful request for input.")
        json_resp = json_resp['data']
        resume_texts = [record['fields']['Что готов дать компании?'][0] for record in json_resp['records']]
        record_ids = [record['recordId'] for record in json_resp['records']]
        try:
            results = model_manager.get_prediction(resume_texts)
        except TypeError:
            response = make_response("Non-text input.")
            response.status_code = 400
            return response
        result = json.dumps({'records': [ { 'recordId': record_id, 'fields': {'ответ модели': 'субъективно' if i == 1 else 'несубъективно'} } for record_id, i in zip(record_ids, results)]
                                          })
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        resp = requests.patch(URL + 'datasheets/' + datasheet_id + '/records', headers=headers, data=result)

        if resp.json()['code'] != 200:
            response = make_response(resp.json()['message'])
            response.status_code = 400
            return response
        print("Successful request for changes.")

        response = make_response("Success.")
        response.status_code = 200
        return response

if __name__ == '__main__':
    app.run()
