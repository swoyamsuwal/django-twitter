import subprocess
import os

# Path to your Django project (adjust if needed)
project_path = os.path.join(os.getcwd(), 'admin')

# Change working directory to the Django project folder
os.chdir(project_path)

# Run the Django development server
subprocess.run(["python", "manage.py", "runserver"])
