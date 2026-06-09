from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    firebase_project_id: str = "ogrodzenia-wielkopolska"
    google_application_credentials: str = "./serviceAccountKey.json"
    firebase_service_account_json: str | None = None
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    port: int = 8000

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
