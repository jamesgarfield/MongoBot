import os

from time import mktime, localtime, sleep

print "The doctor is in"
while True:
    pulse = open('/tmp/bot.pulse', 'r')
    lastpulse = pulse.readline()
    if mktime(localtime()) - float(lastpulse) > 25:
        print "He's dead, Jim"
        os.system("ps ax | grep 'medulla.py' | grep -v grep | awk '{print $1}' | xargs kill")
        os.system("python medulla.py >> hippocampus/log/sys.log 2>>hippocampus/log/error.log &")
        print "It's cool, we had the thingy"
    sleep(10)
