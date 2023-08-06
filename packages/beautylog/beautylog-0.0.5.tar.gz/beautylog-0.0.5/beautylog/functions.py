import time
from functools import wraps
import os
import sys
import traceback
STDOUT = sys.stdout
#python setup.py sdist bdist_wheel 
#python -m twine upload dist/*



def writeFile(file_path, mode, content):
    with open(file_path, mode) as f:
        f.write(content + '\n')


def readFile(file_path):
    with open(file_path) as f:
        print(f.read())


def writeLog(msg, file_dir = os.path.dirname(__file__), is_n = ''):
    msg = str(msg)
    run_time = time.strftime(is_n + "%Y-%m-%d %H:%M:%S ", time.localtime())
    writeFile(os.path.join(file_dir, 'debug.log'), 'a', run_time + msg)
    print(run_time + msg)


def failExsit(err, file_dir = os.path.dirname(__file__)):
    writeLog('[[ERROR]] : %s ' % err, file_dir)


class __BeautyLogOut__:
    def __init__(self, func):
        self._buff = ''
        self.func_name = func.__name__

    def write(self, out_stream):
        if out_stream not in ['', '\r', '\n', '\r\n']:
            self_out = sys.stdout
            sys.stdout = STDOUT
            writeLog("[%s] %s" % (self.func_name, out_stream))
            sys.stdout = self_out

    def flush(self):
        self._buff = ""


def logDecoration(func):
    file_dir = os.path.dirname(func.__code__.co_filename)
    @wraps(func)
    def log(*args, **kwargs):
        try:
            writeLog("[%s] was called" % func.__name__, file_dir, '\n')
            beauty_out = __BeautyLogOut__(func)
            sys.stdout = beauty_out
            func_return = str(func(*args, **kwargs))
            sys.stdout = STDOUT
            writeLog("[%s] return [%s]" % (func.__name__, func_return), file_dir)
        except Exception as err:
            failExsit("[%s] %s" % (func.__name__, str(err)), file_dir)
    return log

if __name__ == "__main__":

    @logDecorationDebug
    def my():
        print('a')
        print('b')

    @logDecorationDebug
    def main():
        print("main")
        my()
    main()