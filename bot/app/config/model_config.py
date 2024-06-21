from pydantic import BaseModel, SecretStr


class AppConfigModel(BaseModel):
    major_version: int
    minor_version: int
    patch_version: int
    locale_dir: str


class DetectModelConfigModel(BaseModel):
    path: str


class PredictModelConfigModel(BaseModel):
    path: str


class BotConfigModel(BaseModel):
    telegram_token: SecretStr
    owner_username: str
    webhook_url: str


class PostgresConfigModel(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str


class RedisConfigModel(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    db: int


class YandexDiskConfigModel(BaseModel):
    api_key: SecretStr
    base_dir: str


class ServerConfigModel(BaseModel):
    debug: bool
    port: int


class ConfigModel(BaseModel):
    application: AppConfigModel
    bot: BotConfigModel
    detect_model: DetectModelConfigModel
    predict_model: PredictModelConfigModel
    postgres: PostgresConfigModel
    redis: RedisConfigModel
    yandex_disk: YandexDiskConfigModel
    server: ServerConfigModel
