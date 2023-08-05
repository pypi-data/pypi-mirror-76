import schedule
import time
import json
import threading
import sys

from llamalogs.llamaProxy import LlamaProxy
from llamalogs.aggregateLog import AggregateLog

class LogAggregator:
	#lock for the aggregate log/stat maps
	lock = threading.Lock()
	aggregateLogs = {}
	aggregateStats = {}

	@staticmethod
	def start_timer():
		# sending messages after 5 seconds upon startup, then to a 1 min interval
		time.sleep(5)
		LogAggregator.send_messages()

		delay = 59.5
		schedule.every(delay).seconds.do(LogAggregator.send_messages)
		while True and len(schedule.jobs) > 0:
			schedule.run_pending()
			time.sleep(delay)

	@staticmethod
	def send_messages():
		if (LlamaProxy.isDevEnv):
			print("Sent Messages")
		log_list, stat_list = LogAggregator.gather_messages()
		LlamaProxy.send_messages(log_list, stat_list)

	@staticmethod
	def gather_messages():
		with LogAggregator.lock:
			currentLogs = LogAggregator.aggregateLogs
			LogAggregator.aggregateLogs = {}
			currentStats = LogAggregator.aggregateStats
			LogAggregator.aggregateStats = {}

		log_list = []
		stat_list = []
		for sender in currentLogs:
			for receiver in currentLogs[sender]:
				log_list.append(currentLogs[sender][receiver].toAPIFormat())
				
		for component in currentStats:
			for name in currentStats[component]:
				stat_list.append(currentStats[component][name].toAPIFormat())
		
		return log_list, stat_list

	@staticmethod
	def add_log(log):
		with LogAggregator.lock:
			if (log.sender not in LogAggregator.aggregateLogs):
				LogAggregator.aggregateLogs[log.sender] = {}
			if (log.receiver not in LogAggregator.aggregateLogs[log.sender]):
				LogAggregator.aggregateLogs[log.sender][log.receiver] = AggregateLog(log)

			working_ob = LogAggregator.aggregateLogs[log.sender][log.receiver]

			if (log.isError):
				working_ob.errors = working_ob.errors + 1
			if (log.elapsed):
				prev_amount = working_ob.elapsed * working_ob.elapsedCount
				working_ob.elapsed = (prev_amount + log.elapsed) / (working_ob.total + 1)
				working_ob.elapsedCount = working_ob.elapsedCount + 1
			if (log.initialMessage):
				working_ob.initialMessageCount = working_ob.initialMessageCount + 1

			working_ob.total = working_ob.total + 1
			if (working_ob.message == '' and log.isError == False):
				working_ob.message = str(log.message or '')
			if (working_ob.errorMessage == '' and log.isError == True):
				working_ob.errorMessage = str(log.message or '')
		if (LlamaProxy.isDevEnv):
			print("adding log")
			print(LogAggregator.aggregateLogs)

	@staticmethod
	def add_stat(stat):
		with LogAggregator.lock:
			if (stat.type == "point"):
				if (stat.component not in LogAggregator.aggregateStats):
					LogAggregator.aggregateStats[stat.component] = {}
				LogAggregator.aggregateStats[stat.component][stat.name] = stat    

			if (stat.type == "average"):
				LogAggregator.add_stat_avg(stat)
			if (stat.type == "max"):
				LogAggregator.add_stat_max(stat)

	@staticmethod
	def add_stat_avg(stat):
		if (stat.component not in LogAggregator.aggregateStats):
			LogAggregator.aggregateStats[stat.component] = {}
		if (stat.name not in LogAggregator.aggregateStats[stat.component]):
			LogAggregator.aggregateStats[stat.component][stat.name] = stat
			stat.count = 0

		existing = LogAggregator.aggregateStats[stat.component][stat.name]
		existing.value = existing.value + stat.value
		existing.count = existing.count + 1
	
	@staticmethod
	def add_stat_max(stat):
		if (stat.component not in LogAggregator.aggregateStats):
			LogAggregator.aggregateStats[stat.component] = {}
		if (stat.name not in LogAggregator.aggregateStats[stat.component]):
			LogAggregator.aggregateStats[stat.component][stat.name] = stat

		existing = LogAggregator.aggregateStats[stat.component][stat.name]
		if (stat.value > existing.value):
			existing.value = stat.value
