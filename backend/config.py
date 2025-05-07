import os

class Settings:
    """Configurações da aplicação."""

    DATABASE_URL_FONTE = os.environ.get("DATABASE_URL")
    TARGET_DATABASE_URL_ALVO = os.environ.get("TARGET_DATABASE_URL")

    API_VERSION = "v1"
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

settings = Settings()