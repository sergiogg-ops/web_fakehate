# Natural Language Processing

This is the source code for creating a web page to test the abilities of humans in several NLP task. This website was created at Pattern Recognition and Human Language Technology (PRHLT) research center with educational purposes. In this version it offers a new modern look and includes a few changes towards normalization to reconcile different sources of data. It also includes new task, these are te supported tests: 
- Fake news detection: 20 articles are shown from a total amount of 50, that must be classified between 'Real' or 'Fake'.
- Hate speech detection: 50 short texts are shown from a total amount of 75, that must be classified between 'Hate speech' or 'Non hate speech'.
- Steretype identification: 50 short texts are swon in a random order and must be classified between 'Steretypical' or 'Non stereotypical'.
- Irony detection: 50 short texts are shown in a random order and must be classified between 'Ironic' or 'Non ironic'.

The result of each session is sent to an email address and also stored in the local file system. To control who can do the test we have included a password that need to be verified at the beggining of each session.

## Administrator guide
### Deploy process
In order to deploy this web you will need to have a fixed DNS identificator for your server. Then you must update the files `flaskapp` and `flaksapp.service` with your server values. Those are the steps for deployment in linux (in other OS might be different):

First, install the packages:
```sh
sudo apt-get update
sudo apt-get install nginx
```

Copy the systemd service file and setup Nginx:
```sh
sudo cp flaskapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
sudo cp flaskapp /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
sudo nginx -t
```

Finish the deployment by restarting the services:
```sh
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl restart flaskapp
chmod 777 flaskapp.sock
```
For this last step you can also use the `restart.sh` script.

### Web maintainance
There are several variables that should be adjusted for each application of the web:
- The email with the results of each session is sent using a gmail account. You should set the constant `SENDER_EMAIL` to the address of you gmail account. You will need to generate an app specific password and set the constant `SENDER_PASSWORD` to it. Finally, you should set the `RECEIVER_EMAIL` constant to the account in which you would like to receive the reports. This late email account doesn't need to be gmail account, it can be from any mail server.
- If you want to change the data that the app uses you can either modify the `data.json` file or update the `DATA_PATH` constant to your json file. With both options the samples must include the following fields:
    - `title`: stores the headline of the fake news test samples.
    - `text`: stores the main text of the samples.
    - `label`: stores the label of the samples. For the fake news text it should contain plain text with either 'Real' or 'Fake. For the rest of the task is a binary value (0 or 1).
- The evaluation of the sessions is stored in the `log.csv` file and includes the user name, test name, time, F-1 score and accuracy obtained by the user. More detailed information is stored in the `answ.json` file, with also the samples index that were presented to the user and the classification that they performed.
- The password that the users must provide should be included in the list of the constant `PASSWORDS`.
