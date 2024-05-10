# Price monitoring bot

### This bot fetches the USD/UAH exchange rate from Google Finance, stores the values in an SQLite database, and sends the accumulated price values to the user over time.

To start using this script, you need to:
- Have Python installed
- Download this repository to your local machine
- Create a virtual environment using the command ```python -m venv .venv```
- Activate the virtual environment: ```.venv\Scripts\activate```
- Install all necessary dependencies: ```pip install -r requirements.txt```
- Start: ```python app.py```

To run on local macine:
- Open the .env file and replace YourToken on your key from Telegram

Deploy:
- delete .env file, than add environment variables form .env