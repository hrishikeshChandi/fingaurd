import os
from getpass import getpass
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    app_name: str = "FinGuard"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        os.environ["GROQ_API_KEY"] = getpass("Enter your GROQ API key: ")
        groq_api_key = os.getenv("GROQ_API_KEY")

    # Risk thresholds
    concentration_threshold: float = float(os.getenv("CONCENTRATION_THRESHOLD", 0.5))
    sharpe_threshold: float = float(os.getenv("SHARPE_THRESHOLD", 1.0))
    drawdown_threshold: float = float(os.getenv("DRAWDOWN_THRESHOLD", -0.3))
    volatility_threshold: float = float(os.getenv("VOLATILITY_THRESHOLD", 0.3))


settings = Settings()
