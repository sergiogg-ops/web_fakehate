# Natural Language Processing

This is the source code for creating a web page to test the abilities of humans in several NLP task. This website was created at Pattern Recognition and Human Language Technology (PRHLT) research center with educational purposes. This version uses the same external look as the previous one, but we have kept improving the code and easing the maintenance.  It also includes a new task, these are the supported tests: 
- Fake news detection: 20 articles are shown from a total amount of 50, that must be classified between 'Real' or 'Fake'.
- Hate speech detection: 50 short texts are shown from a total amount of 75, that must be classified between 'Hate speech' or 'Non hate speech'.
- Steretype identification: 50 short texts are swon in a random order and must be classified between 'Steretypical' or 'Non stereotypical'.
- Irony detection: 50 short texts are shown in a random order and must be classified between 'Ironic' or 'Non ironic'.
- Sexism identification in tweets: 50 short texts are shown in a random order and must be classified between 'Sexist' or 'Non sexist'.
- Stereotype identification in sexist tweets: 50 short texts are shown in a random order and must be classified between 'Steretypical' or 'Non stereotypical'.
- Sexism identification in memes: 50 images are shown in a random order and must be classified between 'Sexist' or 'Non sexist'.
- Stereotype identification in sexist memes: 50 images are shown in a random order and must be classified between 'Steretypical' or 'Non stereotypical'.
- Sexism identification in videos: 50 videos are shown in a random order and must be classified between 'Sexist' or 'Non sexist'.
- Stereotype identification in sexist videos: 25 videos are shown in a random order and must be classified between 'Steretypical' or 'Non stereotypical'.
- Conspiracy theories detection: 20 articles are shown from a total amount of 30, that must be classified between 'Conspiracy' or 'Mainstream'.

The result of each session is sent to an email address and also stored in the local file system. To control who can do the test we have included a password that need to be verified at the beggining of each session.

# Administrator guide
This section is dedicated to the deployment and posterior updating of the web page. It contains the details about the implementation of the database and the semantics of the required fields along with some advises about the development.
## Deploy process
In order to deploy this web you will need to have a fixed DNS identificator for your server. Then you must update the files `flaskapp` and `flaksapp.service` with your server values. You can create the python environment to lauch the process by using the `requirements.txt` file and pip:
```sh
pip install -r requirements.txt
```
To deploy the web in linux (in other OS might be different) do the following:

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

## Web maintenance
There are several variables that should be adjusted for each specific application of the web:
- For maintenance and debugging the app should be runned in debug mode: `app.run(debug=True)`.
- The email with the results of each session is sent using a gmail account. You should set the constant `SENDER_EMAIL` to the address of you gmail account. You will also need to generate an app specific password and set the constant `SENDER_PASSWORD` to it. Finally, you should set the `RECEIVER_EMAIL` constant to the account in which you would like to receive the reports. This late email account doesn't need to be gmail account, it can be from any mail server.
- The evaluation of the sessions is stored in the `log.csv` file and includes the user name, test name, time, F-1 score and accuracy obtained by the user. More detailed information is stored in the `answ.json` file, with also the samples index that were presented to the user and the classification that they performed.
- The password that the users must provide should be included in the list of the constant `PASSWORDS`.
- If you want to change the data that the app uses you can either modify the `data.json` file or update the `DATA_PATH` constant to your json file. With both options the samples must include the following fields:
    - `headline`: stores the headline of the fake news test samples.
    - `text`: stores the main text of the samples.
    - `test`: identificator of the test for which the sample will be used (list).
    - `task`: identificator of the tasks for which the sample has been labelled (list).
    - `label`: stores the label of the sample for the different tasks. It is a list of binary values each one of which is related to the task in the same index.
    - `media`: stores the name of the file that includes the image or video in the corresponding folder: `static/memes_images/` or `static/tiktok_videos/`.
    - `media_type`: stores a value that represents the content of `media`, either 'image' or 'video'.
- The original sources of data are stored in the `orig_data` folder and the `data.json` file can be recovered from the using the `orig_data/create_data.py` script.
- The script `orig_data/add_loco.py` can be used to ad more samples from a dataset in the format of [LOCO corpus](https://osf.io/snpcg/).
- For the changes to be applied the debug mode should be unset and the `app.run(host=0.0.0.0, port=80, debug = False)` is more appropiate. The service should also be restarted, what can be done with the `restart.sh` script.