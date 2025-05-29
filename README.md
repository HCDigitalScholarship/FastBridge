# FastBridge

A newer faster Bridge

Full reference documentation is here:
https://docs.google.com/document/d/1OLF_AXg8-KjiQozGNCCo6V-dmIm8jeIk8udHJ8xuvkI/

Bridge provides several tools to help students of Ancient Languages – currently Latin and Greek, but hopefully Sanskrit, Armaiac, and Coptic will be added soon.
Bridge has three main tools/apps: Lists, Oracle, and Lemmatizer. Lists helps make custom vocabularly lists, and Oracle gives the most familiar sections in an unfamiliar work.

Lemmatizer tries to do the boring part of lemmatizing texts, matching all the lemma that have only one possibility.

---

# Local development

To whom this reaches, definitely follow these directions chronilogically to get setup the quickest, you'll be installing virtual environement, and loading the packages into the environment rather than your machine directly.

## 1. Set up a virtual environment

`pip install virtualenv`

`python3 -m venv env`

Linux/Mac: `source env/bin/activate` Windows: `env/Scripts/activate` - activate the envrionemnt in the terminal

`python -m pip install --upgrade pip` - not really necessary but useful.

`pip install -r requirements.txt` - install the packages into the environment

### Notes

Use python 3.11

## Requirements.txt notes

if cltk, numpy, protobuf,  stanza have version numbers specified in requirements.txt, remove them, let pip do the work when reinstalling requiremnts

make sure to specifiy PyYAML==6.0.1 in requirements.txt

may also have to pip install pybind11 before using pip install -r requirements.txt -> pybind11 is used by fasttext which is imported by cltk in requirements.txt

## Useful commands

`deactivate` = get out of python env

`rm -r env` = remove current python environment, useful for reinstalling dependencies

`uvicorn main:app --host=0.0.0.0 --port=${PORT:-5001}`
= use this instead of heroku to locally host the app, you must be in FastBridge/FastBridgeApp for this to work , can use other port numbers but I've been using 5001.

while running uvicorn:
`Ctrl + C`    =    stop uvicorn processes, useful for making a change in code, saving, then hosting new changes locally

If out of uvicorn, but you cannot run the host command due to activity on that port:
`lsof -i :5001`    =  list the current activity on port 5001(or whatever you chose previously), look for the PID number if anything shows up
`kill -9 PID_CODE`  = using the PID you identified using lsof, kill that process, then try hosting through port 5001 again

the app will be running on http://localhost:5001/, so navigate to that in your browser to test the changes

## IMPORTANT - BELOW THIS LINE IS OLD README SETUP ONLY.  DO NOT DELETE

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

# Troubleshooting server errors

For nginx errors: `tail -n 200 var/log/nginx/error.log`

For application errors: `tail -n 200 /var/log/gunicorn.error.log`
