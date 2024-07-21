import psycopg2
from sqlmodel import SQLModel, Field, create_engine, Session


# Definição do modelo de dados
class Oportunidade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    texto: str
    url: str
    regiao: str | None = Field(default=None)
