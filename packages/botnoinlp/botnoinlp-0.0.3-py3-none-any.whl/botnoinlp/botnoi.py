import requests
class BotNoi:
	def __init__(self,message,token):
        self.token = token
    def chitchat(self,message,styleid,botname):
    	url = "https://openapi.botnoi.ai/service-api/botnoichitchat?keyword=test&styleid=test&botname=test"
		headers = {
    		'Authorization': 'Bearer %s'self.token
		}
		response = requests.request("GET", url, headers=headers).json()
		return response


