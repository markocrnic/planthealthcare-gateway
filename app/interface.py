from flask import Flask, redirect, request
from flask_cors import CORS
from api_management import paths


app = Flask(__name__)
CORS(app)


@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(path):

    redirect_path = setpath(path)
    if redirect_path == '404':
        return {'msg': 'Path not found'}, 404
    else:
        print('Requested path: ' + redirect_path + ' | Requested method: ' + request.method)
        return redirect(redirect_path, code=307)


def setpath(path):
    path_dict = paths()
    apiname = path.split('/')[0]
    if apiname in path_dict:
        apipath = path_dict[apiname] + path
        return apipath
    else:
        print('Path not found: ' + path)
        return '404'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
