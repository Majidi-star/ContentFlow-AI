# ContentFlow AI: Automated Content Harvesting & Management System 🚀

[English](#english) | [فارسی](#persian)

---

<a name="english"></a>
## 🌍 English Description

**ContentFlow AI** is a professional-grade automated pipeline designed to bridge the gap between web data and content generation. This system features a high-performance web scraper and a robust management API, allowing for seamless integration into automation platforms like **n8n**.

### ✨ Key Features
* **Advanced Scraping:** Multi-selector support for complex websites (e.g., Zoomit) using Selenium (Headless mode).
* **Intelligent Cleaning:** Uses BeautifulSoup4 to strip unwanted HTML tags, delivering pure, noise-free content.
* **RESTful API:** A Flask-based backend to retrieve the latest scraped content and manage files securely.
* **Duplicate Prevention:** Built-in history tracking to avoid scraping the same URL twice.
* **n8n Integration Ready:** Designed to work as a source for AI translation agents and auto-publishing workflows.

### 🛠 Tech Stack
* **Language:** Python 3.x
* **Web Automation:** Selenium & ChromeDriver
* **Processing:** BeautifulSoup4
* **Backend:** Flask API
* **Workflow:** n8n (External Integration)

### 🤖 n8n Workflow Integration
This project is part of a larger ecosystem. While the core scripts handle data acquisition, an **n8n workflow** (shown below) connects to the API to:
1.  Fetch the latest technology news.
2.  Translate content using AI models (GPT/Llama).
3.  Generate SEO-optimized social media posts or articles.
*(Note: n8n JSON is excluded for security reasons).*

<img width="1673" height="591" alt="n8n screenshot" src="https://github.com/user-attachments/assets/987c1ede-0a25-4308-b762-74fef60edbd2" />

---

<a name="persian"></a>
## 🇮🇷 توضیحات فارسی

**سیستم هوشمند ContentFlow AI** یک خط لوله (Pipeline) خودکار برای استخراج هوشمند محتوا از وب و مدیریت آن است. این پروژه با هدف حذف عملیات دستی در جمع‌آوری اخبار و تبدیل آن به محتوای قابل استفاده در شبکه‌های اجتماعی یا وب‌سایت‌ها طراحی شده است.

### ✨ قابلیت‌های کلیدی
* **اسکرپر پیشرفته:** قابلیت عبور از ساختارهای پیچیده وب‌سایت‌ها با Selenium در حالت Headless.
* **پاکسازی هوشمند محتوا:** استفاده از BeautifulSoup4 برای حذف کدهای زائد HTML و ارائه متن خالص.
* **مدیریت از طریق API:** بهره‌گیری از Flask برای ایجاد دسترسی به جدیدترین فایل‌ها و مدیریت حافظه.
* **جلوگیری از محتوای تکراری:** دارای سیستم تاریخچه‌گیری (History Tracking) داخلی.
* **آماده اتصال به n8n:** بهینه‌سازی شده برای نقش "منبع داده" در ورودی اتوماسیون‌های هوش مصنوعی.

### 🤖 یکپارچگی با n8n (ترجمه و تولید محتوا)
این نرم‌افزار به گونه‌ای طراحی شده که به یک **Workflow در n8n** متصل شود. روند کار به این صورت است:
۱. سیستم داده‌ها را از وب‌سایت‌های مرجع (مثل زومیت) جمع‌آوری می‌کند.
۲. اتوماسیون n8n محتوا را از طریق API دریافت می‌کند.
۳. محتوا توسط مدل‌های هوش مصنوعی ترجمه و به پست‌های شبکه‌ای یا مقالات سئو شده تبدیل می‌شود.

---

## 🚀 Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ContentFlow-AI.git](https://github.com/YOUR_USERNAME/ContentFlow-AI.git)
