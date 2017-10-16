from datetime import datetime

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(object):
    """This takes care of all Logging"""

    __metaclass__ = Singleton

    def __init__(self, log_path, filename):
        super(Logger, self).__init__()
        self.arg = arg

        log_path = join(BENCHMARKS_FOLDER, SFN_PREFIX)
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        LOG_FILE = open(join(log_path, SFN_PREFIX+'.log'), 'a')

    @classmethod
    def log(self, message):
        timestamp = datetime.now().strftime('%d.%m.%y %H:%M:%S > ')
        try:
            LOG_FILE.write(timestamp + message + '\n')
        except:
            print "[WARNING] No LOG_FILE not defined. -> Debug mode."
        print timestamp + message

