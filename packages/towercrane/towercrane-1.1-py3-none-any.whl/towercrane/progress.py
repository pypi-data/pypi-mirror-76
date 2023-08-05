import os
import sys
import threading
from os.path import getsize
import time

class ProgressPercentage(object):
    """
    ProgressPercentage
    """
    def __init__(self, file_name, size):
        self._filename = file_name
        self._size = size
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def printBar (self,iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        if iteration == total: 
            print()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            self.printBar(self._seen_so_far, self._size, prefix = self._filename+".zip" , suffix = 'Complete', length = 50)

