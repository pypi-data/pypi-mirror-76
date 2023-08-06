"""
client side api and implementation
"""

import logging
import json
from threading import Thread
from k3process import rpc
import threading
import time

logger = logging.getLogger(__name__)
stubLogger = logging.getLogger("stub_call_logger")
# logger = None
# moduleNm = __name__

class _Traget():
    
    def __init__(self, proxyClient):
        self.targetTarget = None
        self.proxyClient = proxyClient
    
    def _retister_target(self, targetTarget):
        self.targetTarget = targetTarget
    
    def call_on_client_stub(self, functionName, kwargs):
        logger.info("Client side call_on_client_stub received: {} {}".format(functionName, kwargs))
        if self.targetTarget:
            return self.targetTarget(functionName, kwargs)
        else:
            logger.warning("Recveid msg on stub side, but not target has been registered. Raising error for callee")
            raise RuntimeError("No c callback set to forward client call to")
        
    def shortcut_proxy_calls(self, functionName, argListForNCalls):
        """
        For the given function when forward_proxy_stub_call is called,
        return the values from argListForNCalls instead for the
        next len(argListForNCalls) calls 
        """
        self.proxyClient._short_cut_n_proxy_calls(functionName, argListForNCalls)
        
        
            

class ProxyClient:
    
    def __init__(self, config):
        self.proxyRunningEvent = threading.Event()
        self.config = config
        with open(self.config["stub_function_definition"]) as fh:
            self.stubFuncDef = json.load(fh)
        
        self.stubCallLogHandle = None
        if config["stub_call_log_path"]:
            fmtStr = "%(asctime)s: %(message)s"
            fh = logging.FileHandler(config["stub_call_log_path"])
            fh.setFormatter(logging.Formatter(fmtStr))
            stubLogger.addHandler(fh)
            
        self.recvThread = Thread(target=self._run, name="stub_client_proxy_recv")
        self.target = _Traget(self)
        self.remoteTarget = None
        logging.debug("ProxyClient init complete")
        self.callCount = 0
        self.shortCutLock = threading.Lock()
        self.shortCutDict = {}
            
    def get_function_parameters(self, functionName):
        try:
            methodArgs = self.stubFuncDef[functionName]["parameters"]
            for arg in methodArgs:
                _a1, _a2, _a3 = arg
        except Exception:
            logger.warning(f"Function definition for function {functionName} in the wrong format")
            raise
        return methodArgs
    
    def register_server_to_client_target_func(self, aCallable):
        self.target._retister_target(aCallable)
    
    def _run(self):
        try:
            logger.debug("Connecting to server")
            with rpc.K3RPCClient("stub_client", self.config["host"], self.config["port"], self.config["auth_key"].encode('utf-8')) as rpcClientSession:
                logger.info("Connecting to server successful")
                rpcClientSession.set_target(self.target)
                rpcClientSession.wait_remote_target_set()
                self.remoteTarget = rpcClientSession.get_remote_target_proxy()
                self.proxyRunningEvent.set()
                rpcClientSession.wait_remote_close()
                logger.info("Server terminated client server connection")
        except Exception as e:
            logger.error("Proxy client receive thread raised an exception", exc_info=True)
        finally:
            logger.info("Proxy client receive thread done")
            
    def _short_cut_n_proxy_calls(self, functionName, argListForNCalls ):
        """
        For the given function when forward_proxy_stub_call is called,
        return the values from argListForNCalls instead for the
        next len(argListForNCalls) calls 
        """
        with self.shortCutLock:
            if functionName in self.shortCutDict:
                raise RuntimeError(f"{len(self.shortCutDict[functionName])} values already in shortcut dict for function {functionName}")
            self.shortCutDict[functionName] = argListForNCalls
        
            
    def forward_proxy_stub_call(self, functionName, kwargs):
        logger.debug(f"forward_proxy_stub_call {functionName} called. Args: {kwargs}")
        
        if self.remoteTarget == None:
            logger.error("Cannot forward stub call as proxy is not running")
            raise RuntimeError("Cannot forward stub call as proxy is not running") 
        
        self.callCount += 1
#         if self.callCount % 100 == 0:
#             print(self.callCount)

        ret = None
        with self.shortCutLock:
            if functionName in self.shortCutDict:
                ret = self.shortCutDict[functionName].pop(0)
                logger.debug(f"Returning for function {functionName} a shortcut value {ret}. Remaining vals for func: {len(self.shortCutDict[functionName])}")
                
                if len(self.shortCutDict[functionName]) == 0:
                    self.shortCutDict.pop(functionName, None)
        
        if ret == None:
            ret = self.remoteTarget.proxy_stub_call(functionName, kwargs)
        stubLogger.debug("{:40} {:44} -> {}".format(functionName, str(kwargs), str(ret)))
        return ret
    
    def start_proxy_async(self):
        self.recvThread.start()
        self.proxyRunningEvent.wait(2)
        
def init_proxy_client(stubConfig) -> ProxyClient:
    global logger
    try:
        with open(stubConfig) as fh:
            config = json.load(fh)
        logging.basicConfig(level=config["log_level"].upper(), format="%(asctime)s %(levelname)s: %(message)s")
    #     logger = logging.getLogger(moduleNm)
        prx =  ProxyClient(config)
        logger.info("Proxy connection/recv thread started")
        prx.start_proxy_async()
    except:
        logger.exception("Error in k3stubproxy.init_proxy_client")
        raise
    else:
        logger.info("init_proxy_client complete")
    return prx
        