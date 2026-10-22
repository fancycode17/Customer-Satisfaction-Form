Below is a list of potential errors and how to fix them:
* **Python command not found**: Install Python 3.12 or newer and ensure it is available on your command line. Ensure there are no spelling mistakes in the command.
* **Dependency installation fails**: Verify that the virtual environment is activated and that your Python version is compatible.
* **MIssing `DJANGO_SECRET_KEY`**: Check that `.env` exists in the project root and contains a valid secret key.
* **Database errors**: run `python manage.py migrate` from the `main/` directory.
* **Port already in use**: Start the server on another port (e.g. 8001).
* **PowerShell activation is blocked**: Review your PowerShell execution policy or use Command Prompt instead.