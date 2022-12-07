from google.cloud import datastore
from google.cloud.exceptions import ServiceUnavailable
import uuid
import json
import os
import redis
import time

datastore_client = datastore.Client(project=os.getenv("DATASTORE_PROJECT"))

def save_info(details):
	key = datastore_client.key(os.getenv("DATASTORE_RESPONSE_KIND"), str(uuid.uuid4()))
	entity = datastore.Entity(key=key)
	entity.update(json.loads(json.dumps(details)))
	
	try:
		datastore_client.put(entity)
	except ServiceUnavailable:
		return

def save_result_to_redis(details):

	redis_pool = None

	# global redis_pool
	print("PID %d: initializing redis pool..." % os.getpid())
	redis_pool = redis.ConnectionPool(host='redis-18294.c1.us-west-2-2.ec2.cloud.redislabs.com', port=18294, db=0, health_check_interval=10)
	print("redis connection_pool is created")

	start_time = time.time()
	redis_res_json = json.dumps(details)

	try:
		redis_connection = redis.Redis(connection_pool=redis_pool)
		redis_connection.set(str(uuid.uuid4()), redis_res_json)	
	except redis.exceptions.ConnectionError as e:
		print(e)
	except redis.exceptions.RedisError as e:
		print(e)
	except Exception as e:
		print(e)
	print("redis time:", time.time()-start_time)
	return