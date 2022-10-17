#import packages
from flask import *  # flask is a web framework of python
import mysql.connector
import uuid   # 128-bit label used for information in computer systems
import time
import enchant #spellcheck library
from better_profanity import profanity  # censor bad words
from nltk.tokenize import word_tokenize #natural language toolkit
dict = enchant.Dict("en_US")

app = Flask(__name__) #flask object
app.secret_key=uuid.uuid4().hex
# module
myconn = mysql.connector.connect(
  host="localhost",
  user="manthan",
  passwd="Manthan1234#",
  database="newfeedbackschema"
)

#first call "/"
@app.route("/",methods=['GET']) # GET = provide all info # POST = User need to provide parameters.
# app.route: mapping the URLs to a specific function that will handle the logic for that URL
def mainpage():
	return render_template("homepage.html") #generate output from a template file

# if student login button pressed
@app.route("/admin",methods=['GET','POST'])
def admin():
	if request.method=="POST":
		uname=request.form['uname'] #uname is the id/name set from admin.html
		pwd=request.form['pwd']
		#mysql call
		cur=myconn.cursor() #mysql instance to fetch data
		type = 'Student'
		# sql query execute
		cur.execute("select * from login where username=%s and userpasswd=%s and usertype=%s" ,(uname,pwd,type))
		# fetching all data from above query
		data=cur.fetchall()
		if data:
			session['loggedin']=True
			print(session)
			flash("Login successfully")

			cur = myconn.cursor()
			cur.execute("SELECT * FROM courseteacher")
			data = cur.fetchall()
			print(data)
			return render_template("feedback.html",uname=uname,data=data)#,uname=uname) #for student login
		else:
			flash("Invalid username or password")
			session['loggedin'] = False
			return render_template("admin.html")
	else:
		return render_template("admin.html")

# if teacher login button pressed
@app.route("/teacherAdmin",methods=['GET','POST'])
def admin1():
	if request.method=="POST":
		uname=request.form['uname']
		pwd=request.form['pwd']
		cur=myconn.cursor()
		type = 'Teacher'
		cur.execute("select * from login where username=%s and userpasswd=%s and usertype=%s" ,(uname,pwd,type))
		data=cur.fetchall()
		if data:
			cur.execute("select * ,((q1+q2+q3)/3) as score_avg from feedback_table where teachername=%s",(uname,))
			data1 = cur.fetchall()
			session['loggedin']=True
			flash("Login successfully")
			return render_template("viewnew.html",data = data1) #for teacher login
		else:
			flash("Invalid username or password")
			return render_template("adminteacher.html")
	else:
		return render_template("adminteacher.html")

@app.route("/feedback",methods=['GET','POST'])
def feedback():
	cur1 = myconn.cursor()
	cur1.execute("SELECT * FROM courseteacher")
	data = cur1.fetchall()

	if request.method == "POST":
		print(session['loggedin'])
		uname=request.form['uname']
		coursename=request.form['coursename']
		teachername=request.form['teachername']

		cur=myconn.cursor()
		cur.execute("Select * from courseteacher where coursename=%s and tearchername=%s",(coursename,teachername))
		records = cur.fetchall()
		print("records::",records)

		if records !=[]:
		# cur.execute("select * from students where rollno=%s and eventname=%s and courses=%s",(rollno,event_name,course))
		# records=cur.fetchall()
		# if records:
		# 	cur1 = myconn.cursor()
		#and coursename=%s
			print(coursename)
			cur.execute("select * from feedback_table where username=%s  and teachername=%s",(uname,teachername))
			data=cur.fetchall()
			print("data::",data)
			if len(data)==0:
				# flash("Feedback submitted successfully")
				# parameters passed for autofill
				return render_template("fbform.html",uname=uname,coursename=coursename,teachername=teachername)
			else:
				flash("You had already given the feedback")
				return render_template("feedback.html", uname=uname, data=data)
				
		else:
			flash("Wrong combination of Course and Teacher selected!!")
			return render_template("feedback.html",uname=uname,data=data)
	else:
		return render_template("feedback.html",data=data)

