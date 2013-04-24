#!/usr/bin/env python
import os
os.chdir(os.path.dirname(__file__))

from bottle import route, default_app, request


@route('/up/:channel', method='POST')
def up(channel):
   return {'result': True}


application = default_app()
