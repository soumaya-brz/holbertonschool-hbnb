# HBnB Project – Part 3

## Description
Backend REST API pour gérer : utilisateurs, lieux, reviews et commodités.  
JWT pour authentification, rôles admin et persistance via SQLAlchemy.

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
