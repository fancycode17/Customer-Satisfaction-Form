# customer-satisfaction-form
(**Note**: this guide assumes you have already installed the required software needed to setup and install the application. If you haven't done so already, please see the [prerequisites](prerequisites.md))

## Setup

1. Download Project repository
    - **Option A: Download ZIP**
        1. Download repository as a ZIP file
        2. Extract the ZIP file
        3. Open the extracted project folder in your terminal or code editor

    - **Option B: Clone with Git**
        1. Run: `git clone https://github.com/fancycode17/Customer-Satisfaction-Form.git`
        2. Run: `cd Customer-Satisfaction-Form`
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - If using Windows Command Prompt (cmd): `.venv\Scripts\activate.bat`
   - If using Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - If using macOS/Linux bash/zsh: `source .venv/bin/activate`
   - If using macOS/Linux fish: `source .venv/bin/activate.fish`
4. Install Python dependencies: `pip install -r requirements.txt`
5. Configure environment variables
    1. Create a new file `.env` in the project root and copy the code from `.env.example` to it.
    2. Generate a new secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
    3. In `.env` replace the placeholder value of `DJANGO_SECRET_KEY` with the generated key.
    4. Check that the development settings are appropriate for your environment.
**Note: never commit `.env` or real secret values to Git**
6. Prepare the database. From the project root run:
    - `cd main`
    - `python manage.py migrate`
7. Verify the installation
    - Run the Django configuration check: `python manage.py check`
    - Run the preprepared tests: `python manage.py test`. If Django states that zero tests were found, check test files and configuration.

## Running the Program

1. Navigate to `customer-satisfaction-form/main`
2. Start the development server: `python manage.py runserver`
3. Open the local address displayed in the terminal (usually http://127.0.0.1:800)
4. Optional - to use another port (e.g. if port 8000 is occupied): `python manage.py runserver [port number]`, replacing `[port number]` with the port you would like to run the application on.
5. Press `Ctrl+C` in the terminal to stop the development server.

## Running on your local network

The steps above enable the application to run on your computer. However, the application won't be accessible on other devices on the local network.

To enable other devices on the local network to access the application, run `python manage.py runserver 0.0.0.0:8000`. The address will be your IP address, followed by the port number (in this case 8000).

To locate your port number, run the following in the terminal based on your OS:
- Windows: `ipconfig`. Your IP address can be found on the line that starts with `IPv4 Address...`
- macOS/Linux: `ip addr`
- macOS/Linux: `hostname -I`

**Example (Windows OS)**:
Output of `ipconfig` (the line that starts with `IPv4 Address...`) is `IPv4 Address. . . . . . . . . . . : 192.168.0.21`, and the port number is 8000. Therefore, the application can be accessed at: http://192.168.0.21:8000.

## Aditional Documentation

* Make sure the system [prerequisites](prerequisites.md) are installed.
* Any issues? Visit the [troubleshooting](troubleshooting) page or [create an issue](https://github.com/fancycode17/Customer-Satisfaction-Form/issues)
* Learn [how the application works](architecture.md)