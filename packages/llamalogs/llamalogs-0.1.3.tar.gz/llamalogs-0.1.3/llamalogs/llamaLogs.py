import threading 
import traceback
import schedule

from llamalogs.logAggregator import LogAggregator
from llamalogs.log import Log
from llamalogs.returnLog import ReturnLog
from llamalogs.stat import Stat
from llamalogs.llamaProxy import LlamaProxy

class LlamaLogs:
    globalAccountKey = ''
    globalGraphName = ''
    isDisabled = False
    commThread = None

    @staticmethod
    def init(options = {}):
        try:
            if ("accountKey" in options):
                LlamaLogs.globalAccountKey = str(options["accountKey"])
            if ("graphName" in options):
                LlamaLogs.globalGraphName = str(options["graphName"])
            if ("isDevEnv" in options):
                LlamaProxy.isDevEnv = options["isDevEnv"] or False
            if ("disabled" in options):
                LlamaLogs.isDisabled = options["disabled"] or False

            if LlamaLogs.commThread is None and LlamaLogs.isDisabled is False:
                LlamaLogs.commThread = threading.Thread(target=LogAggregator.start_timer)
                LlamaLogs.commThread.daemon = True
                LlamaLogs.commThread.start()
        except:
            print("`LlamaLogs Error: init function")
    
    @staticmethod
    def stop():
        try:
            if LlamaLogs.commThread is not None:
                schedule.clear()
                LlamaLogs.commThread = None
        except:
            print("`LlamaLogs Error: stop function")

    @staticmethod
    def point_stat(options = {}):
        try:
            if LlamaLogs.isDisabled: 
                return
            options["type"] = "point"
            LlamaLogs.processStat(options)
        except:
            print("LlamaLogs Error: point_stat function")

    @staticmethod
    def avg_stat(options = {}):
        try:
            if LlamaLogs.isDisabled: 
                return
            options["type"] = "average"
            LlamaLogs.processStat(options)
        except:
            print("LlamaLogs Error: avg_stat function")

    @staticmethod
    def max_stat(options = {}):
        try:
            if LlamaLogs.isDisabled: 
                return
            options["type"] = "max"
            LlamaLogs.processStat(options)
        except:
            print("LlamaLogs Error: max_stat function")

    @staticmethod
    def log(options = {}, returnLog = None):
        try:
            if LlamaLogs.isDisabled: 
                return
            return LlamaLogs.processLog(options, returnLog)
        except:
            print("LlamaLogs Error: log function")
            traceback.print_exc()

    @staticmethod
    def force_send():
        try:
            if LlamaLogs.isDisabled: 
                return
            LogAggregator.send_messages()
        except:
            print("LlamaLogs Error: force_send function")

    @staticmethod
    def processStat(options = {}):
        stat = Stat()
        stat.component = options["component"]
        stat.name = options["name"]
        stat.value = options["value"]
        stat.type = options["type"]

        if ("accountKey" in options):
            stat.account = options["accountKey"]
        else:
            stat.account = LlamaLogs.globalAccountKey or -1 

        if ("graphName" in options):
            stat.graph = options["graphName"]
        else:
            stat.graph = LlamaLogs.globalGraphName
        
        LogAggregator.add_stat(stat)

    @staticmethod
    def processLog(options = {}, returnLog = {}):
        if (returnLog is not None):
            options["s"] = returnLog.sender
            options["r"] = returnLog.receiver
            options["initialMessage"] = returnLog.initialMessage
            options["startTime"] = returnLog.startTime
            options["accountKey"] = returnLog.accountKey
            options["graphName"] = returnLog.graphName

        log = Log()
        if ("s" in options):
            log.sender = options["s"]
        else:
            log.sender = options["sender"]

        if ("r" in options):
            log.receiver = options["r"]
        else:
            log.receiver = options["receiver"]
        
        if ("message" in options):
            log.message = options["message"]

        if ("isError" in options):
            log.isError = (options["isError"] and True) or False

        if ("accountKey" in options):
            log.account = options["accountKey"]
        else:
            log.account = LlamaLogs.globalAccountKey or -1 

        if ("graphName" in options):
            log.graph = options["graphName"]
        else:
            log.graph = LlamaLogs.globalGraphName

        if ("initialMessage" in options):
            log.initialMessage = options["initialMessage"]

        if ("startTime" in options):
            log.elapsed = log.timestamp - options["startTime"]

        if (log.sender == "" or log.receiver == "" or log.graph == "" or log.account == ""):
            return None
        

        LogAggregator.add_log(log)
        return ReturnLog(log)