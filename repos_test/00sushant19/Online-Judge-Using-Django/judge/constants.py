from online_judge.settings import BASE_DIR

# FILES AND DIRECTORIES
CODES_DIR = 'judge/'
# project path in host file system
HOST_PATH = str(BASE_DIR)
# container path where all code files reside
CONT_PATH = ''
# max length of user submitted code
MAX_CODE_LENGTH = 10000


class Judge:
    GCCCONT = 'gcccon'
    GCCIMG = 'gcc:11.2.0'
    GCC = 'GNU GCC C11 11.2.0'
    GPP20 = 'GNU G++20 11.2.0'
    GPP17 = 'GNU G++17 11.2.0'
    GPP14 = 'GNU G++14 11.2.0'

    PY2CON = 'py2con'
    PY2IMG = 'python:2.7.18'
    PY2 = 'Python 2.7.18'

    PY3CON = 'py3con'
    PY3IMG = 'python:3.8.11'
    PY3 = 'Python 3.8.10'