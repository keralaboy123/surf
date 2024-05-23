from mitmproxy.tools.main import run
from mitmproxy import master as dump
import asyncio
import signal
from mitmproxy import options
from mitmproxy.addons import dumper, errorcheck, keepserving, readfile, termlog
from mitmproxy import addons

"this code is important we can extend this so we can create a gui for this python api."

class CustomServerAddon:
    def __init__(self,master):
        self.master = master
        
    def request(self, flow):
        print("got a reqest ", flow.request.url)
 
    def response(self, flow):
        print("got a responce :", flow.request.url)

class surf:
    ip= "127.0.0.1"
    port = 8080
    
    async def __run(self,opts=None):
        self.opts = opts or options.Options(listen_host= self.ip ,listen_port = self.port)
        self.loop = asyncio.get_event_loop()
        self.master = dump.Master(self.opts,event_loop=self.loop)
        self.master.addons.add(CustomServerAddon(self))
        self.master.addons.add(termlog.TermLog())
        self.master.addons.add(*addons.default_addons())
        self.master.addons.add(
            keepserving.KeepServing(),
            readfile.ReadFileStdin(),
            errorcheck.ErrorCheck(),
        )
        signal.signal(signal.SIGINT, self.stop_from_terminal)
        signal.signal(signal.SIGTERM, self.stop)
        await self.master.run()
        return  self.master
        
    def run(self):
        asyncio.run(self.__run())
        
    def stop_from_terminal(self, *_):
        self.loop.call_soon_threadsafe(getattr(self.master, "prompt_for_exit", self.master.shutdown))

    def stop(self,*_):
        self.loop.call_soon_threadsafe(self.master.shutdown)


if __name__ == "__main__":
   surf_class = surf()
   print("running")
   surf_class.run()
   print("stoped .. ")



