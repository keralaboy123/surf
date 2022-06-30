from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster

import threading
import asyncio
import time
import addon

#thread example borrowed from https://gist.github.com/BigSully/3da478792ee331cb2e5ece748393f8c4

def  threadloop(loop, master):
    asyncio.set_event_loop(loop)
    #master.run_loop(loop.run_forever)


class prox:
    def __init__(self,host='0.0.0.0',port=8080,addon=object()):
       self.options = Options(listen_host=host, listen_port=port, http2=True)
       self.dumpmaster = DumpMaster(self.options, with_termlog=False, with_dumper=False)
       self.config = ProxyConfig(self.options)
       self.dumpmaster.server = ProxyServer(self.config)
       self.dumpmaster.addons.add(addon)
       self.dumpmaster
       self.loop = self.dumpmaster.channel.loop
       self.thread = threading.Thread(target=threadloop, args=(self.loop, self.dumpmaster))


    def starter(self):
        print("starting mitmproxy")
        self.thread.start()


    def stoper(self):
        print("stoping mitmproxy")
        #self.loop.stop()
        self.dumpmaster.shutdown()



class AddonDemo(object):
    def request(self, flow):
        print("@request received = "+flow.request.url)

    def response(self, flow):
        print("@responce received")

def run():
    proxy=prox(addon=AddonDemo())
    proxy.starter()
    time.sleep(20)
    proxy.stoper()


if __name__ == "__main__":
    run()
    time.sleep(1)
    run()
