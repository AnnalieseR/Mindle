# Mindle

Mindle is a project with both frontend and backend components, designed to be developed and run concurrently. This README provides instructions on setting up, running, and managing the project.

## Table of Contents
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Scripts](#scripts)
- [Dependencies](#dependencies)
- [License](#license)

## Installation
To set up Mindle, follow these steps:

1. **Clone the Repository:**

```bash
  git clone https://github.com/AnnalieseR/Mindle.git
  cd Mindle
```

2. **Install Dependencies:**

Run the following command to install all dependencies for both the frontend and backend:

```bash
  yarn setup
```

This will execute the `install-all` script, which:
- Installs frontend dependencies using `yarn install`.
- Installs backend dependencies using `yarn install`.
- Creates a Python virtual environment and installs Python dependencies from `requirements.txt`.

## Running the Project
To start the project, run:

```bash
  yarn start
```

This will execute the `start` script, which:
- Starts the frontend application using `yarn run frontend`.
- Starts the backend application using `yarn run backend`.

## Scripts
- `setup`: Installs all necessary dependencies for both frontend and backend.
- `install-all`: Installs dependencies for frontend and backend, sets up a Python virtual environment, and installs Python dependencies.
- `start`: Runs both the frontend and backend concurrently.
- `frontend`: Starts the frontend application.
- `backend`: Starts the backend server.


## License
This project is licensed under the `UNLICENSED` license.

