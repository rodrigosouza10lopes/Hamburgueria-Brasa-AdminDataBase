import streamlit as st
import pandas as pd
import re
from sqlalchemy import create_engine, text 
from urllib.parse import quote_plus

SERVIDOR =  r"brasa-rodrigo.database.windows.net"
BANCO = "HamburgueriaBrasa"
DRIVER = "ODBC Driver 18 for SQL Server"

#OUTRO MÉTODO LOGIN
#SUARIO = "sa"
#SENHA = "Senai@134"

def ler_segredo():
    try:
        return st.secrets["banco"]
    except Exception:
        return None
    


@st.cache_resource
def conectar():
    # Autentificação via windows utilizando ODBC
    banco = ler_segredo()
    print(banco)
    if banco :
        odbc = ( 
            f"DRIVER={'ODBC Driver 17 for SQL Server'};SERVER={banco['servidor']};DATABASE={banco['nome']};"
            f"UID={banco['usuario']};PWD={banco['senha']};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60"
            )
        print(odbc)
    else: # SQL Server local, autentificação do windons
       odbc = ( 
           f"DRIVER={{{DRIVER}}};SERVER={SERVIDOR};DATABASE={BANCO};"
           "Trusted_Connection=yes;TrustServerCertificate=yes"
       )

    return create_engine("mssql+pyodbc:///?odbc_connect="+ quote_plus(odbc), pool_pre_ping=True)


def consultar(sql):
    with conectar().connect() as conexao:
        return pd.read_sql(text(sql), conexao) 


def mensagem_erro(erro):
    """Tira só a mensagem do SQL Server do meio do texto do erro."""
    achou = re.search(r"\[SQL Server\](.+?)\s*\(\d+\)", str(erro))
    return achou.group(1) if achou else str(erro)