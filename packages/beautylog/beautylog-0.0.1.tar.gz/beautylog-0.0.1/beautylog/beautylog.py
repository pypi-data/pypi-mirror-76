import time
from functools import wraps


def writeFile(file_path, mode, content):
    with open(file_path, mode) as f:
        f.write(content + '\n')


def readFile(file_path):
    with open(file_path) as f:
        print(f.read())


def writeLog(msg):
    msg = str(msg)
    run_time = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    writeFile(__file__ + 'debug.log', 'a', run_time + msg)
    print(run_time + msg)


def failExsit(err):
    writeLog('[[ERROR]] : %s ' % err)


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
