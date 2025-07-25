# GFSC Scam Tracker

A Django web application for scraping and tracking bogus banks from the GFSC website.

---

## Features

- Scrapes and stores scam/bogus bank data from the GFSC site
- Tracks new and removed items
- Responsive, paginated tables
- User authentication (login required)
- Email notifications on changes
- Scheduled scraping support

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Foysal1327/gfsc-scam-tracker.git
cd gfsc-scam-tracker
```

### 2. Set up a virtual environment

```bash
python -m venv myvenv
source myvenv\Scripts\activate  # On Windows
# or
source myvenv/bin/activate      # On Linux/macOS
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

- Create a MySQL database named `web_scraper_db`.
- Import the schema:
- make sure your mariaDb version updated to 10.5 or more
- Update `gfsc_scraper/settings.py` with your MySQL credentials.

```bash
mysql -u root -p web_scraper_db < schema.sql
```

### 5. Run migrations and create a superuser

```bash
cd gfsc_scraper
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

## Deployment

- Use [Gunicorn](https://gunicorn.org/) or [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) for production.
- Use [Nginx](https://nginx.org/) or [Apache](https://httpd.apache.org/) as a reverse proxy.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `settings.py`.
- Set up static files:

```bash
python manage.py collectstatic
```

- Set up a process manager (e.g., [supervisor](http://supervisord.org/)) to keep your app running.
---

## Deployment on a Linux Server

### 1. System Preparation

- Update your system:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- Install Python, pip, and venv:
  ```bash
  sudo apt install python3 python3-pip python3-venv -y
  ```
- Install MariaDB (or MySQL) and required libraries:
  ```bash
  sudo apt install mariadb-server libmariadb-dev -y
  # Or for MySQL:
  # sudo apt install mysql-server libmysqlclient-dev -y
  ```
- (Optional) Secure your MariaDB installation:
  ```bash
  sudo mysql_secure_installation
  ```

### 2. Database Setup

- Log in to MariaDB and create the database and user:
  ```bash
  sudo mysql -u root -p
  CREATE DATABASE web_scraper_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  CREATE USER 'youruser'@'localhost' IDENTIFIED BY 'yourpassword';
  GRANT ALL PRIVILEGES ON web_scraper_db.* TO 'youruser'@'localhost';
  FLUSH PRIVILEGES;
  EXIT;
  ```
- Import the schema:
  ```bash
  mysql -u youruser -p web_scraper_db < schema.sql
  ```

### 3. Project Setup

- Clone your project and set up the environment:
  ```bash
  git clone https://github.com/Foysal1327/gfsc-scam-tracker.git
  cd gfsc-scam-tracker
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Update `gfsc_scraper/settings.py` with your database credentials.

### 4. Django Setup

- Run migrations and create a superuser:
  ```bash
  cd gfsc_scraper
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py collectstatic
  ```

### 5. Gunicorn Setup (as a systemd service)

- Install Gunicorn:
  ```bash
  pip install gunicorn
  ```
- Create a Gunicorn systemd service file `/etc/systemd/system/gfsc-scam-tracker.service`:
  ```ini
  [Unit]
  Description=Gunicorn instance to serve GFSC Scam Tracker
  After=network.target

  [Service]
  User=yourusername
  Group=www-data
  WorkingDirectory=/path/to/gfsc-scam-tracker/gfsc_scraper
  Environment="PATH=/path/to/gfsc-scam-tracker/venv/bin"
  ExecStart=/path/to/gfsc-scam-tracker/venv/bin/gunicorn --workers 3 --bind unix:/path/to/gfsc-scam-tracker/gfsc_scraper.sock gfsc_scraper.wsgi:application

  [Install]
  WantedBy=multi-user.target
  ```
- Reload systemd and start Gunicorn:
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl start gfsc-scam-tracker
  sudo systemctl enable gfsc-scam-tracker
  ```

### 6. Nginx Setup

- Install Nginx:
  ```bash
  sudo apt install nginx -y
  ```
- Create an Nginx config `/etc/nginx/sites-available/gfsc-scam-tracker`:
  ```nginx
  server {
      listen 80;
      server_name your_domain_or_ip;

      location = /favicon.ico { access_log off; log_not_found off; }
      location /static/ {
          root /path/to/gfsc-scam-tracker/gfsc_scraper;
      }
      location /media/ {
          root /path/to/gfsc-scam-tracker/gfsc_scraper;
      }
      location / {
          include proxy_params;
          proxy_pass http://unix:/path/to/gfsc-scam-tracker/gfsc_scraper.sock;
      }
  }
  ```
- Enable the config and restart Nginx:
  ```bash
  sudo ln -s /etc/nginx/sites-available/gfsc-scam-tracker /etc/nginx/sites-enabled
  sudo nginx -t
  sudo systemctl restart nginx
  ```

### 7. Security & Environment

- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `settings.py`.
- Use environment variables or a `.env` file for secrets (see [django-environ](https://django-environ.readthedocs.io/en/latest/)).
- Set up HTTPS with [Let's Encrypt](https://certbot.eff.org/) (recommended).

### 8. Process Management

- Gunicorn is managed by systemd (see above).
- For scheduled scraping, use `cron` as described earlier.

---

## How the Scraper Works

- The scraper fetches the GFSC bogus banks page, parses the HTML table, and extracts relevant data.
- Data is cleaned and normalized before being stored in the database.
- On each run, new and removed items are detected by comparing with existing records.

## How the Refresh Button Works

- The refresh button triggers an AJAX (HTMX) request to the backend.
- The backend re-scrapes the data, updates the database, and returns updated tables (current, new, removed items) without reloading the page.

## How Differences Are Displayed

- **New items**: Displayed in the "New Items" table.
- **Removed items**: Displayed in the "Removed Items" table.
- **Current items**: Displayed in the main table with pagination.

## How Authentication Is Enforced

- All main views are decorated with `@login_required`.
- Users must log in to access the dashboard and data.

## How to Set Up Scheduled Scraping

### On Linux/macOS (cron):

Edit your crontab:

```bash
crontab -e
```

Add a line (every hour):

```
0 * * * * /path/to/venv/bin/python /path/to/manage.py scrape_data
```

### On Windows (Task Scheduler):

- Create a new task.
- Set the action to run:
  ```
  your_path\web_scrapper_test\myvenv\Scripts\python.exe your_path\web_scrapper_test\gfsc_scraper\manage.py scrape_data
  ```
- Set your desired schedule.

---

## email sample
- Update `gfsc_scraper/settings.py` with your SMTP credentials.

<img width="517" alt="image" src="https://github.com/user-attachments/assets/e5dbcda4-fdc9-49fd-9ad9-0d5262a5f80d" />

## License

MIT
