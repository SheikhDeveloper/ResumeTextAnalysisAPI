import json
from model_manager import ModelManager
from flask import Flask, request, make_response
import requests

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
        model_manager = ModelManager()
        json_resp = get(URL, 'datasheets/' + datasheet_id + '/records', headers={'Authorization': 'Bearer ' + token})['data']
        if json_resp['code'] != 200:
            response = make_response(json_resp['message'])
            response.status_code = 400
            return response
        resume_texts = [record['Что готов дать компании?'] for record in json_resp]
        try:
            results = model_manager.get_prediction(resume_texts)
        except TypeError:
            response = make_response("Non-text input.")
            response.status_code = 400
            return response
        result = json.dumps({'ответ модели': results})
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        resp = requests.patch(URL + 'datasheets/' + datasheet_id + '/records', headers=headers, data=result)

        if resp.status_code != 200:
            response = make_response(resp.json()['message'])
            response.status_code = 400
            return response

        response = make_response("Success.")
        response.status_code = 200
        return response

if __name__ == '__main__':
    app.run()
