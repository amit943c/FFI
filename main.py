import re
import os
import json
import time
import traceback
import uuid
from flask import Flask, request, jsonify, render_template, redirect, flash, session, Blueprint
from app.commons.utils.aws import *
from flask_login import login_required, current_user
from app.commons.utils.datastore import *
from multiprocessing.pool import ThreadPool

main = Flask(__name__)


def image_upload(image):
	path_prefix = os.getenv("PATH_PREFIX_CAMERA_IMG")
	start_time = time.time()
	object_name = ""
	# image = req.files.get('image')
	# print(req.files)
	start_time_2 = time.time()
	print("First Time: ", start_time_2 - start_time)
	if image.name != '':
		uuid_img_path = uuid.uuid4()

		try:
			object_name = str(uuid_img_path) + ".jpg"
			file_path = path_prefix + object_name
			image.save(file_path)
			start_time_3 = time.time()
			print("Time in saving: ", start_time_3 - start_time_2)
		except Exception as e:
			object_name = str(uuid_img_path) + ".png"
			file_path = path_prefix + object_name
			image.save(file_path)
		start_time_4 = time.time()
		print("Time in uploading: ", start_time_4 - start_time_3)
	return object_name, path_prefix

@main.route("/", methods=["GET"])
# @login_required
def initiate():
	return render_template('first.html')

@main.route("/capture", methods=["GET"])
# @login_required
def capture():
	return render_template('second.html')

@main.route("/_health", methods=["GET"])
def _health():
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

@main.route("/search_celeb", methods=["POST"])
# @login_required
def search_celeb():
	start_time = time.time()
	req = request
	name = req.form.get('name', "")
	mobile = req.form.get('mobile', "NA")
	email_id = req.form.get('email', "NA")
	is_student = req.form.get('is_student', "NA")
	name_of_institute = req.form.get('name_of_institute', "NA")
	year_of_education = req.form.get('year_of_education', "NA")
	company = req.form.get('name_of_company', "NA")
	designation = req.form.get('designation', "NA")
	looking_for_opportunities = req.form.get('looking_for_opportunities', "NA")
	gender = req.form.get('gender')
	details = {
		'name': name,
		'mobile_number': mobile,
		'email_id': email_id,
		'student': is_student,
		'name_of_institute': name_of_institute,
		'year_of_education': year_of_education,
		'name_of_company': company,
		'designation': designation,
		'looking_for_opportunities': looking_for_opportunities,
		'gender': gender,
	}
	try:
		start_time = time.time()
		pool = ThreadPool(processes=2)
		async_result_datastore = pool.apply_async(save_result_to_redis, (details,))
		image = req.files.get('image')
		async_result_celeb = pool.apply_async(search_face_db, (details, image,))
		(celeb, input_person, congrats_text) = async_result_celeb.get()
		is_stored = async_result_datastore.get()
		print("Total time: ", time.time()-start_time)
	except Exception as e:
		print(e)
		return render_template('error.html')		

	return render_template('faces.html', celeb=celeb, input_person=input_person, congrats_text=congrats_text)


def save_to_datastore(details):
	start_time = time.time()
	save_info(details)
	print("datastore time", time.time()-start_time)
	return True

def search_face_db(details, image):
	init_time = time.time()
	object_name, path_prefix = image_upload(image)
	resize_image(object_name, path_prefix)

	name = details.get('name', "")

	input_person = {
		'face_image': "camera/" + object_name,
		'name': name,
	}
	gender = details.get('gender')
	if gender.lower() == "female":
		collection_id = "celeb_female_ffi"
	elif gender.lower() == "male":
		collection_id = "celeb_male_ffi" 
	else:
		collection_id = "celeb_female_ffi" 

	res = search_face(object_name, threshold=0, max_faces=1, collection_id=collection_id)
	celeb = {}
	if len(res) > 0:
		celeb = res[0]

	similarity = float(celeb.get('similarity', "0"))
	celeb_object_name = celeb.get("face_image", "")

	try:
		celeb_object_name =  celeb_object_name.split("/")[-1]
		celeb_name = " ".join(celeb_object_name.split(".")[0].split("_")).title()
	except:
		celeb_name = ""

	celeb['name'] = celeb_name

	# if similarity > 59.99:
	# 	congrats_text = "You have a celebrity lookalike!"
	# elif similarity > 29.99:
	# 	congrats_text = "You somewhat look like somebody famous!"
	# else:
	# 	congrats_text = "No match. Maybe you are the Celeb!"

	congrats_text = "Yay! You are closest to…"
	print("similarity : ", similarity)
	print("[visitor_details] Name: {}, Mobile: {}, Email: {}".format(name, details.get('mobile_number'), details.get('email_id')))
	return (celeb, input_person, congrats_text)

# def mainthread(request):
#     res = await asyncio.gather(*[save_to_datastore(request), search_face_db(request)])
#     return res

# if __name__ == '__main__':
# 	main.run()
