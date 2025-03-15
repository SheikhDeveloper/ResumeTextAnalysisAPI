import json
from model_manager import ModelManager
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/resume_analysis/predict', methods=['GET'])
def predict(resume_text: str) -> str:
    '''
    @brief: Analyzes the resume's content and predicts whether it is substantive or not
    @param resume_text: str - Text of the resume to analyze
    '''
    if request.method == 'GET':
        model_manager = ModelManager()
        try:
            result = model_manager.get_prediction(resume_text)
        except TypeError:
            response = make_response("Non-text input.")
            response.status_code = 400
            return response
        result = json.dumps(result)
        response = make_response(result)
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.run()