@app.route("/feedbackpage",methods=['GET','POST'])
def feedbackpage():
	if request.method=='POST':
		uname=request.form['uname']
		coursename=request.form['coursename']
		teachername=request.form['teachername']
		print(uname,coursename,teachername)

		secq=request.form['secq'] #first star rating
		thirdq=request.form['thirdq'] #second
		fourthq=request.form['fourthq'] #third
		comment=request.form['comment'] #text area
		cur=myconn.cursor()
		print(comment)
		# cur.execute("""insert into feedback_table(username,coursename,teachername,q1,q2,q3,comment)
		# 	values(%s,%s,%s,%s,%s,%s,%s)""",(uname,coursename,teachername,secq,thirdq,fourthq,comment))
		# myconn.commit()
		
		#profanity-check
		# custom_badwords = ['abusive']
		# profanity.add_censor_words(custom_badwords)
		path = "C:\\Users\\user\\Desktop\\hello_MANTHAN\\hello_MANTHAN\\Feedback-system-project-master\\Feedback-system-project-master\\pyproject\\"

		filename = path+'profanity_wordlist.txt'
		# profanity check..
		profanity.load_censor_words_from_file(filename) # inbuilt function in profanity module.
		
		# censored_text = profanity.censor(comment)
		censored_text_check = profanity.contains_profanity(comment)
		# print(censored_text, censored_text_check)
		
		#misspelled words
		words = word_tokenize(comment) #nltk library
		misspelled = []
		for word in words:
			if dict.check(word) == False:
				misspelled.append(word)
		# print("The misspelled words are : " + str(misspelled))
		# for word in misspelled:
		# 	print("Suggestion for " + word + " : " + str(dict.suggest(word)))
			
		if censored_text_check == True:
			flash("ALERTT... Bad language found. Please correct before sending your feedback!")
			return render_template("fbform.html", uname=uname, coursename=coursename, teachername=teachername,)
		else:
			if misspelled == []:
				cur.execute("""insert into feedback_table(username,coursename,teachername,q1,q2,q3,comment)
									values(%s,%s,%s,%s,%s,%s,%s)""",
				            (uname, coursename, teachername, secq, thirdq, fourthq, comment))
				myconn.commit()
				flash("Feedback submitted successfully!")
				return render_template("admin.html")
			else:
				flash("Misspelled words found are.."+str(misspelled)+". Please correct before sending your feedback!")
			# return redirect(url_for('feedback'))
				return render_template("fbform.html",uname=uname,coursename=coursename,teachername=teachername)

# @app.route("/viewfeedback",methods=['GET','POST'])
# def viewfeedback():
# 	if request.method=='POST':
# 		course=request.form['course']
# 		cur=myconn.cursor()
# 		cur.execute("SELECT q1,q2,q3  FROM `feedback_table` where course=%s",(course,))
# 		percentage=cur.fetchall()
# 		percentage = (((int(percentage[0][0]) + int(percentage[0][1]) + int(percentage[0][2])) * 100) / 15)
# 		# percentage=int(percentage[0][0])
# 		cur.execute("SELECT DISTINCT course FROM `feedback_table`")
# 		data=cur.fetchall()
# 		return render_template("viewfeedback.html",data=data,percentage=percentage,course=course)
# 	else:
# 		cur=myconn.cursor()
# 		cur.execute("SELECT DISTINCT course FROM feedback_table")
# 		data=cur.fetchall()
# 		return render_template("viewfeedback.html",data=data)


@app.route("/logout")
def logout():
	session['loggedin']=False
	flash("You are successfully logged out.")
	return render_template("homepage.html")

@app.route("/logoutTeacher")
def logoutTeacher():
	session['loggedin']=False
	# flash("You are successfully logged out.")
	return render_template("adminteacher.html")


#starter of the application
if __name__=="__main__":
	app.run(host="localhost",port=8009) #run Flask object
	app.run(debug = True)
	# app.run()
	# app.run(debug=True)
