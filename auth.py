# import os
# import uuid
# import tempfile
# import pandas as pd
# from flask import Flask, request, jsonify, render_template, redirect, flash, session, Blueprint, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, login_required, current_user, logout_user
# from .app.commons.utils.whatsapp import send_whatsapp_msg
# from .models import LEADS, User
# from . import db

# auth = Blueprint('auth', __name__)

# @auth.route('/signup')
# def signup():
#     return render_template('auth/signup.html')

# @auth.route('/signup', methods=['POST'])
# def signup_post():
# 	# code to validate and add user to database goes here
# 	email = request.form.get('email')
# 	name = request.form.get('name')
# 	password = request.form.get('password')

# 	user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

# 	if user: # if a user is found, we want to redirect back to signup page so user can try again
# 		flash('Email address already exists')
# 		return redirect(url_for('auth.signup'))

# 	# create a new user with the form data. Hash the password so the plaintext version isn't saved.
# 	new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

# 	# add the new user to the database
# 	db.session.add(new_user)
# 	db.session.commit()

# 	return redirect(url_for('auth.login'))

# @auth.route('/login')
# def login():
#     return render_template('auth/login.html')

# @auth.route('/login', methods=['POST'])
# def login_post():
#     # login code goes here
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False

#     user = User.query.filter_by(email=email).first()

#     # check if the user actually exists
#     # take the user-supplied password, hash it, and compare it to the hashed password in the database
#     if not user or not check_password_hash(user.password, password):
#         flash('Please check your login details and try again.')
#         return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
#     login_user(user, remember=remember)
#     # if the above check passes, then we know the user has the right credentials
#     return redirect(url_for('main.function'))


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


# ####################################################################################################
# ####################################################################################################
# ############################################Dashboard###############################################
# ####################################################################################################
# ####################################################################################################
# ####################################################################################################

# # @auth.route("/dashboard", methods=["POST","GET"])
# # @login_required
# # def dashboard():
# # 	all_employees = EMPLOYEE_DATA.query.filter_by(company_id=current_user.id).all()
# # 	serialized_data = []
# # 	not_invited, user_not_initiated, user_in_progress, completed = 0, 0, 0, 0
# # 	for employee in all_employees:
# # 		if employee.status == "completed":
# # 			completed+=1
# # 		elif employee.status == "in_progress":
# # 			user_in_progress+=1
# # 		elif employee.status == "pending" and employee.invitation != "pending":
# # 			user_not_initiated+=1

# # 		if employee.invitation == "pending":
# # 			not_invited+=1
# # 		serialized_data.append([employee.name, employee.mobile_number, employee.email_id, employee.uan, employee.status, employee.employee_status, employee.invitation])

# # 	nav_dictionary = {	
# # 		"Not Invited": not_invited,
# # 		"User: Not Initiated": user_not_initiated,
# # 		"User: In Progress": user_in_progress,
# # 		"Completed": completed,
# # 		}

# # 	color_dict = {
# # 		'red': 'red',
# # 		'green': 'green',
# # 		'amber': 'orange',
# # 	}
# # 	return render_template('dashboard.html', value=serialized_data, dictionary=nav_dictionary, color_dict=color_dict, name=current_user.name)

