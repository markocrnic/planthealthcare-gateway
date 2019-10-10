from flask import Flask, redirect, request
from flask_cors import CORS
from api_management import paths
import jwt


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


def setpath(path):
    path_dict = paths()
    apiname = path.split('/')[0]
    if apiname in path_dict:
        apipath = path_dict[apiname] + path
        return apipath
    else:
        print('Path not found: ' + path)
        return '404'


def checkTokenValiditi(request):
    secret = 'planthealthcare'
    try:
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.split('Bearer ', 1)[1]
    except:
        print('Authorization header not present.')
        return 403

    try:

        decoded = jwt.decode(token, secret, algorithms=['HS256'])
        return decoded

    except jwt.ExpiredSignatureError:
        print('JWT token expired')
        return 401

    except:
        print('Invalid JWT token')
        return 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
