from pydantic_settings import BaseSettings

class Setting(BaseSettings): 
    email: str
    password: str
    
    class Config: 
        env_file = ".env"
        
setting = Setting()