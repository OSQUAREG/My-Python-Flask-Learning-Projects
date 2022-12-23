1. Create the Project Folder
2. Check the python version is version 3:
    `$ py -3 --version`
2. Create your virtual environment venv: 
`py -3 -m venv venv`
3. Activate your venv: `venv/Scripts/activate`
4. Install Fast API package: `pip install fastapi[all]`
5. Install uvicorn to work as the server that runs the code: `pip install uvicorn[standard]`
6. Install the Postgres driver for db, psycopg2: `pip install psycopg2`
7. Install the ORM SQLAlchemy: `pip install sqlalchemy`
8. Then create `main.py` file and start coding.
9. Start your server using: `uvicorn main:app` This will run the code in your localhost without updating the changes 
   you make to the code. Usually for production. 
10. However, you can use `uvicorn main:app --reload` to continually update your code to the server as you make 
   changes to the code. Good for development.
Note: `main` is the `main.py` file name and app is the `app` initialized in the `main.py` file 
11. Or if its in a package folder e.g folder name: app, `uvicorn app.main:app`
12. Also install passlib library for hashing the user's password before saving it in the DB: `pip install passlib[bcrypt]` 
13. Install python-jose[cryptography] to create JWT Tokens for user authentications: `pip install python-jose[cryptography]`
 