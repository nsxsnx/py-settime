path = '//support/incoming/asued/'
masks = ['*.fmx', '*.exe']

import os, datetime, time, random, glob
import pywintypes, win32file, win32con

class GMT_4(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=4)
    def dst(self, dt):
        return datetime.timedelta(0)

def changeFileCreationTime(fname, newtime):
    wintime = pywintypes.Time(newtime)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None)
    win32file.SetFileTime(winfile, wintime.replace(tzinfo=GMT_4()), None, None)
    winfile.close()

def settime(file, mtime):
    atime = (datetime.datetime.now() + datetime.timedelta(days=-1, minutes=-64)).timestamp()
    os.utime(file, (atime, mtime))
    changeFileCreationTime(file, mtime)

def getrtime():
    while True:
        res = datetime.datetime(2002, 1, 10, 10, 00) + datetime.timedelta(days = random.randint(0,1825), minutes = random.randint(0, 420), seconds = random.randint(0, 60))
        if res.weekday() < 5: return res
 
# entry point
for root, dirs, files in os.walk(path):
    for mask in masks:
        for file in glob.glob(os.path.join(root, mask)):
            print(file)
            try: settime(file, getrtime().timestamp())
            except: print('EXCEPT')
