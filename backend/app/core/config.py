from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_env: str = "development"
    secret_key: str

    # Database
    database_url: str

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # Stripe
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str

    # Daily.co
    daily_api_key: str
    daily_api_url: str = "https://api.daily.co/v1"

    # Resend
    resend_api_key: str
    resend_from_email: str = "onboarding@resend.dev"

    # Email
    teacher_email: str

    # Currency
    payment_currency: str = "usd"


settings = Settings()