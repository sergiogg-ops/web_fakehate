from flask import Flask, render_template, request, session, redirect, url_for
from pandas import read_json, concat, DataFrame
from flask_session import Session
from sklearn.metrics import f1_score, accuracy_score
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import time, ctime
import smtplib
import tempfile

# Constants
DATA_PATH = 'data.json'
SENDER_EMAIL = "bot.fake.news@gmail.com"
SENDER_PASSWORD = "yuvpgvblrhadplhq "  # App-specific password
RECEIVER_EMAIL = "prosso@dsic.upv.es"
PASSWORDS = ['fsu']
#LABEL = {'Real': 1, 'Fake': 0}
LABEL = {
    'fake news': ['Fake', 'Real'],
    'hate speech': ['Hate Speech', 'Non Hate Speech'],
    'stereotype': ['Stereotypical', 'Non Stereotypical'],
    'irony': ['Ironic', 'Non Ironic'],
    'sexism': ['Sexist', 'Non Sexist'],
    'conspiracy': ['Conspiracy', 'Mainstream'],
    'oppositional thinking': ['Conspiracy', 'Critical']
}

app = Flask(__name__)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
app.secret_key = 'f4k3nh4t3'  # For session management, update this key
Session(app)
data = read_json(DATA_PATH)

def sample_data(data, test):
    subset = data[data['test'].apply(lambda x: test in x)]
    if test in ['fake news detection','conspiracy detection in articles']:
        MAX = 20
    elif test == 'stereotype identification in sexist tiktoks':
        MAX = 25
    elif test in ['hate speech detection', 'stereotype identification', 'irony detection', 'sexism identification in tiktoks']:
        MAX = 50
    else:
        MAX = len(subset)
    subset = subset.sample(MAX)
    idxs = subset.index.tolist()
    labels = [subset['label'][i][subset['test'][i].index(test)] for i in idxs]
    media = subset['media'][idxs].tolist()
    return idxs, labels, media

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
    #try:
    test = request.form.get('task')
    password = request.form.get('password')
    if not password in PASSWORDS:
        return render_template('index.html', error='Invalid password')
    idxs, labels, media = sample_data(data, test)
    
    # Store data in server-side session
    session['texts'] = idxs
    session['labels'] = labels
    session['results'] = [0] * len(idxs)
    session['curr_t'] = 0
    session['test'] = test
    session['task'] = data['task'][idxs[0]][data['test'][idxs[0]].index(test)]
    session['media'] = media
    session['f1'] = 0
    session['acc'] = 0
    # except:
    #     print('Error')
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
    text = text if text else ''
    headline = data['headline'][session['texts'][curr_t]]
    test = session['test']
    task = session['task']
    name1 = LABEL[task][0]
    name2 = LABEL[task][1]
    image = session['media'][curr_t] if session['media'] and data['media_type'][session['texts'][curr_t]] == 'image' else None
    video = session['media'][curr_t] if session['media'] and data['media_type'][session['texts'][curr_t]] == 'video' else None
    # print('Test:',test)
    # print('Media:',session['media'][curr_t])
    # print('Headline:',headline)
    # print('Text:',text)
    return render_template('classify.html', 
                           task=test, 
                           text=text, 
                           headline=headline, 
                           button1=name1, 
                           button2=name2,
                           current=curr_t+1,
                           max=len(session['texts']),
                           image=image,
                           video=video)

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
    test = session['test']
    
    f1 = f1_score(labels, results)
    acc = accuracy_score(labels, results)
    session['f1'] = f1
    session['acc'] = acc
    return render_template('report.html', f1_score=f"{f1:.2%}", accuracy=f"{acc:.2%}", task=test)

@app.route('/send_report', methods=['POST'])
def send_report():
    if 'results' not in session:
        return redirect(url_for('index'))
        
    user_name = request.form.get('user_name')
    test = session['test']
    results = session['results']
    labels = session['labels']
    
    f1 = session['f1']
    acc = session['acc']
    
    subject = f"{test.capitalize()} Classification Report: {user_name}"
    body = f"Report of {user_name}:\nF1 Score: {f1:.2%}\nAccuracy: {acc:.2%}"
    
    send_email(SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL, subject, body)
    hora = ctime(time())
    with open('log.csv','a') as log:
        log.write(f'{user_name},{test},{hora},{f1:.2%},{acc:.2%}\n')
    log = DataFrame({'user':user_name,'time':hora,'samples':str(session['texts']),'answ':str(results)},index=[0])
    log = concat((read_json('answ.json'),log),ignore_index=True)
    log.to_json('answ.json',orient='records')
    return redirect(url_for('index'))

# Redirect all HTTP traffic to HTTPS
# @app.before_request
# def before_request():
#     if not request.is_secure and app.env != 'development':
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)

if __name__ == '__main__':
    # app.run(debug=True) # For local development
    app.run(host='0.0.0.0', port=5000, debug = False) # For deployment
