# itcs3155finalproject
Welcome to our groups final project.
To initalize your virtual environment, run
python -m venv venv
To activate it, run
venv/Scripts/Activate
To download requirements, run
pip install -r requirements.txt
To deactivate your virtual environment, run
deactivate
If you install new packages, you can add them to the requirements.txt by running
pip freeze > requirements.txt

Once you have a linked db (Changing SQLACLEHMY_DATABASE_URI to your database URL), you can run "flask db init" to initialize it.
To set up the databases, run "flask db migrate -m"
then "flask db upgrade". (Or you can use a program like MySQL Workbench to manually set up the tables, going off of models.py)
