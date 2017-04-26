#-*- coding: utf-8 -*-
from flask import render_template, flash, redirect, request, Response,send_file
from flask import Flask, session, url_for, escape
from app import app
import json
from . import function
import os
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# app.secret_key = os.urandom(24)

UPLOAD_FOLDER = os.getcwd()

# index view function suppressed for brevity
@app.route('/')
@app.route('/index')
def index():
	if 'email' in session:

		return render_template("search.html",
                        title='Welcome',
						session=session['email']
						)

	return render_template("search.html",
                        title='Welcome',
						session=None)

@app.route('/search_results', methods=['GET', 'POST'])
def results():

	if request.method == 'POST':
	    Email= request.form.get("email")
	    PW = request.form.get("password")
	    result1 = function.Check_email(Email)
	    result2 = function.Check_pw(Email, PW)
	    if result1 ==[]:
	        error = 'Invalid username'
	    elif result2 ==[]:
	        error = 'Invalid password'
	    else:
	        session['email'] = Email
	        return redirect('/')

	    return render_template("search_results.html",
	                        title='results'
	                        )


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'email' in session:
		return redirect('/')
	else:
	    error=None
	    if request.method == 'POST':
	        Email= request.form.get("email")
	        PW = request.form.get("password")
	        result1 = function.Check_email(Email)
	        result2 = function.Check_pw(Email, PW)
	        if result1 ==[]:
	            error = 'Invalid username'
	        elif result2 ==[]:
	            error = 'Invalid password'
	        else:
	            session['email'] = Email
	            return redirect('/')

	    return render_template("login.html",
	                        title='Sign In',
	                        error=error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	# ImmutableMultiDict([('user[last_name]', 'yoo'),
	# 					('user[password]', '1q2w3e4r'),
	# 					('user[birthday_month]', '1'),
	# 					('user[birthday_day]', '4'),
	# 					('user[birthday_year]', '2011'),
	# 					('utf8', '✓'),
	# 					('from', 'email_signup'),
	# 					('user[first_name]', 'dongwon'),
	# 					('user[email]', 'asldkfj@nave.rcom'),
	# 					('user_profile_info[receive_promotional_email]', '0'),
	# 					('user_profile_info[receive_promotional_email]', '1'),
	# 					('authenticity_token', '#j')])

	if request.method == 'POST':
		Email= request.form.get("user[email]")
		PW = request.form.get("user[password]")
		result = function.Save_mem(Email, PW)
		if result == 1:
			session['email'] = Email
			return redirect('/')
		else:
			error = 'Email already exists.'
			return render_template("signup.html",
								title='SignUp',
								error=error)
	else:
		return render_template("signup.html",
							title='SignUp',
							error=None)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    return redirect('/')


@app.route('/enrollment_home/address', methods=['GET', 'POST'])
def enrollment_home_address():
	# Check session
    if not 'email' in session:
        return redirect('/')
    User = session['email']
    citycode = function.Check_citycode(User)


	# 등록 수정을 원하는 경우 고려해야함

    # if citycode[0][0] != '0':
        # return "already enroll home!"


    if request.method == 'POST':
        print(request.form)
		# ImmutableMultiDict([('country_code', 'US'),
		# 					('city', '1'),
		# 					('street', '1'),
		# 					('zipcode', '1'),
		# 					('apt', '1'),
		# 					('state', '1')])
        state = request.form.get("state")
        city = request.form.get("city")
        street = request.form.get("street")
        apt = request.form.get("apt")
        zipcode = request.form.get("zipcode")
        function.Save_home_address(User, state, city, street, apt, zipcode)
        citycode = zipcode[0:3]
        function.Update_Citycode(User, citycode)
        return redirect('/enrollment_home/room')

	# if citycode[0][0] != '0':
        # city =
    return render_template("address.html",
                        title='progress',
						session='OK',
						city='')


@app.route('/enrollment_home/room', methods=['GET', 'POST'])
def enrollment_home_room():
	# Check session
	if not 'email' in session:
		return redirect('/')


	if request.method == 'POST':
		User = session['email']
		print(request.form)
		# ImmutableMultiDict([('house_type', '2'),
		# 					('number_of_room', '1')])

		house_type = request.form.get("house_type")
		if house_type == '1':
			house_type = 'A'
		elif house_type == '2':
			house_type = 'P'
		room = request.form.get("number_of_room")
		function.Save_home_room(User, house_type, room)
		return redirect('/enrollment_home/car_elevator')

	return render_template("room.html",
                        title='progress',
						session='OK')

@app.route('/enrollment_home/car_elevator', methods=['GET', 'POST'])
def enrollment_home_car_elevator():
	# Check session
	if not 'email' in session:
		return redirect('/')


	if request.method == 'POST':
		User = session['email']
		print(request.form)
		# ImmutableMultiDict([('elevatorType', 'yes'),
		# 					('parkingType', 'neo')])
		print(User)
		elevator = house_type = request.form.get("elevatorType")
		parking = house_type = request.form.get("parkingType")
		function.Save_home_car_elevator(User, elevator, parking)
		return redirect('/rooms')


	return render_template("car_elevator.html",
                        title='progress',
						session='OK')

@app.route('/enrollment_home/complete', methods=['GET', 'POST'])
def enrollment_home_complete():
	# Check session
	if not 'email' in session:
		return redirect('/')


	if request.method == 'POST':
		print(request.form)
		# ImmutableMultiDict([('elevatorType', 'yes'),
		# 					('parkingType', 'no')])
		return redirect('/')

	return render_template("enrollment_home_complete.html",
                        title='progress',
						session='OK')

@app.route('/enrollment_pet/pet', methods=['GET', 'POST'])
def enrollment_pet_pet():
    # Check session
	if not 'email' in session:
		return redirect('/')

	# User = session['email']
    # citycode = function.Check_citycode(User)
	# if citycode[0][0] != '0':
    #     return "already enroll home!"


	if request.method == 'POST':
		print(request.form)

		# ImmutableMultiDict([('petName', 'mong'),
		# 					('petGender', 'male'),
		# 					('pet[birthday_month]', '1'),
		# 					('pet[birthday_day]', '10'),
		# 					('pet[birthday_year]', '2016')])

		User = session['email']

		petname = request.form.get("petName")
		petgender = request.form.get("petGender")
		month = request.form.get("pet[birthday_month]")
		day = request.form.get("pet[birthday_day]")
		year = request.form.get("pet[birthday_year]")

		petbirth = year+"-"+month+"-"+day
		function.Save_pet_pet(User, petname, petgender,petbirth)

		return redirect('/enrollment_pet/size')

	return render_template("pet.html",
                        title='pet',
						session='OK')

@app.route('/enrollment_pet/size', methods=['GET', 'POST'])
def enrollment_pet_size():

	if not 'email' in session:
		return redirect('/')



	if request.method == 'POST':
		print(request.form)

		# ImmutableMultiDict([('pet-breed', '1'),
		# 					('pet-size', '3')])

		User = session['email']

		breed = request.form.get("breed")
		size = request.form.get("size")
		function.Save_pet_size(User, breed, size)

		return redirect('/enrollment_pet/vac')

	return render_template("pet_size.html",
                        title='pet',
						session='OK')

@app.route('/enrollment_pet/vac', methods=['GET', 'POST'])
def enrollment_pet_vac():

	if not 'email' in session:
		return redirect('/')

	if request.method == 'POST':
		print(request.form)

		# ImmutableMultiDict([('ns', '1'),
		# 					('vac', '2')])
		User = session['email']
		ns = request.form.get("ns")
		vac = request.form.get("vac")
		function.Save_pet_vac(User, ns, vac)
		function.Increase_npet(User)

		return redirect('/pets')

	return render_template("pet_vac.html",
                        title='pet',
						session='OK')

@app.route('/enrollment_pet/complete', methods=['GET', 'POST'])
def enrollment_pet_complete():
	# Check session
	if not 'email' in session:
		return redirect('/')


	if request.method == 'POST':
		print(request.form)
		# ImmutableMultiDict([('elevatorType', 'yes'),
		# 					('parkingType', 'no')])
		return redirect('/')

	return render_template("enrollment_pet_complete.html",
                        title='progress',
						session='OK')

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():

	if not 'email' in session:
		return redirect('/')

	if request.method == 'POST':
		print(request.form)

	User = session['email']
	check_room = function.Check_citycode(User)
	if(check_room):
		room = function.Read_house(User)
	else:
		room = ''

	return render_template("user_rooms.html",
                        title='MyProfile/rooms',
						session='OK', rooms = room)

@app.route('/pets', methods=['GET', 'POST'])
def pets():

	if not 'email' in session:
		return redirect('/')

	if request.method == 'POST':
		print(request.form)

	User = session['email']
	check_pet = function.Check_npet(User)
	if check_pet[0][0]=='1':
		pet = function.Read_pet(User)
		# if pet[0][6] == '1':
		# 	pet[0][6] == "Small"
		# elif pet[0][6] == '2':
		# 	pet[0][6] == "Medium"
		# else:
		# 	pet[0][6] == "Large"
	else:
		pet = ''

	return render_template("user_pets.html",
                        title='MyProfile/pets',
						session='OK', pets=pet)

@app.route('/users/edit', methods=['GET', 'POST'])
def users_edit():

	if not 'email' in session:
		return redirect('/')

	if request.method == 'POST':
		print(request.form)


	return render_template("user_edit.html",
                        title='MyProfile/edit',
						session='OK')

# https://www.slideshare.net/arload/flask-restful-api
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        imgName = request.form['imgName']
        file = request.files['uploadedfile']
        path = UPLOAD_FOLDER + file.filename;
        if file and allowed_file(file.filename):
            file.save(path)
            return "ok";
    return "error";

@app.route('/image/<fileName>', methods=['POST', 'GET'])
def loadImage(fileName):
    return send_file(UPLOAD_FOLDER+"/"+fileName, mimetype='image');

@app.route('/test', methods=['GET', 'POST'])
def test():
	User = session['email']
	function.Save_image(User, 'houst', '/home/soyoung/team/real/petsit_flask_UI/sky')


	if not 'email' in session:
		return redirect('/')

	if request.method == 'POST':
		print(request.form)

	User = session['email']
	info = function.Read_member(User)
	# http://snacky.tistory.com/6
	#
	return render_template("test_get_rooms.html",
                        title='MyProfile/rooms',
						session='OK', rooms = info)

	# if not 'email' in session:
	# 	return redirect('/')
	#
	# # if request.method == 'GET':
	# 	# print(request.form)
	# data = function.Read_member()
	# print(data)

	# return render_template("test_get_rooms.html",
    #                     title='progress',
	# 					session='OK',
	# 					rooms = data)
