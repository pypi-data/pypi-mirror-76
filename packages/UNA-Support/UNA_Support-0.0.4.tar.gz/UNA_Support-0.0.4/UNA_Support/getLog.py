import os

from datetime import *

class Log:

    def __init__(self, filename, path):
        date_now = datetime.now().strftime("%Y%m%d")
        self.filename = path + '\\' + date_now + '_' + filename + '.log'
        try:
            os.makedirs(path)
        except:
            pass

    def info(self, text):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f = open(self.filename, "a")
        f.write(date_now + ': INFO -     ' +str(text) + '\n')
        f.close()

    def error(self, text):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f = open(self.filename, "a")
        f.write(date_now + ': ERROR -     ' +str(text) + '\n')
        f.close()

    def start(self, text):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f = open(self.filename, "a")
        f.write(date_now + ': START - ' + str(text) + '\n')
        f.close()

    def end(self, text):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f = open(self.filename, "a")
        f.write(date_now + ': END - ' + str(text) + '\n\n')
        f.close()

    def text_tab(self, text):
        f = open(self.filename, "a")
        f.write('\t\t\t\t\t\t' +str(text) + '\n')
        f.close()

    def empy_line(self):
        f = open(self.filename, "a")
        f.write('\n')
        f.close()
