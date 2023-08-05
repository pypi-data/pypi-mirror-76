import requests

class LlamaProxy:
	isDevEnv = False

	@staticmethod
	def send_messages(currentLogs, currentStats):
		LlamaProxy.send_data(currentLogs, currentStats)

	@staticmethod
	def send_data(log_list, stat_list):
		url = 'https://llamalogs.com/'
		if (LlamaProxy.isDevEnv):
			url = 'http://localhost:4000/'

		if (LlamaProxy.isDevEnv):
			print("data_lists")
			print(log_list)
			print(stat_list)	

		if (len(log_list) or len(stat_list)):
			try:
				first_log = (len(log_list) and log_list[0]) or (len(stat_list) and stat_list[0])
				account_key = first_log["account"]
				# connect and receive timouts
				requests.post(url + 'api/v0/timedata', json = {"account_key": account_key, "time_logs": log_list, "time_stats": stat_list}, timeout=(2, 5))
			except:
				print('LlamaLogs Error; error sending data to llama logs server')	