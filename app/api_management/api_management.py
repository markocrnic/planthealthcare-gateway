from ast import literal_eval
import ftputil
import jwt
from loadconfig import load_config


config = load_config('config/config.yml')

PATH_DICT = {}


def readpathsfromftp():

    try:
        f = open('paths.txt', 'r')
        content = f.read()

        return content

    except:
        return refreshpaths()


def getpaths():
    content = readpathsfromftp()
    PATH_DICT = literal_eval(content)

    return PATH_DICT


def refreshpaths():
    try:
        a_host = ftputil.FTPHost(config['ftp']['host'], config['ftp']['user'], config['ftp']['password'])

        for (dirname, subdirs, files) in a_host.walk(config['ftp']['path']):
            for f in files:
                if f == 'paths.txt':
                    a_host.download(dirname + f, f)
                    with open(f) as txtfile:
                        content = txtfile.read()
                        print(str(content))
        a_host.close()

        return content

    except Exception as e:
        print(e)
        a_host.close()


def setpath(path):
    path_dict = getpaths()
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

