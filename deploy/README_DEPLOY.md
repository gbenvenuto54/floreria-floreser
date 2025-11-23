# Despliegue en Ubuntu 22.04 (Gunicorn + Nginx)

Requisitos
- Ubuntu 22.04 LTS
- Python 3.11, pip, venv
- MySQL 8 (con usuario/BD creados)
- Nginx

1) Clonar y preparar entorno
```
sudo apt update && sudo apt install -y python3.11-venv python3.11 python3-pip mysql-client nginx
cd /opt
sudo mkdir floreria-floreser && sudo chown $USER:$USER floreria-floreser
cd floreria-floreser
# Copiar archivos del proyecto aquí (o git clone)
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
cp .env.example .env  # editar variables reales
python manage.py collectstatic --noinput
python manage.py migrate
```

2) Servicio systemd (Gunicorn)
- Edita rutas absolutas en deploy/gunicorn.service según tu ubicación.
```
sudo cp deploy/gunicorn.service /etc/systemd/system/floreria-gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable floreria-gunicorn
sudo systemctl start floreria-gunicorn
sudo systemctl status floreria-gunicorn
```

3) Nginx (proxy + estáticos)
- Edita `server_name` y rutas de `staticfiles`/`media`.
```
sudo cp deploy/nginx.conf /etc/nginx/sites-available/floreria
sudo ln -s /etc/nginx/sites-available/floreria /etc/nginx/sites-enabled/floreria
sudo nginx -t
sudo systemctl restart nginx
```

4) Firewall (opcional)
```
sudo ufw allow 'Nginx Full'
```

5) Backup MySQL diario (cron)
- Edita credenciales en script.
```
sudo cp deploy/backup_mysql.sh /usr/local/bin/backup_floreria.sh
sudo chmod +x /usr/local/bin/backup_floreria.sh
(crontab -l; echo "0 3 * * * /usr/local/bin/backup_floreria.sh") | crontab -
```

Troubleshooting
- Revisa `journalctl -u floreria-gunicorn -f` para logs.
- Permisos de carpeta `/opt/floreria-floreser` deben permitir lectura a usuario de servicio.
- Si usas SSL, configura certbot/Let's Encrypt en Nginx.
