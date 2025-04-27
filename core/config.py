from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str

    MYSQL_DATABASE: str
    MYSQLUSER: str
    MYSQL_ROOT_PASSWORD: str
    MYSQLHOST: str
    MYSQLPORT: int = 3306

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"mysql://root:MtNOApKlxniyUHTJwbOBuHKsTfIdMgnB@yamabiko.proxy.rlwy.net:52822/railway"
        # return f"mysql+pymysql://{self.MYSQLUSER}:{self.MYSQL_ROOT_PASSWORD}@{self.MYSQLHOST}:{self.MYSQLPORT}/{self.MYSQL_DATABASE}"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
