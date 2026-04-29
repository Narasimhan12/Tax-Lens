from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Tax Lens API"
    environment: str = "dev"
    api_prefix: str = "/api/v1"

    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_deployment: str

    mongodb_uri: str
    mongodb_db_name: str = "taxlens"

    dataset_path: str = "backend/data/companies.csv"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
