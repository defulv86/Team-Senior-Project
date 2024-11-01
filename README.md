Installation along with instructions to make sure it works properly.

1. Clone the repository to your local repository: git clone https://github.com/defulv86/Team-Senior-Project.git

2. Go to the following directory after the clone is complete: Team-Senior-Project/ppst

3. Please add the virtual environment by either of the following two commands:
    python -m venv venv
    py -m venv venv

4. Activate the virtual environment: source venv/scripts/activate

5. Install the django into the directory: pip install django

6. Perform the migrations: py manage.py makemigrations

7. Finalize the migrate: py manage.py migrate

8. Install the fixture: py manage.py shell < fixture.py

9. Run the project: py manage.py runserver
