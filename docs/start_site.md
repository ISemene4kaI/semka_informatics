# Nginx настройка и использование

## План действий

- [ ] Установить пакеты
- [ ] Клонировать репозиторий
- [ ] Запустить серверную часть сайта
- [ ] Запустить Nginx
- [ ] Дополнительные настройки системы

## Установка пакетов
Для начала проверяем версию apt, подгружаем нужные пакеты.
```bash
sudo apt update
sudo apt install -y nginx git
```

Далее проверяем версии, что пакеты установлены и у нас актуальные версии
```bash
nginx -v
docker --version
docker compose version
```

## Клонирование проекта
Для начала выбираем нужную директорию, куда будем клонировать наш репозиторий.
К примеру это директория может называться Projects, Github, Gitlab (как угодно, главное что вы знаете)

Клонируем репозиторий, т.к. он публичный сделать это легко

```bash
cd /projects
sudo git clone https://github.com/ISemene4kaI/semka_informatics.git
cd semka_informatics
```

Папка и ссылка на репозиторий может быть как вам удобно. Всё зависит от проекта, в этом мы делаем так.

## Запуск серверной части приложения

> [!NOTE]
> Если docker не скачан, его можно установить по инструкции из [файла](https://github.com/ISemene4kaI/semka_informatics/blob/main/docs/install_docker.md)

Запускаем серверную часть, если нужны будут права root пишем перед этим sudo
```bash
docker compose up -d --build
```

Проверка контейнеров
```bash
docker compose ps
```

Проверяем что вернет backend (серверная часть) по запросу
```bash
curl http://127.0.0.1:5000
```

## Запуск Nginx

Будем всё делать в обычной для nginx директории
```bash
sudo nano /etc/nginx/sites-available/semka_informatics
```

Создаем конфиг Nginx в редакторе который открылся
```
server {
    listen 80;
    listen [::]:80;
    server_name твойдомен.ru www.твойдомен.ru;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

После этого включаем сайт, посл этого убрав дефолтный и начинаем работу с сертификатами.
```bash
sudo ln -s /etc/nginx/sites-available/isemene4kai.ru /etc/nginx/sites-enabled/isemene4kai.ru
sudo rm -f /etc/nginx/sites-enabled/default
sudo mkdir -p /var/www/certbot
sudo chown -R www-data:www-data /var/www/certbot
```

Проверка конфига
```bash
sudo nginx -t
sudo systemctl restart nginx
```

Проверяем работу http
```bash
curl -I http://isemene4kai.ru
curl -I http://www.isemene4kai.ru
```

Делаем тесты домена и возможности работы с сертификатами
```bash
sudo mkdir -p /var/www/certbot/.well-known/acme-challenge
echo test-ok | sudo tee /var/www/certbot/.well-known/acme-challenge/test
curl http://isemene4kai.ru/.well-known/acme-challenge/test
curl http://www.isemene4kai.ru/.well-known/acme-challenge/test
```

Выпускаем сертификаты без привязки к nginx
```bash
sudo certbot certonly --webroot -w /var/www/certbot -d isemene4kai.ru -d www.isemene4kai.ru
```

Далее меняем стартовый конфиг на новый
```bash
sudo nano /etc/nginx/sites-available/isemene4kai.ru
```
```
server {
    listen 80;
    listen [::]:80;
    server_name isemene4kai.ru www.isemene4kai.ru;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name isemene4kai.ru www.isemene4kai.ru;

    ssl_certificate /etc/letsencrypt/live/isemene4kai.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/isemene4kai.ru/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=15552000" always;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_redirect off;
    }
}
```

При правильной работе DNS и прочих сервисов всё должно запуститься

## Дополнительные настройки системы
Если используете UFW firewall на сервере
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

> [!WARNING]
> Если для вашего приложения нужные еще порты через которые он будет связываться, добавьте их.

## Финал

Вот так мы поставили наш простенький сайт на Nginx, если будут какие либо ошибки, то можно открывать issue или дисскусии.
