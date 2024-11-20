# Natural Language Processing

This is the source code for creating a web page to test the abilities of humans in several NLP task. Currently it is just a prototype and only supports two tasks: 
- Fake news detection: 20 articles are shown from a total amount of 50, that must be classified between 'Real' or 'Fake'.
- Hate speech detection: 50 short text are shown from a total amount of 75, that must be classified between 'Hate speech' or 'Non hate speech'.

The result of each session is sent to an email address and also stored in the local file system.

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
- If you want to change the data that the app uses you can either modify the `data.json` file or update the `DATA_PATH` constant to your json file.