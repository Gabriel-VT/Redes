from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os
import functools

pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-12efc6a7-dbc9-44cd-91df-d4977f237ed8'
pnconfig.subscribe_key = 'sub-c-724ad54c-da65-11e9-a6c8-3e57a349bb32'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

addr = input('digite seu apelido: ')

def checksum(st):
  return functools.reduce(lambda x,y:x+y, map(ord, st))

def my_publish_callback(envelope, status):
  # Check whether request successfully completed or not
  if not status.is_error():
    pass

class MySubscribeCallback(SubscribeCallback):
  def __init__(self):
    self.__addr = addr

  def presence(self, pubnub, presence):
    pass

  def status(self, pubnub, status):
    pass
  def parse_text(self, text):
    lista=text.split('; ')
    dic={}
    for i in range(len(lista)):
      if ': ' in lista[i]:
        lista[i]=lista[i].split(': ')
        try:
          dic[lista[i][0]]=int(lista[i][1])
        except:
          dic[lista[i][0]]=lista[i][1]
    return dic

  def message(self, pubnub, message):
    received=self.parse_text(message.message)
    if received['Sender'] != self.__addr: print(received)


class P2P(): 
  def __init__(self):
    self.__addr = addr
  
  def run(self):
    try: 
      channel=input('digite o canal: ')
      pubnub.add_listener(MySubscribeCallback())
      pubnub.subscribe().channels(channel).execute()
      ## publish a message

      while True:
        content = input("Input a message to publish: ")

        sequence=0
        check=checksum(content)

        header='Sender: '+str(self.__addr)+'; Seq: '+ str(sequence)+'; Checksum: '+str(check)+'; Content: '
        message=header+str(content)+'; '

        if content == 'exit': os._exit(1)
        pubnub.publish().channel(channel).message(str(message)).pn_async(my_publish_callback)

    except Exception as e:
      print(e)

    finally:
      os._exit(1)

iniciaServico = P2P()
iniciaServico.run()