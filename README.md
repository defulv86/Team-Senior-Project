Installation along with instructions to make sure it works properly.

1. Clone the repository to your local repository: git clone https://github.com/defulv86/Team-Senior-Project.git

2. Go to the following directory after the clone is complete: Team-Senior-Project/ppst

3. Please add the virtual environment using either of the following two commands:
    - macOS/Linux: python -m venv venv
    - Windows:     py -m venv venv

4. Activate the virtual environment: source venv/scripts/activate

5. Install the Django and Python-Dateutil with this command:
    pip install -r requirements.txt

6. in the Team-Senior-Project/ppst directory, run either of these two commands:
    - Windows:
        For only real data (regular fixture), run:
            migrate_regular_fixture.py
        For only fake data, run:
            migrate_fake_test_data_fixture.py
    - macOS/Linux:
        For only real data (regular fixture), run:
            python manage.py makemigrations
            python manage.py migrate
            python manage.py shell < regular_fixture.py
        For only fake data, run:
            python manage.py makemigrations
            python manage.py migrate
            python manage.py shell < fake_data_fixture.py

7. Once you install the requirements needed.. You need to make one edit to a file in your virtual environment.
    - Go to your venv/Lib/django/contrib/admin/templates/admin/base.html
    - At line 48, replace the line with: 
        - <a href="{% url 'admin_dashboard' %}" class="headerlink">Back to Admin Dashboard</a> /
    - Save the file.

8. Run the project: py manage.py runserver
