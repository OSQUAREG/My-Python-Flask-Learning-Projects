# sLearning Flask API - AltSchool

#### Basic Steps:

1. Create your virtual environment

   ```
   python -m venv flaskapienv
   ```
2. Activate your virtual environment

   ```
   source flaskapienv/Scripts/activate
   ```
3. Install the APIFlask and other needed packages

   ```
   pip install APIFlask python-dotenv SQLAlchemy
   ```
4. and also do `pip freeze > requirements.txt`

   Create `.falskenv`or `.env` file in the base directory and enter your app configs into it as:

   ```
   FLASK_ENV = development
   FLASK_DEBUG = 1
   FLASK_APP = main.py (or app.py)
   ```
5. Document your installed packages into a .txt file.

   ```
   pip freeze > requirements.txt
   ```
6. Create the `main.py` (or `app.py`) file to contain the different decorators such as:

   ```
   # for retrieving
   @app.get()
   @app.output()

   # for creating
   @app.post()
   @app.output()
   @app.input()

   # for updating
   @app.put()
   @app.output()
   @app.input()

   # for deleting
   @app.delete()
   ```
7. 
8. Also create the `db.py` for your database models, creations and sessions configs.
9. After writing your lines of code for the database creations and model in `db.py`, run db.py using: `python db.py` to create the databse.
10. Create a `schema.py` file where you will create all your schemas, used for serializing fields in the database.
