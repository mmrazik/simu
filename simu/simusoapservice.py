import bottle
from bottle import route, run, request, abort
bottle.debug(True)

@route('/up/:channel', method='GET')
def up(channel):
   print channel
   callback = request.GET.get('callback')
   return "{callback}({{result: \"false\"}})".format(callback=callback, channel=channel)

def simu_soap_service():
    """ Entry point for simu-soap-service """
    run(host="0.0.0.0", port=7777)
