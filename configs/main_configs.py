import os
from Enums import AppEnv
from dotenv import load_dotenv

load_dotenv() # Load environment variables
class MainConfigs:
    env = os.getenv("APP_ENV", AppEnv.DEV)  # default to 'dev' if not set
    api_key = None
    
    @classmethod
    def get_run_config(cls):
        """Get the run config for the app"""
       
        if cls.env == AppEnv.PROD.value:
            return {
                "host": "0.0.0.0",
                "port": 8000,
                "reload": False,
                "workers": 4,
            }
        else:
            return {
                "host": "127.0.0.1",
                "port": 8000,
                "reload": True,
            }
    
    @classmethod
    def get_api_key(cls):
        """Get the API key from the environment variables"""
        if cls.env == AppEnv.PROD.value and cls.api_key is None:           
            cls.api_key = os.getenv("GEDLT_MASXAI_PROD_KEY")         
        return cls.api_key
