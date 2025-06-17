# Installation Guide


## Database setup

Install MariaDB.

Go to `src\backend\ReadOnly_Database\MariaDB\requirements.txt` and install requirements.

Go to `src\backend\ReadOnly_Database\MariaDB\create_db.py` and execute the file using python.

You may have to alter the root credentials in create_db.py to match your root user and password. (Default root username: root; default root password: root)



## Backend setup
Do Database setup

Go to `src\backend\OpenAPI_Server\output\requirements.txt` and install requirements.

Go to `src\backend\OpenAPI_Server\output\start_server.py` and execute the file using python.



## Live Demo Setup
Do Database setup

Go to `src\backend\ReadOnly_Database\MariaDB\requirements.txt` and install requirements.

Go to `LiveSimulation\create_livedemo_table.py` and execute the file using python.

Go to `LiveSimulation\app.py` and execute the file using python.

Visit `localhost:7042` to access the Live Demo


## Frontend setup

**<span style="color:red">TODO: Add frontend setup instructions here.</span>**






