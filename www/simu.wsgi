#!/usr/bin/env python
import os
os.chdir(os.path.dirname(__file__))
import subprocess

from bottle import route, default_app, request

simu_remote = ['sudo', '/home/mmrazik/simu/bin/simu-remote']


def operation(operation, channel):
   call = simu_remote + ['-c', channel, '-o', operation]
   try:
       subprocess.check_call(call)
       return {'result': True}
   except subprocess.CalledProcessError as e:
       return {'result': False,
               'error': e.message}
      

@route('/up/:channel')
def up(channel):
    return operation('up', channel)


@route('/down/:channel')
def down(channel):
    return operation('down', channel)


@route('/stop/:channel')
def stop(channel):
    return operation('stop', channel)

application = default_app()
