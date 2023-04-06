from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import csv,os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
SECRET_KEY = os.getenv("MY_SECRET")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'lakshaysh93@gmail.com' # Replace with your email
app.config['MAIL_PASSWORD'] = SECRET_KEY # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'Portfolio Form' # Replace with your email

mail = Mail(app)

print(__name__)

@app.route("/")
def my_home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
    with open('database.csv', mode='a', newline='')as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
            data = request.form.to_dict()
            email1 = data["email"]
            subject1 = data["subject"]
            message1 = data["message"]
            write_to_csv(data)
            msg = Message(subject='Recruiter contact Request', recipients=['lakshaysh93@gmail.com']) # Replace with your email
            msg.body = f'Email: {email1}\nSubject: {subject1}\nMessage: {message1}'
            mail.send(msg)
            return redirect('/thankyou.html')
    else: 
        return "Something went Wrong ! Try again"