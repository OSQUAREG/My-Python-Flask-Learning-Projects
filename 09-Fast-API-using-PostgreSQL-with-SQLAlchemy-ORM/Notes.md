1. Create the Project Folder
2. Check that the python version is version 3: 
   `$ py -3 --version`
3. Create your virtual environment venv: 
   `py -3 -m venv venv`
4. Activate your venv: 
   `venv/Scripts/activate`
5. Install all Fast API packages: 
   `pip install fastapi[all]`
6. Install uvicorn to work as the server that runs the code: 
   `pip install uvicorn[standard]`
7. Install the Postgres driver for db, psycopg2: 
   `pip install psycopg2`
8. Install the SQLAlchemy as the ORM: 
   `pip install sqlalchemy`
9. Then create `main.py` file and start coding.
10. **Starting Your Server:** use: `uvicorn main:app` This will run the code in your localhost but changes in your code will not auto-update to the running server. Usually for production. 
    However, you can use `uvicorn main:app --reload` to continually update your code to the running server as you make changes to the code. Use this for development.
    Note: `main` is the `main.py` file name and app is the `app` initialized in the `main.py` file. 
    Also note, if the main.py is in a package folder e.g. named `app`, then use: `uvicorn app.main:app --reload`
11. **Hashing Your Password:** install passlib library for hashing the user's password before saving it in the DB: 
    `pip install passlib[bcrypt]` 
12. **Creating JWT Tokens for Sessions:** Install python-jose[cryptography] to create JWT Tokens for user authentications: 
    `pip install python-jose [cryptography]` 
13. **Using Database Migration Tool:** Install alembic as the database migration tools, to make and track changes to models on database tables. `pip install alembic`. 
    Read docs @ https://alembic.sqlalchemy.org/en/latest/tutorial.html 
14. **Initialize Alembic** and also create a directory called alembic (or any use any name) using: `alembic init alembic` 
15. **Setting up Alembic:** Go to the alembic folder, then to env.py and import `Base` from `app.models`. Then change the `target_metadata` from `None` to `Base.metadata`.
16. Under the line: `config = context.config`, set a new config main option as: 
    `config.set_main_option("sqlalchemy.url", f"postgresql+psycopg2://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}")"`
    This will override the variable `sqlalchemy.url` in alembic.ini line 58. This way you can use the env variables earlier defined in database.py for SQLALCHEMY_URL. 
    Note: Remember to first import settings from app.config, then define the variables past into the f string. This will help us avoid hard-coding the env variable values into the sqlalchemy url.
17. Go to the alembic.ini file, then comment out line 58 having the `sqlalchemy.url`. 
18. **Create a Migration Script by Creating Alembic Revision:** On the terminal, use `alembic revision -m` to track database changes like a `git commit -m`.
    `alembic revision -m "create posts table"` 
        or use 
    `alembic revision --autogenerate -m "auto-create tables`
19. Go to the version folder and click on the new revision just created and edit the `def upgrade` and `def downgrade`.
20. On the `def upgrade` function, write the code to perform actions on the database. Then on the `def downgrade` function, write the code to undo it.
21. **Setup CORS Middleware** in the main.py to allow API communicate with other domain. Read more here: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS and https://fastapi.tiangolo.com/tutorial/cors/ 
22. 
 