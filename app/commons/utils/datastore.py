from google.cloud import datastore
from google.cloud.exceptions import ServiceUnavailable
import uuid
import json
import os

datastore_client = datastore.Client(project=os.getenv("DATASTORE_PROJECT"))

def save_info(details):
	key = datastore_client.key(os.getenv("DATASTORE_RESPONSE_KIND"), str(uuid.uuid4()))
	entity = datastore.Entity(key=key)
	entity.update(json.loads(json.dumps(details)))
    
	try:
		datastore_client.put(entity)
	except ServiceUnavailable:
		return
