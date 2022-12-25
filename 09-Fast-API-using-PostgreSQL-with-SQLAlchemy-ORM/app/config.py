from pydantic import BaseSettings


# Setting System Environment Variables:
# NB: Sys. Env. Variables are usually capitalized, however Pydantic can also capitalize them whenever they are not.
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # importing the environment variables from the .env file
    class Config:
        env_file = ".env"


settings = Settings()