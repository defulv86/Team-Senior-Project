Installation along with instructions to make sure it works properly.

1. Clone the repository to your local repository: git clone https://github.com/defulv86/Team-Senior-Project.git

2. Go to the following directory after the clone is complete: Team-Senior-Project/ppst

3. Please add the virtual environment using either of the following two commands:
    - macOS/Linux: python -m venv venv
    - Windows:     py -m venv venv

4. Activate the virtual environment: source venv/scripts/activate

5. Install the Django and Python-Dateutil with this command:
    pip install -r requirements.txt

6. Open Task Scheduler on Windows:
    - Click on the "Create Task" button.
    - Give the Task a name (Check Test Status)
    - Go to the 'Triggers' tab and click 'New'.
        - For the settings, set it up as daily. 
        - In the advanced settings, check the 'Repeat task every:' and select '5 minutes' from the dropdown menu. Then 'for a duration of', select 1 day.
        - Click ok at the bottom
    - Go to the 'Actions' tab and click 'New'
        - Keep Action as "Start a program"
        - For the 'Program/script', browse to your terminal. If using Git Bash, here's an example: "C:\Program Files\Git\git-bash.exe"
        - In the 'add arguments' box, put in this command: -c "directory/to/your/project/ppst/check_tests.sh" 
            - Here is an example: -c "/c/Users/nickp/November6/Team-Senior-Project/ppst/check_tests.sh"
        Click ok at the bottom.
    - OPTIONAL. In the Settings tab, you can choose whether you want to stop the task if it runs longer than an hour but that's up to you.
    - Click ok

7. in the Team-Senior-Project/ppst directory, run this command:
    - Windows: py migrationsfix.py

    - macOS/Linux will need to run these:
        python manage.py makemigrations
        python manage.py migrate
        python manage.py shell < fixture.py

8. Once you install the requirements needed.. You need to make one edit to a file in your virtual environment.
    - Go to your venv/Lib/django/contrib/admin/templates/admin/base.html
    - At line 48, replace the line with: 
        - <a href="{% url 'admin_dashboard' %}" class="headerlink">Back to Admin Dashboard</a>
    - Save the file.

9. Run the project: py manage.py runserver
