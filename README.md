# DIVWordPress
API Divloopers para manuseio de dados wordpress.


## Instalação
Prepare o ambiente virtual python.
```shell
python3 -m venv venv;
source venv/bin/activate;
pip3 install --upgrade pip
pip3 install -r requirements.txt
```
Em seguida, crie o arquivo: `.env`.

```dotenv
################
# AMBIENTE DEV #
################

in_production = False
in_testing = True

# Base de dados
database__port = 3060
database__connect_timeout = 150000
database__minconn = 0
database__maxconn = 20
database__models_schema = ''
database__needed = False
database__engine = 'mysql+pymysql://user:pass@host/database'
```

