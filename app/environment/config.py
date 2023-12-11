from pydantic_settings import BaseSettings

# Define a Settings class that inherits from BaseSettings and specifies configuration parameters
class Settings(BaseSettings):
    # Database connection parameters
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    
    # Security-related parameters
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Configuration settings for loading environment variables from a file
    class Config:
        env_file = ".env"

# Create an instance of the Settings class to store and access configuration settings
settings = Settings()