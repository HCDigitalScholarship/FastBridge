# FastBridge [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/HCDigitalScholarship/FastBridge/tree/dev)

A newer faster Bridge
Full reference documentation is here: https://docs.google.com/document/d/1OLF_AXg8-KjiQozGNCCo6V-dmIm8jeIk8udHJ8xuvkI/
Bridge provides several tools to help students of Ancient Languages – currently Latin and Greek, but hopefully Sanskrit, Armaiac, and Coptic will be added soon.
Bridge has three main tools/apps: Lists, Oracle, and Lemmatizer. Lists helps make custom vocabularly lists, and Oracle gives the most familiar sections in an unfamiliar work.
Lemmatizer tries to do the boring part of lemmatizing texts, matching all the lemma that have only one possiblity.

---

# Local development

## 1. Set up a virtual environment

`pip install virtualenv`

`python3.7 -m venv env`

`source env/bin/activate`

`python -m pip install --upgrade pip`

## 2. Set up your Google API Files and Credentials
You need to create personal Google API files to work on this project. Follow [these instuctions](https://developers.google.com/sheets/api/quickstart/python), which are also summarized here:

**Create credentials for a Google service account**

Follow the instructions [here](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id) to create a credentials file.

Save the file in the root of the eproject as `credentials.json`

Follow [these instructions](https://stackoverflow.com/a/39065422) to add your localhost as a redirect URI on the credentials

`touch FastBridgeApp/quickstart.py`

Edit the new quickstart.py file (should be in the FastBridgeApp directory) to contain [this text](https://github.com/googleworkspace/python-samples/blob/master/sheets/quickstart/quickstart.py)

Follow the prompts in the browser to complete Google Sheets Authorization

## 3. Finish installing requirements and run local server:

`pip install -r requirements.txt`

`heroku local`

The app will be running on http://0.0.0.0:5000/

---

# Deploying the dev app

This project is configured to automatically deploy the `dev` branch to heroku.

The dev app is available at: https://fastbridge-dev.herokuapp.com
