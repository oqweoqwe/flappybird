import json
from os.path import exists, getsize
from os import mkdir

class DataFile:

	def __init__(self):
		self.path = "./data/data.txt"
		if not exists("./data/"):
			print("data dir not found, attempting to create it")
			try:
				mkdir("data")
			except:
				print("mkdir error")
		if not exists(self.path):
			with open(self.path, "w") as f:
				json.dump({"high_score": 0}, f)

	def get_high_score(self):
		with open(self.path, "r+") as f:
			if getsize(self.path) > 0:
				return json.load(f).get("high_score", 0)
			else :
				print("file empty, putting default value")
				json.dump({"high_score": 0}, f)
				return 0

	def set_high_score(self, high_score):
		with open(self.path, "r+") as f:
			
			if getsize(self.path) > 0:
				data = json.load(f)
				data["high_score"] = high_score
				f.seek(0)
				json.dump(data, f)
				f.truncate()
			else :
				print("file empty, putting high score")
				json.dump({"high_score": high_score}, f)