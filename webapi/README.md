# Nearby: Web API
Developed by Nick Jones

## Overview
The web API supports the Android client by handling a variety of data.  It
makes this data available using a REST API built using Python 3.4, Bottle,
SQLalchemy, and Postgres 9.3.

The primary functionality of the application is matching Bluetooth MAC addresses
to people.  The API handles the creation and management of user accounts,
devices, and MAC observerations.

## API Workflow
The Application/API workflow is as follows:

1. Users create accounts.
2. Users login to their account using their username and password
3. Users may edit/delete their accounts
4. Users register a device with the server by sending MAC to server.
5. Server stores pairing between users and MACs
6. User devices scan for other devices.  User devices are set to discoverable.
7. Any MACs seen get sent to the server as "observations"
8. Android client queries server for nearby users.
9. User responds with users based on recently seen MACs.

## Installation/Deployment
This code is intended to be deployed to an nginx server with Postgres.

To run this code on a fresh machine, you will first need to install virtualenv
using python3.4.

Next, perform `virtualenv .` in the same directory as this
README.

Next, activate the virtual env using `source bin/activate`.

Install dependencies using `pip install -r requirements.txt`

Now init the database using `alembic upgrade head`.  You must be in the same
directory as alembic.ini for this to work.  Postgres login information is
contained in alembic.ini and webapi.py.  You should change this information
to match the login information for your server.

Now, run the deployment script `src/install.bash`.  This will move
files to the right places and start the server processes.  If your
sever configuration is different, you may need to change this script.
