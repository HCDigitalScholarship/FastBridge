# FastBridge

A newer faster Bridge

Full reference documentation is here:
https://docs.google.com/document/d/1OLF_AXg8-KjiQozGNCCo6V-dmIm8jeIk8udHJ8xuvkI/

Bridge provides several tools to help students of Ancient Languages – currently Latin and Greek, but hopefully Sanskrit, Armaiac, and Coptic will be added soon.
Bridge has three main tools/apps: Lists, Oracle, and Lemmatizer. Lists helps make custom vocabularly lists, and Oracle gives the most familiar sections in an unfamiliar work.

Lemmatizer tries to do the boring part of lemmatizing texts, matching all the lemma that have only one possibility.

---

# Local development

## 1. Set up a virtual environment

`pip install virtualenv`

`python3.7 -m venv env`

`source env/bin/activate`

`python -m pip install --upgrade pip`

## 2. Set up your Google API Files and Credentials

> Note: this step is optional for local development.

You need to create personal Google API files to work on this project. Follow [these instructions](https://developers.google.com/sheets/api/quickstart/python), which are also summarized here:

**Create credentials for a Google service account**

Follow the instructions [here](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id) to create a credentials file.

Save the file in the root of the project as `credentials.json`

Follow [these instructions](https://stackoverflow.com/a/39065422) to add your localhost as a redirect URI on the credentials

## 3. Finish installing requirements and run local server:

`pip install -r requirements.txt`

`heroku local`

The app will be running on http://0.0.0.0:5000/

## Logging in

To access authorized views (eg `/account/login`), you need an account in the SQLite database located at `FastBridgeApp/sql_app.db`. You may open this file in an SQLite3 editor and add your account.

The easiest way is to copy the sample database, which already has an `admin`/`admin` account:

```
cp FastBridgeApp/sql_app.example.db FastBridgeApp/sql_app.db
```

You can now log in with user: `admin`, password: `admin`.

---
# Deploying

## Deploying the dev app (BROKEN)

This project is configured to automatically deploy the `dev` branch to heroku.

The dev app is available at: https://fastbridge-dev.herokuapp.com

*As of June 2022 the heroku dev app is broken due to issues with running out of ram. We recommend just doing local development*


## Deploying to dev/production on DigitalOcean

**1. Shell into the server and the cd to the FastBridge directory**

`cd /srv/FastBridge`

**2. Update Python dependencies**

`source /srv/bridge_env/bin/activate`

`pip install -r requirements.txt`

**3. Update git repo**

`git pull origin master`

**4. Restart the application**

`systemctl restart gunicorn`

---

# Setting up the server
*Some incomplete notes on setting up the server. See also /installation for starting config files*

certbot --nginx -d example.url -> [2]

cd /srv/FastBridge

source /srv/bridge_env/bin/activate

pip install -r requirements.txt

---

# Merging Files From Production
*Due to the nature of this project, some files are updated direclty on the server by the Admin through the web portal. The changes to these files need to be re-incorporated occassionally into the git history. This is notthe ideal way to do this, with changes flowing in opposite directions, but it is how it currently is. TODO: Fix this.*

**Follow these instructions to incorporate files from Prod into master:**

1. On the prod server: `git status` to view changed files

2. On your local machine: ensure master is up to date. Create and checkout a new branch, ex. `git checkout -b prod-updates`

3. Locally: copy all changed files down into your project directory. ex `scp root@[IP_ADDRESS]:/srv/FastBridge/FastBridgeApp/Latin.py ./FastBridgeApp/Latin.py`

4. Locally: commit the changes and push branch to origin

5. On Github: create a pull request and manually review the changed files and any conflicts. Merge when ready.

6. On prod: `git pull origin master`

If everything has gone right, both master and production should now be the same, incorporating both versions of files. If you messed up the production git at some point (ex. by making a commit or tracking files that are preventing you from pulling), you may need to clean the prod server first. Be sure to scp any files you want to preserve down to your local machine first. **Cleaning git will remove these files from prod!** Use `git reset --hard [COMMIT_HASH]` to update to the last good commit. Then, `git clean -f -d`. You should now be able to pull master without issue.

---

# Troubleshootign server errors

For nginx errors: `tail -n 200 var/log/nginx/error.log`

For application errors: `tail -n 200 /var/log/gunicorn.error.log`
