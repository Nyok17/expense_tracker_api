#expense_tracker_api

A simple expense tracker api which enable users to register, login and manage their expenses.

## Features

- JWT-based user authentication
- Password hashing with Bcrypt
- Create(POST), Retrieve(GET), Update(PUT) and Delete(DELETE) for todos
- Filter by past week, past 1 month and past 3 months
- Database integration with postgreSQL database
- Custom error handling
- Flask Blueprint
- `.env` support for secret keys

## Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- PostgreSQL
- dotenv

## Getting Started

1. Clone the Repo:
   ```bash
   git clone https://github.com/Nyok17/expense_tracker_api.git
   ```

2. Roadmap project url:
   ```bash
   https://roadmap.sh/projects/expense-tracker-api
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the API:

   ```bash
   python main.py
   ```

## API

1. User(Authentication) Routes
   -POST /register: Create a new user using username, email and password
   -POST /register: Login a registered user using email and password

2. Expense Routes 
   -POST /expenses: Create a new expense.
   -GET /expenses: Retrieve all expenses for the authenticated user.
   -GET /expenses/<int:id>: Retrieve a specific expense by ID.
   -PUT /expenses/<int:id>: Update an existing expense.
   -DELETE /expenses/<int:id>: Delete an expense.

3. Filtering example Queries
   -Get past week:
      -GET /expenses?filter=week
   -Get past month:
      -GET /expenses?filter=month
   -Get past 3 months:
      -GET /expenses?filter=3months
   -Custom range:
      -GET /expenses?start_date=2025-05-01&end_date=2025-05-15

## License
MIT
