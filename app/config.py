import os


class Settings:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
    jwt_secret = os.getenv("JWT_SECRET", "dev-secret-change-me-please-32bytes!!")
    jwt_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    ocr_engine = os.getenv("OCR_ENGINE", "gemini")  # gemini | mock
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    upload_dir = os.getenv("UPLOAD_DIR", "./data/uploads")
