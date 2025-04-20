# Flask Backend Application

This is a Flask-based backend application with optimized structure and setup.

## Project Structure

```
.
├── src/                    # Source code directory
│   ├── __init__.py        # Application factory
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/            # API routes
│   │   ├── __init__.py
│   │   └── routes.py
│   └── utils/             # Utility functions
│       └── response.py
├── app.py                 # Application entry point
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the variables in `.env` as needed

## Running the Application

To run the application in development mode:
```bash
flask run
```

The server will start at `http://localhost:5000`

## API Endpoints

- `GET /api/health`: Health check endpoint
- `GET /api/users`: Get all users endpoint

## Features

- Optimized project structure
- SQLAlchemy database integration
- Password hashing with bcrypt
- Standardized API responses
- CORS support
- Environment variable configuration
- Error handling 