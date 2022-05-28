#!/bin/bash
protocol="$1"

if [ -f ".env" ]; then
    echo ".env exists."
    vars=$(grep -v '^#' .env)
    eval "${vars}"
    echo "${WSGI_HOST} : ${WSGI_PORT}"

else
    echo ".env does not exist."
    exit 1
fi

if [[ -z "${protocol// }" ]]
    then
        protocol="http"
fi

date_base=$(date "+%Y%m%d%H%M%S")
path_base=$PWD
name_base=$(basename "$PWD")
name_wsgi="api.wsgi.${name_base}.service"
path_install=".install/${date_base}"
name_nginx="${name_base}.${protocol}.conf"

echo "Inicializando instalação ${name_base} como ${protocol}"

echo ATUALIZANDO SERVIDOR
apt update && apt upgrade -y

echo INSTALANDO SERVIÇOS
apt install nginx python3-venv python3-certbot-nginx -y

#chown -R www-data:www-data .

mkdir log
mkdir -p "${path_install}"

python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
deactivate

echo INSTALANDO SERVICOS E CONFIGURACOES UNIX
systemctl disable "${name_wsgi}"

cp "$(pwd)/srv/conf/nginx.${protocol}.conf" "${path_install}"
cp "$(pwd)/srv/services/api.wsgi.service" "${path_install}/${name_wsgi}"

sed -i "s,APP_BASE_PATH,$PWD,gi" "${path_install}/${name_wsgi}"
sed -i "s,APP_BASE_NAME,${name_base},gi" "${path_install}/${name_wsgi}"
sed -i "s,WSGI_PORT,${WSGI_PORT},gi" "${path_install}/${name_wsgi}"
sed -i "s,WSGI_HOST,${WSGI_HOST},gi" "${path_install}/${name_wsgi}"
sed -i "s,WSGI_PORT,${WSGI_PORT},gi" "${path_install}/nginx.${protocol}.conf"
sed -i "s,WSGI_HOST,${WSGI_HOST},gi" "${path_install}/nginx.${protocol}.conf"
sed -i "s,NGINX_PORT,${NGINX_PORT},gi" "${path_install}/nginx.${protocol}.conf"
sed -i "s,NGINX_DOMAIN,${NGINX_DOMAIN},gi" "${path_install}/nginx.${protocol}.conf"

ln -sf "$(pwd)/${path_install}/${name_wsgi}" "/etc/systemd/system"
ln -sf "$(pwd)/${path_install}/nginx.${protocol}.conf" "/etc/nginx/sites-available/${name_nginx}"
ln -sf "/etc/nginx/sites-available/${name_nginx}" /etc/nginx/sites-enabled/

chmod -R 755 "${path_install}"

systemctl daemon-reload
systemctl enable "${name_wsgi}"
systemctl restart "${name_wsgi}"
systemctl stop nginx
systemctl start nginx

journalctl -f -u "${name_wsgi}"