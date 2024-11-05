from flask import Flask, render_template, request, session, redirect, url_for
from pandas import read_json
from flask_session import Session
from pandas import read_json
from sklearn.metrics import f1_score, accuracy_score
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import time, ctime
import smtplib
import tempfile

# Constants
DATA_PATH = 'data.json'
LABEL = {'Real': 1, 'Fake': 0}
SENDER_EMAIL = "bot.fake.news@gmail.com"
SENDER_PASSWORD = "yuvpgvblrhadplhq "  # App-specific password
RECEIVER_EMAIL = "prosso@dsic.upv.es"

app = Flask(__name__)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
app.secret_key = 'f4k3nh4t3'  # For session management, update this key
Session(app)
data = read_json(DATA_PATH)

def sample_data(data, task):
    MAX = 50 if task == 'hate speech' else 20
    subset = data[data['task'] == task].sample(MAX)
    idxs = subset.index.tolist()
    labels = [LABEL[l] for l in data['label'][idxs]] if task == 'fake news' else data['HS'][idxs].tolist()
    return idxs, labels


def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Sends an email report.
    """
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    try:
        input_request = request.get_json()
        task = input_request['button']
        print(task)
        password = input_request['password']
        print(password)
        #texts, headlines, labels = read_data(DATA_PATH, task)
        idxs, labels = sample_data(data, task)
        
        # Store data in server-side session
        session['texts'] = idxs
        session['labels'] = labels
        session['results'] = [0] * len(idxs)
        session['curr_t'] = 0
        session['task'] = task
    except:
        print('Error')
    
    return redirect(url_for('classify'))


@app.route('/classify')
def classify():
    # Add session validation
    if 'curr_t' not in session:
        return redirect(url_for('index'))
    
    curr_t = session['curr_t']
    if curr_t >= len(session['texts']):
        return redirect(url_for('report'))
    
    text = data['text'][session['texts'][curr_t]]
    headline = data['title'][session['texts'][curr_t]] if session['task'] == 'fake news' else ''
    task = session['task']
    
    if task == 'fake news':
        return render_template('classify.html', text=text, headline=headline, button1='Real', button2='Fake',current=curr_t+1,max=len(session['texts']))
    else:
        return render_template('classify.html', text=text, headline=headline, button1='Hate Speech', button2='Non Hate Speech',current=curr_t+1,max=len(session['texts']))


@app.route('/submit_classification', methods=['POST'])
def submit_classification():
    if 'curr_t' not in session:
        return redirect(url_for('index'))
        
    classification = request.form.get('classification')
    if classification:
        session['results'][session['curr_t']] = int(classification)
        session['curr_t'] += 1
        # Explicitly save the session after modification
        session.modified = True
    return redirect(url_for('classify'))


@app.route('/report')
def report():
    if 'results' not in session:
        return redirect(url_for('index'))
        
    results = session['results']
    labels = session['labels']
    task = session['task']
    
    f1 = f1_score(labels, results)
    acc = accuracy_score(labels, results)
    return render_template('report.html', f1_score=f"{f1:.2%}", accuracy=f"{acc:.2%}", task=task)


@app.route('/send_report', methods=['POST'])
def send_report():
    if 'results' not in session:
        return redirect(url_for('index'))
        
    user_name = request.form.get('user_name')
    task = session['task']
    results = session['results']
    labels = session['labels']
    
    f1 = f1_score(labels, results)
    acc = accuracy_score(labels, results)
    
    subject = f"{task.capitalize()} Classification Report: {user_name}"
    body = f"Report of {user_name}:\nF1 Score: {f1:.2%}\nAccuracy: {acc:.2%}"
    
    send_email(SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL, subject, body)   
    #return render_template('report.html', f1_score=f"{f1:.2%}", accuracy=f"{acc:.2%}", task=task, message=message)
    hora = ctime(time())
    with open('log.csv','a') as log:
        log.write(f'{user_name},{task},{hora},{f1:.2%},{acc:.2%}\n')
    #return render_template('index.html')
    return redirect(url_for('index'))

# Redirect all HTTP traffic to HTTPS
# @app.before_request
# def before_request():
#     if not request.is_secure and app.env != 'development':
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)


if __name__ == '__main__':
    app.run(debug=True) # For local development
    #app.run(host='0.0.0.0', port=80, debug = False) # For deployment