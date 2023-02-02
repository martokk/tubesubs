from sqlmodel import SQLModel


class Alerts(SQLModel):
    primary: list[str] = []
    secondary: list[str] = []
    success: list[str] = []
    danger: list[str] = []
    warning: list[str] = []
    info: list[str] = []
    light: list[str] = []
    dark: list[str] = []
