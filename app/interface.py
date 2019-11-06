from flask import Flask, redirect, request, make_response
import requests
import json
from flask_cors import CORS
from api_management.api_management import getpaths, refreshpaths, checkTokenValiditi, setpath, createresponse
from api_management.jaeger import initializejaeger


app = Flask(__name__)
CORS(app)
tracer = initializejaeger()


@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(path):
    with tracer.start_active_span('Gateway call: ' + path + ': ' + request.method) as scope:

        redirect_path = setpath(path)

        scope.span.log_kv({'event': 'Call through gateway', 'url': redirect_path})

        if redirect_path == '404':
            return {'msg': 'Path not found'}, 404
        elif 'usermanagement' in redirect_path:
            request_data = requests.post(redirect_path, headers={'content-type': 'application/json'}, data=json.dumps(request.json))
            response = make_response(request_data.content)
            response.headers['Content-Type'] = 'application/json'
            return response, request_data.status_code
        else:
            print('Requested path: ' + redirect_path + ' | Requested method: ' + request.method)

            token_status = checkTokenValiditi(request)

            if token_status == 401:
                return {'msg': 'JWT has expired.'}, 401
            elif token_status == 400:
                return {'msg': 'Invalid JWT token'}, 401
            elif token_status == 403:
                return {'msg': 'Authorization header not present'}, 403

            api_name = path.split('/')[0]
            request_data = {'method': request.method, 'api_name': api_name, 'redirect_path': redirect_path}

            if request.method == 'POST' or request.method == 'PUT':
                request_data['data'] = request.json
            else:
                request_data['data'] = None

            response, status_code = createresponse(request_data)

            return response, status_code


@app.route('/registerapi/', methods=['GET', 'POST'])
def registerapi():
    with tracer.start_active_span('Client test method') as scope:
        scope.span.log_kv({'event': 'Call to register api', 'request_method': request.method})

        if request.method == 'GET':
            return getpaths()
        elif request.method == 'POST':
            return refreshpaths()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
