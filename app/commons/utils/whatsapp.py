import os
import json
import requests

def send_whatsapp_msg(number, url, name, remind=False, company_name="IDfy"):
  
	# defining the api-endpoint 
	api_endpoint = os.getenv("KALEYRA_WA_URL")
  
	# your API key here
	api_key = os.getenv("KALEYRA_API_KEY")
	from_number = os.getenv("FROM_NUMBER")

	if remind:
		template_name = os.getenv("MSG_TEMPLATE_NAME_REMIND")
		toll_free_num = os.getenv("TOLL_FREE_NUM")
		msg = r'"{}","{}","{}"'.format(name, url, toll_free_num)
	else:
		template_name = os.getenv("MSG_TEMPLATE_NAME_INVITE")
		msg = r'"{}","{}","{}"'.format(name, company_name, url)

	headers = {"Content-Type": "application/json", "api-key": api_key}
	
	# data to be sent to api
	data = {
			"to": number,
	        "from": from_number,
	        "type": "mediatemplate",
	        "template_name": template_name,
	        "params": msg,
	        "lang_code": "en",
	        "channel":"whatsapp",
	    }
  
	# sending post request and saving response as response object
	r = requests.post(url=api_endpoint, headers=headers, data=json.dumps(data))
  	
	print(json.dumps(data))
	print(r.json())
	if "20" in str(r.status_code):
		return "success", None
	else:
		return "failure", "something"
