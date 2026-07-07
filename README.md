# Export-Data-from-BD
Projeto em Python para conectar em uma base Oracle, consultar dados da tabela PCPRODUT, exportar os registros em formato JSON, compactar o arquivo em ZIP e enviar automaticamente por email.

Funcionalidades
Conexão com banco Oracle usando oracledb
Consulta de produtos na tabela PCPRODUT
Exportação dos dados para arquivo .json
Compactação automática em .zip
Envio do arquivo por email via SMTP
Geração de log da execução
Tecnologias utilizadas
Python 3
OracleDB
JSON
SMTP
ZIP
EmailMessage
Instalação

Clone o repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git

Acesse a pasta do projeto:

cd seu-repositorio

Instale a dependência necessária:

pip install oracledb
Configuração

Antes de executar o script, altere as informações abaixo no código:

PASTA_DESTINO = r"C:\Users\pedro.ivo\Desktop\Projeto"

EMAIL_REMETENTE = "seu_email@email.com"
EMAIL_SENHA = "sua_senha_ou_senha_de_app"
EMAIL_DESTINO = "email_destino@email.com"

SMTP_SERVIDOR = "smtp.seuprovedor.com"
SMTP_PORTA = 465

Também configure os dados de conexão Oracle:

dsn = """
(DESCRIPTION =
 (ADDRESS_LIST =
   (ADDRESS = (PROTOCOL = TCP)(HOST = YOUR IP)(PORT = YOUR PORT))
 )
 (CONNECT_DATA =
   (SERVICE_NAME = YOUR SERVICE LINK)
 )
)
"""

E informe o usuário e senha do banco:

conn = oracledb.connect(
    user="seu_usuario",
    password="sua_senha",
    dsn=dsn
)
Consulta SQL

O script realiza uma consulta na tabela PCPRODUT, retornando informações como:

Código do produto
Informações técnicas
Código da marca
Descrição
Código auxiliar
NBM
Percentual de IPI de venda

Exemplo:

SELECT 
    CODPROD,
    INFORMACOESTECNICAS,
    CODMARCA,
    DESCRICAO,
    CODAUXILIAR,
    NBM,
    PERCIPIVENDA
FROM PCPRODUT;
Como executar

Execute o arquivo Python:

python exportador_pcprodut.py

Ao finalizar, o sistema irá:

Conectar ao banco Oracle
Exportar os dados para JSON
Compactar o JSON em ZIP
Remover o JSON original
Enviar o ZIP por email
Registrar tudo no arquivo exportacao.log
Exemplo de saída

Arquivos gerados na pasta configurada:

pcprodut_20260707_143000.zip
exportacao.log
Log

O arquivo exportacao.log registra as principais etapas do processo:

2026-07-07 14:30:00 - Conectando ao Oracle...
2026-07-07 14:30:05 - 1500 produtos exportados
2026-07-07 14:30:06 - Gerando JSON...
2026-07-07 14:30:07 - Compactando arquivo...
2026-07-07 14:30:08 - Email enviado com sucesso
Atenção

Não envie para o GitHub dados sensíveis como:

Usuário do banco
Senha do banco
IP do servidor
Service Name
Email e senha
Porta SMTP interna

O ideal é armazenar essas informações em variáveis de ambiente ou em um arquivo .env, mantendo esse arquivo fora do versionamento.
