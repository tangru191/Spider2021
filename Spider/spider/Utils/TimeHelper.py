import time

"""
#@Time:2018
#@Author:tangru
"""


class TimeHelper:
    def getTime(self):
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return currentTime
