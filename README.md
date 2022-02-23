# SMS-OTP
Python Flask application to create and verify 6-digit OTPs :)

Has both a frontend and backend version, based on what you need to use it for.

The frontend version comes with a (you guessed it!) frontend that you can interact with. The backend version requires a client that can send HTTP Requests to it, and does not come with a webpage to interact with.

It utilizes a SQLite database to store and verify OTPs. Should massive scalability be required, this can be moved to a SQL database too. However, this code is not tested for massive scale or other functionalities, so do make the required changes and testing if you use it.

The application is run on Flask, a very compact and simple application that serves its function and nothing else. No CSS whatsoever either for the frontend.

## How To Install
Requires Python (3.8+ recommended) to be installed
1. Clone this repo and do `pip install -r requirements.txt`
2. Create the database with `py init_db.py`
3. Create a `.flaskenv` file with the following information: `FLASK_APP=<CHANGETHIS> FLASK_ENV=development` with `FLASK_APP` being "backend" or "frontend" depending on the version you are using
4. Run `flask run`

### Frontend Version
1. Open your browser and browse to `127.0.0.1:5000` or your own custom address if you changed it
2. Use the nav points to create and verify your OTPs
3. Frontend is very easy to use!

### Backend Version
1. The client should be sending requests to `127.0.0.1:5000` or your own custom address if you changed it
2. The 3 endpoints available are `/` , `/create` and `/verify`
3. The create and verify endpoints allow both GET and POST requests
4. When you send a GET request, the API returns information about it and how to use it
5. Send a POST request to create and verify OTPs at their respective APIs
6. You can do this with a front-end application, Postman or similar tools