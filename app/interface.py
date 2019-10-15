from flask import Flask, redirect, request
from flask_cors import CORS
from api_management import getpaths, refreshpaths, checkTokenValiditi



app = Flask(__name__)
CORS(app)


@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(path):

    redirect_path = setpath(path)
    if redirect_path == '404':
        return {'msg': 'Path not found'}, 404
    elif 'usermanagement' in redirect_path:
        return redirect(redirect_path, code=307)
    else:
        print('Requested path: ' + redirect_path + ' | Requested method: ' + request.method)
        data = checkTokenValiditi(request)

        if data == 401:
            return {'msg': 'JWT has expired.'}, 401
        elif data == 400:
            return {'msg': 'Invalid JWT token'}, 401
        elif data == 403:
            return {'msg': 'Authorization header not present'}, 403

        return redirect(redirect_path, code=307)


@app.route('/registerapi/', methods=['GET', 'POST'])
def registerapi():
    if request.method == 'GET':
        return getpaths()
    elif request.method == 'POST':
        return refreshpaths()


def setpath(path):
    path_dict = getpaths()
    apiname = path.split('/')[0]
    if apiname in path_dict:
        apipath = path_dict[apiname] + path
        return apipath
    else:
        print('Path not found: ' + path)
        return '404'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
