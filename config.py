from pydantic_settings import BaseSettings

class Setting(BaseSettings): 
    email: str
    password: str
    db_name: str
    db_username: str
    db_password: str
    
    class Config: 
        env_file = ".env"
        
setting = Setting()