#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import signal
import logging
import logging.handlers
import daemonize
import subprocess
import wiringpi as wp


NAME = 'rasptea1_motion_state'
AUDIOFILE = '/home/pi/rasptea1/TEA_pt1_fin.wav'
PIDFILE = '/var/run/%s' % (NAME,)
LOGFILE = '/var/log/%s.log' % (NAME,)


def init_logger(name):
   logger = logging.getLogger(name)
   handler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=100000, backupCount=10)
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   handler.setLevel(logging.INFO)
   handler.setFormatter(formatter)
   logger.addHandler(handler)
   logger.setLevel(logging.INFO)
   return logger


logger = init_logger('rasptea1.motion_state')


def main():
    plogger = init_logger('rasptea1.player')
    # init WiringPi
    wp.wiringPiSetup()
    # set pin 4 to input mode
    wp.pinMode(4, 0)
    # keep player status
    playerActive = False
    # infinite loop
    while True:
        try:
            # read sensor state
            motionState = wp.digitalRead(4)
            if motionState == 1 and not playerActive:
                player = subprocess.Popen(['omxplayer', '-o', 'local', AUDIOFILE],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
                plogger.info('Player started')
                playerActive = True
                # wait for audio played completely
                player.wait()
                plogger.info('Player stopped')
                playerActive = False
        except Exception as e:
            plogger.error('Player error in loop occured %s' % (e,))
    # wait for 100 ms
    wp.delay(100)


def getpid():
    try:
        pf = file(PIDFILE, 'r')
        pid = int(pf.read().strip())
        pf.close()
        return pid
    except (IOError, SystemExit, TypeError, ValueError) as e:
        return None


def start():
    daemon = daemonize.Daemonize(app=NAME, pid=PIDFILE, action=main)
    daemon.start()
    return True


def stop():
    pid = getpid()
    if pid:
        os.kill(pid, signal.SIGTERM)
        return True
    return False


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            msg = '%s was started' % (NAME,)
            print msg
            logger.info(msg)
            start()
        elif sys.argv[1] == 'stop':
            if stop():
                msg = '%s was stopped' % (NAME,)
                print msg
                logger.info(msg)
            else:
                print "%s wasn't running" % (NAME,)
        elif sys.argv[1] == 'restart':
            if stop():
                print '%s was stopped' % (NAME,)
            else:
                print "%s wasn't running" % (NAME,)
            print '%s was started' % (NAME,)
            logger.info('%s was restarted' % (NAME,))
            start()
        elif sys.argv[1] == 'status':
	   pid = getpid()
           if pid:
               print '%s is running as pid %s.' % (NAME, pid)
           else:
               print '%s is not running.' % (NAME,)
        else:
            print "Unknown command"
            sys.exit(2)
    else:
        print "Usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)

