from pydantic import BaseModel


class Browser(BaseModel):
    base_url: str
    login: str
    password: str


class Cms(BaseModel):
    cms_url: str
    cms_login: str
    cms_password: str
    cms_sys_login: str
    cms_sys_password: str


class Telegram(BaseModel):
    bot_url: str
    token: str
    chat_id: str


class Converter(BaseModel):
    cms: Cms
    telegram: Telegram
    browser: Browser
