import oracledb
import json
import smtplib
import zipfile
from email.message import EmailMessage
from datetime import datetime
import os

PASTA_DESTINO = r"C:\Users\"

EMAIL_REMETENTE = " "
EMAIL_SENHA = " "
EMAIL_DESTINO = " "

SMTP_SERVIDOR = " "
SMTP_PORTA = 

if not os.path.exists(PASTA_DESTINO):
    os.makedirs(PASTA_DESTINO)

log_file = os.path.join(PASTA_DESTINO, "exportacao.log")

def log(msg):
    linha = f"{datetime.now()} - {msg}"
    print(linha)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

arquivo_json = os.path.join(PASTA_DESTINO, f"pcprodut_{timestamp}.json")
arquivo_zip = os.path.join(PASTA_DESTINO, f"pcprodut_{timestamp}.zip")

dsn = """
(DESCRIPTION =
 (ADDRESS_LIST =
   (ADDRESS = (PROTOCOL = TCP)(HOST = )(PORT = ))
 )
 (CONNECT_DATA =
   (SERVICE_NAME = )
 )
)
"""

log("Conectando ao Oracle...")

conn = oracledb.connect(
    user=" ",
    password="",
    dsn=dsn
)

cursor = conn.cursor()

query = """
SELECT CODPROD,
        INFORMACOESTECNICAS,
        CODMARCA,
        DESCRICAO,
       CODAUXILIAR,
       NBM,
       PERCIPIVENDA
FROM PCPRODUT; 

SELECT CODFILIAL,
        CODPROD,
        QTBLOQUEADA,
        

"""

cursor.execute(query)

colunas = [col[0] for col in cursor.description]

dados = []

for row in cursor:

    registro = {}

    for i, valor in enumerate(row):

        if hasattr(valor, "read"):
            valor = valor.read()

        if valor is None:
            valor = ""

        registro[colunas[i]] = str(valor)

    dados.append(registro)

log(f"{len(dados)} produtos exportados")

cursor.close()
conn.close()

# =========================
# GERAR JSON
# =========================

log("Gerando JSON...")

with open(arquivo_json, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)

# =========================
# COMPACTAR ZIP
# =========================

log("Compactando arquivo...")

with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(arquivo_json, os.path.basename(arquivo_json))

os.remove(arquivo_json)

log(f"Arquivo ZIP criado: {arquivo_zip}")

# =========================
# ENVIAR EMAIL
# =========================

log("Enviando email...")

msg = EmailMessage()
msg["Subject"] = "Exportação completa PCPRODUT"
msg["From"] = " "
msg["To"] = " "

msg.set_content("Segue arquivo ZIP com todos os produtos da tabela PCPRODUT.")

with open(arquivo_zip, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="zip",
        filename=os.path.basename(arquivo_zip)
    )

with smtplib.SMTP_SSL(SMTP_SERVIDOR, SMTP_PORTA) as smtp:
    smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
    smtp.send_message(msg)

log("Email enviado com sucesso")