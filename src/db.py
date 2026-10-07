import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text 
from urllib.parse import quote_plus

SERVIDOR =  r"D02S22-1252888\SQLEXPRESS"
BANCO = "HamburgueriaBrasa"
DRIVER = "ODBC Driver 18 for SQL server"

#OUTRO MÉTODO LOGIN
USUARIO = "sa"
SENHA = "Senai@134"



def conectar():
    # Autentificação via windows utilizando ODBC

    odbc = ( 
        f"DRIVER={{{DRIVER}}};SERVER={SERVIDOR};DATABASE={BANCO};"
        f"UID={USUARIO};PWD={SENHA};"
        "TrustServerCertificate=yes"
    )

    return create_engine("mssql+pyodbc:///?odbc_connect="+ quote_plus(odbc))

def consultar(sql):
    with conectar().connect() as conexao:
        return pd.read_sql(text(sql), conexao) 


def mensagem_erro(erro):
    """Tira só a mensagem do SQL Server do meio do texto do erro."""
    achou = re.search(r"\[SQL Server\](.+?)\s*\(\d+\)", str(erro))
    return achou.group(1) if achou else str(erro)