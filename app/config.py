from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DATABASE_URL: str

    BOT_TOKEN: str
    BASE_SITE: str
    WEBHOOK_URL:str
    ADMIN_ID: int


    @model_validator(mode="before")
    def prepare(cls, values):
        values["DATABASE_URL"] = (f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}"
                                  f"@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}")
        values["WEBHOOK_URL"] = f"{values['BASE_SITE']}/webhook"
        return values

    # @model_validator(mode="before")
    # def get_webhook_url(cls, values):
    #     values["WEBHOOK_URL"] = f"{values['BASE_SITE']}/webhook"
    #     return values

    class Config:
        env_file = '.env'


settings = Settings()
