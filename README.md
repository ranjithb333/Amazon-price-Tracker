# 🛒 Amazon Price Tracker

A Flask web application that tracks prices of Amazon products.  
It scrapes product data directly from Amazon and stores price history in a **MySQL** database, allowing users to view trends over time.

---

## 🚀 Features
- 🔍 Scrape real-time prices from Amazon product pages  
- 💾 Store product and price history in MySQL  
- 📈 View historical price trends  
- ⏰ Schedule automatic price checks (using cron or Celery)  
- 🌐 Simple Flask web UI to add and monitor products  

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)  
- **Database:** MySQL  
- **Scraping:** Requests + BeautifulSoup (or lxml)  
- **Frontend:** Jinja2 templates + Bootstrap  
- **Optional:** APScheduler / Celery for periodic tasks  

---

