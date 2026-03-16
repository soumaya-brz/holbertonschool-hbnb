# HBnB Project – Part 3

## Description
Backend REST API pour gérer : utilisateurs, lieux, reviews et commodités.  
JWT pour authentification, rôles admin et persistance via SQLAlchemy.

<img width="342" height="605" alt="CaptureER png" src="https://github.com/user-attachments/assets/00838cf1-4b6f-4037-afb5-0d0ec3588dbb" />

## Installation
```bash
git clone <repo-url>
cd holbertonschool-hbnb/part3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app
export FLASK_ENV=development
flask run
