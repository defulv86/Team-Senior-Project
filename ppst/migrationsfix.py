import os
import subprocess

# Paths for the files and directories
db_path = "db.sqlite3"
migration_path = "website/migrations/0001_initial.py"
fixture_script = "fixture.py"  # Ensure fixture.py is in the same directory

# Step 1: Delete db.sqlite3 if it exists
if os.path.exists(db_path):
    print("Deleting database file db.sqlite3...")
    os.remove(db_path)
else:
    print("Database file db.sqlite3 does not exist. Skipping deletion.")

# Step 2: Delete migration file 0001_initial.py if it exists
if os.path.exists(migration_path):
    print("Deleting migration file 0001_initial.py...")
    os.remove(migration_path)
else:
    print("Migration file 0001_initial.py does not exist. Skipping deletion.")

# Step 3: Run makemigrations command
print("Running makemigrations...")
subprocess.run(["py", "manage.py", "makemigrations"])

# Step 4: Run migrate command
print("Running migrate...")
subprocess.run(["py", "manage.py", "migrate"])

# Step 5: Load fixture data by running a script in the Django shell
if os.path.exists(fixture_script):
    print(f"Running fixture script: {fixture_script}...")
    subprocess.run(["py", "manage.py", "shell", "<", fixture_script], shell=True)
else:
    print(f"Fixture script {fixture_script} not found. Please ensure it is in the project directory.")