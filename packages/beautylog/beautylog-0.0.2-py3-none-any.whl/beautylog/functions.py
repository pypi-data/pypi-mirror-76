import time
from functools import wraps
import os
#python setup.py sdist bdist_wheel 
#python -m twine upload dist/*

def writeFile(file_path, mode, content):
    with open(file_path, mode) as f:
        f.write(content + '\n')


def readFile(file_path):
    with open(file_path) as f:
        print(f.read())


def writeLog(msg, file_dir = os.path.dirname(__file__)):
    msg = str(msg)
    run_time = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    writeFile(os.path.join(file_dir, 'debug.log'), 'a', run_time + msg)
    print(run_time + msg)


def failExsit(err, file_dir = __file__):
    writeLog('[[ERROR]] : %s ' % err, file_dir)


def logDecoration(func):
    @wraps(func)
    def log(*args, **kwargs):
        try:
            writeLog("[" + func.__name__ + "] was called")
            func_return = str(func())
            writeLog("[" + func.__name__ + "] return [%s]" % func_return)
        except Exception as err:
            failExsit("[" + func.__name__ + "] " + str(err))
    return log

def logDecorationDebug(func):
    file_dir = os.path.dirname(func.__code__.co_filename)
    @wraps(func)
    def log(*args, **kwargs):
        try:
            writeLog("[" + func.__name__ + "] was called", file_dir)
            func_return = str(func())
            writeLog("[" + func.__name__ + "] return [%s]" % func_return, file_dir)
        except Exception as err:
            failExsit("[" + func.__name__ + "] " + str(err))
    return log
