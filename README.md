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
git clone https://github.com/yourusername/gfsc-scam-tracker.git
cd gfsc-scam-tracker
```

### 2. Set up a virtual environment

```bash
python -m venv myvenv
source myvenv/Scripts/activate  # On Windows
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

```bash
mysql -u root -p web_scraper_db < schema.sql
```

- Update `gfsc_scraper/settings.py` with your MySQL credentials.

### 5. Run migrations and create a superuser

```bash
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
<img width="517" alt="image" src="https://github.com/user-attachments/assets/e5dbcda4-fdc9-49fd-9ad9-0d5262a5f80d" />

## License

MIT 
