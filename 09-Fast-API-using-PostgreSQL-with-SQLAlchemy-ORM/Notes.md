1. Create the Project Folder
2. Check the python version is version 3:
    `$ py -3 --version`
3. Create your virtual environment venv: 
`py -3 -m venv venv`
4. Activate your venv: `venv/Scripts/activate`
5. Install Fast API package: `pip install fastapi[all]`
6. Install uvicorn to work as the server that runs the code: `pip install uvicorn[standard]`
7. Install the Postgres driver for db, psycopg2: `pip install psycopg2`
8. Install the ORM SQLAlchemy: `pip install sqlalchemy`
9. Then create `main.py` file and start coding.
10. Start your server using: `uvicorn main:app` This will run the code in your localhost without updating the changes 
    you make to the code. Usually for production. 
11. However, you can use `uvicorn main:app --reload` to continually update your code to the server as you make 
   changes to the code. Good for development.
Note: `main` is the `main.py` file name and app is the `app` initialized in the `main.py` file 
12. Or if its in a package folder e.g folder name: app, `uvicorn app.main:app`
13. Also install passlib library for hashing the user's password before saving it in the DB: `pip install passlib[bcrypt]` 
14. Install python-jose[cryptography] to create JWT Tokens for user authentications: `pip install python-jose [cryptography]` 
15. Install alembic as the database migration tools, to make and track changes to models on database tables. `pip 
    install alembic`. Read docs @ https://alembic.sqlalchemy.org/en/latest/tutorial.html 
16. Initialize alembic and also create a directory called alembic (or any use any name): `alembic init alembic` 
17. Go to the alembic folder, then to env.py and import Base from app.models.
18. Then save/set the target_metadata to Base.metadata: `target_metadata = Base.metadata` 
19. Under the `config = context.config`, set a new main option to override the variable `sqlalchemy.url` inorder to 
    use the env variables earlier defined in database.py for SQLALCHEMY_URL.
    `config.set_main_option("sqlalchemy.url", f"postgresql+psycopg2://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}")"` 
    Remember to first import settings from app.config, then define the variables past into the f string. This will help us avoid hard-coding the env variable values into the sqlalchemy url.
20. Go to the alembic.ini file, then go to line 58, remove the value for `sqlalchemy.url`. 
21. Use on the terminal, alembic revision -m to track the changes  like a commit in git.
22. Create a Migration Script by creating an alembic revision: `alembic revision -m "create posts table"`
23. Go to the version folder and click on the new revision just created and edit the `def upgrade` and `def downgrade`.
24. On the `def upgrade` function, write the code to perform actions on the database. Then on the `def downgrade` function, write the code to undo it.
25. 
 