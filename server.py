from flask import Flask, render_template , url_for, request, redirect
import csv
import smtplib
from email.message import EmailMessage





app = Flask(__name__)





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{name},{email},{subject},{message}')

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2,delimiter=',', quotechar='"', quoting =csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,subject,message])

def email_to_client(user_name,user_email,user_subject,user_message):
    email = EmailMessage()
    email['from'] = 'mizzi19'
    email['to'] = (user_email)
    email['subject'] = 'Confirmation email'

    email.set_content(f' Dear {user_name}, \n  we have received your message re-{user_subject} \n\n  Message: \n{user_message} \n\n We will be contacting you as soon as possible')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('19m1221@gmail.com','XXXXXX')
        smtp.send_message(email)

def email_to_server(user_name,user_email,user_subject,user_message):
    email = EmailMessage()
    email['from'] = 'mizzi19'
    email['to'] = 'sandro.mizz@gmail.com'
    email['subject'] = 'Contact form mizzi19 site'

    email.set_content(f' Message received from \n name:{user_name} \n email:{user_email} \n subject:{user_subject} \n message:{user_message} \n\n End of message')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('19m1221@gmail.com','XXXXXX')
        smtp.send_message(email)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            email_to_client(data["name"],data["email"],data["subject"],data["message"])
            email_to_server(data["name"], data["email"], data["subject"], data["message"])
            return redirect('/thankyou.html')
        except:
            return 'didnot save to database'
    else:
        return 'Something went wrong try again'



