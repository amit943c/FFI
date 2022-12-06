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

main = Flask(__name__)


def image_upload(request):
	path_prefix = os.getenv("PATH_PREFIX_CAMERA_IMG")
	start_time = time.time()
	object_name = ""
	image = request.files.get('image')
	print(request.files)
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

@main.route("/search_celeb", methods=["POST"])
# @login_required
def search_celeb():
	try:
		init_time = time.time()
		object_name, path_prefix = image_upload(request)
		resize_image(object_name, path_prefix)

		name = request.form.get('name', "")
		mobile = request.form.get('mobile', "NA")
		email_id = request.form.get('email', "NA")

		is_student = request.form.get('is_student', "NA")

		name_of_institute = request.form.get('name_of_institute', "NA")
		year_of_education = request.form.get('year_of_education', "NA")

		company = request.form.get('name_of_company', "NA")
		designation = request.form.get('designation', "NA")

		looking_for_opportunities = request.form.get('looking_for_opportunities', "NA")

		input_person = {
			'face_image': "camera/" + object_name,
			'name': name,
		}
		gender = request.form.get('gender')
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
		print("[visitor_details] Name: {}, Mobile: {}, Email: {}, Company: {}".format(name, mobile, email_id, company))

		# new_session = LEADS(name=name, mobile_number=mobile, email_id=email_id, company=company)
		# db.session.add(new_session)
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
		}
		start_time = time.time()
		save_info(details)
		print("datastore time", time.time()-start_time)
		print("total time", time.time()-init_time)
	except:
		return render_template('error.html')		

	return render_template('faces.html', celeb=celeb, input_person=input_person, congrats_text=congrats_text)

# if __name__ == '__main__':
# 	main.run()
