# Prague Club of Investors - Analyst Performance Tracker

[![Flask](https://img.shields.io/badge/Flask-2.3.3-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Internal-orange.svg)]()

A **production-grade** web application for tracking and comparing investment analyst performance at the Prague Club of Investors (Klub Investorů). Built with Flask, SQLAlchemy, and modern web technologies.

> 🚀 **New to this project?** Start with [QUICKSTART.md](QUICKSTART.md) for the fastest setup.

![Prague Club of Investors](app/static/images/hero-bg.jpg)

---

## 🎯 Mission & Vision

**KI Asset Management (KI AM)** enables motivated students to gain real capital management experience while outperforming market indices.

### Investment Objective
> Outperforming **EEMS** (MSCI Emerging Markets Index) through disciplined, research-driven stock selection.

### Our Values
| Value | Description |
|-------|-------------|
| 🧘 **Patience** | Long-term thinking over short-term speculation |
| 🔮 **Foresight** | Anticipating market trends before they materialize |
| 🛡️ **Integrity** | Transparent analysis and honest reporting |

---

## ✨ Key Features

### 🔐 Authentication & Security
- **Domain-restricted registration**: Only `@klubinvestoru.com` emails
- **Secure password-less onboarding**: Email-based password setup
- **CSRF protection**: All forms protected against cross-site request forgery
- **Activity logging**: Full audit trail of user actions

### 📊 Performance Tracking
- **Real-time stock prices**: Yahoo Finance integration via `yahooquery`
- **Automatic calculation**: Daily performance updates for all approved analyses
- **Benchmark comparison**: Compare against S&P 500 (SPY) and FTSE All-World (VT)
- **Annualized returns**: Proper annualization for holdings > 1 year
- **CSV export**: Download detailed performance reports

### 🗳️ Board Voting System
- **Democratic portfolio construction**: Board members vote on stock purchases
- **Portfolio performance tracking**: Track Board-approved portfolio vs benchmarks
- **Purchase date management**: Flexible date adjustment for accurate tracking

### 🤖 AI-Assisted Workflows
- **Automatic ticker matching**: DeepSeek API + Brave Search for company identification
- **Smart company mapping**: Automatic company name to ticker symbol resolution

### 📝 Blog & Content Management
- **SEO-Optimized Blog**: Built-in blog system with meta tags, keywords, and social sharing
- **AI-Powered Article Generation**: Convert PDF/DOCX documents into full blog articles
  - Investment Pitch style for stock analyses with BUY/HOLD/SELL recommendations
  - Academic Paper style for research reports
  - SEO Article style for web-optimized content
- **AI SEO Assistant**: Auto-generate meta descriptions, keywords, and excerpts
- **Unsplash Integration**: Search and select from 6 curated images for featured images
- **Markdown & HTML Support**: Write in your preferred format

### 📱 Modern UI/UX
- **Premium design**: Apple-inspired aesthetics with glassmorphism effects
- **Responsive layout**: Works on desktop, tablet, and mobile
- **Smooth animations**: Scroll-triggered reveals and micro-interactions
- **Bloomberg Terminal feel**: Professional dashboards for logged-in users

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Main Page   │  │   Dashboard  │  │  Analytics   │          │
│  │  (Public)    │  │  (Private)   │  │  (Private)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      BLUEPRINTS                           │  │
│  │  ┌────────┐ ┌────────┐ ┌──────────┐ ┌────────────────┐  │  │
│  │  │  main  │ │  auth  │ │  analyst │ │     admin      │  │  │
│  │  │(public)│ │(public)│ │(private) │ │   (private)    │  │  │
│  │  └────────┘ └────────┘ └──────────┘ └────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      UTILITIES                            │  │
│  │  ┌────────────┐ ┌─────────────┐ ┌─────────────────────┐  │  │
│  │  │ csv_import │ │ performance │ │ yfinance_helper     │  │  │
│  │  └────────────┘ └─────────────┘ └─────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ SQLAlchemy
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  SQLite (Dev)  │  PostgreSQL (Prod)  │  CSV Exports     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.10 or higher
- Git
- 500MB free disk space

### 1. Clone the Repository

```bash
git clone <repository-url>
cd analyst_website
```

### 2. Set Up Virtual Environment

Choose your operating system:

#### 🐧 Arch Linux / Manjaro

```bash
# Install Python and Git if not present
sudo pacman -S python python-pip git

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 🐧 Debian / Ubuntu / Linux Mint

```bash
# Install Python and Git if not present
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 🍎 macOS

```bash
# Install Homebrew if not present: https://brew.sh
# Then install Python
brew install python git

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 🪟 Windows (PowerShell)

```powershell
# Make sure Python 3.10+ is installed: https://python.org
# Then in PowerShell:

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

#### 🪟 Windows (Command Prompt)

```cmd
REM Create virtual environment
python -m venv venv

REM Activate it
venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:
```bash
SECRET_KEY=your-super-secret-random-key-here
FLASK_ENV=development

# Email is REQUIRED for registration/password reset (use SMTP for local dev)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

> 💡 **Tip**: Generate a secure secret key with: `python -c "import secrets; print(secrets.token_hex(32))"`
> 
> 📧 **Email Setup**: For local development, use Gmail SMTP. For production, use SendGrid (see [Email Configuration](#email-configuration-required) below).

### 5. Initialize Database & Create Admin

```bash
flask init-db
flask create-admin
```

When prompted, enter your `@klubinvestoru.com` email and a secure password.

### 6. Run Development Server

```bash
flask run
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📁 Project Structure

```
analyst_website/
├── app/                          # Main application package
│   ├── __init__.py              # App factory & CLI commands
│   ├── config.py                # Environment configurations
│   ├── extensions.py            # Flask extensions (db, login, mail)
│   ├── models.py                # SQLAlchemy database models
│   │
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── forms.py             # WTForms for login/register
│   │   ├── routes.py            # Login, logout, password reset
│   │   └── utils.py             # Token generation, email sending
│   │
│   ├── admin/                   # Admin panel blueprint
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py            # Dashboard, users, CSV upload,
│   │                            # performance, board voting
│   │
│   ├── analyst/                 # Analyst dashboard blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Personal dashboard, performance
│   │
│   ├── main/                    # Public pages blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Landing page, about, terms
│   │
│   ├── utils/                   # Utility modules
│   │   ├── csv_import.py        # CSV parsing & import logic
│   │   ├── performance.py       # Performance calculation engine
│   │   ├── yahooquery_helper.py # Yahoo Finance integration
│   │   ├── ticker_resolver.py   # Smart ticker resolution with caching
│   │   ├── brave_search.py      # Web search for tickers
│   │   └── deepseek_client.py   # DeepSeek AI integration
│   │
│   ├── email_service.py         # Email service (SendGrid/SMTP)
│   │
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html            # Base layout with navigation
│   │   ├── main/                # Public page templates
│   │   ├── auth/                # Authentication templates
│   │   ├── analyst/             # Analyst dashboard templates
│   │   └── admin/               # Admin panel templates
│   │
│   ├── static/                  # Static assets
│   │   ├── css/                 # Stylesheets (Tailwind + custom)
│   │   ├── js/                  # JavaScript files
│   │   └── images/              # Team photos, icons, logos
│   │
│   └── images/                  # Team member photos
│       ├── Analythical Team leader - Adam Kolomazník picture for main page.jpg
│       └── Qualified Analyst member image for the main page - has a comment.png
│
├── instance/                    # Database file (auto-created)
│   └── analyst.db
│
├── plans/                       # Architecture documentation
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .env                         # Your local environment (gitignored)
├── .gitignore                   # Git ignore rules
├── Procfile                     # Heroku deployment config
├── Dockerfile                   # Docker deployment config
└── README.md                    # This file
```

---

## 🔧 Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ | - | Flask secret key for sessions |
| `FLASK_ENV` | ❌ | `production` | `development` or `production` |
| `USE_LOCAL_SQLITE` | ❌ | `True` | Use local SQLite (`True`) or PostgreSQL (`False`) |
| `DATABASE_URL` | ❌ | `sqlite:///instance/analyst.db` | PostgreSQL connection string (neon.tech) |
| **Email (Choose ONE)** ||||
| `SENDGRID_API_KEY` | ✅* | - | **RECOMMENDED** for production (Render) |
| `MAIL_DEFAULT_SENDER` | ✅* | - | Default "from" address (required with SendGrid) |
| `MAIL_SERVER` | ✅* | `smtp.gmail.com` | SMTP server (local dev only) |
| `MAIL_PORT` | ❌ | `587` | SMTP port |
| `MAIL_USE_TLS` | ❌ | `true` | Use TLS for email |
| `MAIL_USERNAME` | ✅* | - | SMTP username (local dev only) |
| `MAIL_PASSWORD` | ✅* | - | SMTP password/app password (local dev only) |
| **Optional APIs** ||||
| `DEEPSEEK_API_KEY` | ❌ | - | DeepSeek API for AI-assisted ticker matching and blog SEO |
| `BRAVE_SEARCH_API_KEY` | ❌ | - | Brave Search API for ticker lookup fallback |
| `UNSPLASH_API_KEY` | ❌ | - | Unsplash API for blog featured images |
| **Blog Features** ||||
| `DEEPSEEK_API_KEY` | ❌ | - | Required for AI article generation and SEO optimization |
| `UNSPLASH_API_KEY` | ❌ | - | Required for featured image search |
| **Other** ||||
| `ALLOWED_EMAIL_DOMAIN` | ❌ | `klubinvestoru.com` | Allowed registration domain |

\* **Email is REQUIRED** - The app uses email for user registration (password setup) and password reset. You must configure either SendGrid (recommended for production) or SMTP (for local development).

**Database Configuration:**

For local development:
```bash
USE_LOCAL_SQLITE=True
```

For production (Render + neon.tech):
```bash
USE_LOCAL_SQLITE=False
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require
```

**Keep Your Render Service Awake:**
Render's free tier spins down after 15 minutes of inactivity, causing 30-60 second delays. To prevent this:

1. Sign up at [https://uptimerobot.com](https://uptimerobot.com) (free)
2. Add a monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://your-app-name.onrender.com`
   - **Interval**: 5 minutes
3. Done! Your app stays awake 24/7.

Alternative services: [UptimeReboot](https://uptimereboot.com), [Cron-Job.org](https://cron-job.org)

### Email Configuration (REQUIRED)

The application **requires email** for user registration (password setup) and password reset functionality. Without email configured, users cannot complete registration or reset their passwords.

You have two options:

#### Option 1: SendGrid (Twilio) - RECOMMENDED for Production

SendGrid is the **preferred email provider** for production deployments because:
- ✅ Works on Render free tier (SMTP ports are blocked on free tier)
- ✅ 100 emails/day free tier
- ✅ Reliable delivery rates

**Setup Steps:**
1. Go to [https://sendgrid.com](https://sendgrid.com) and sign up for a free account
2. Verify your email address
3. Complete Single Sender Verification:
   - Go to **Settings > Sender Authentication > Single Sender Verification**
   - Click "Create New Sender"
   - Fill in your details (use your `@klubinvestoru.com` email)
   - Verify the sender email via the confirmation link
4. Create an API Key:
   - Go to **Settings > API Keys**
   - Click "Create API Key"
   - Name: `KI Asset Management`
   - Permissions: **Full Access** (or restrict to "Mail Send" only)
   - Copy the generated key (starts with `SG.`)
5. Add to your `.env` file:
   ```bash
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   MAIL_DEFAULT_SENDER=your-verified-sender@klubinvestoru.com
   ```

#### Option 2: SMTP (Local Development Only)

For local development, you can use Gmail SMTP or any SMTP provider.

**Gmail Setup:**
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Add to your `.env` file:
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-gmail-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

> ⚠️ **Note:** SMTP will **NOT work on Render's free tier** as they block outbound SMTP ports. Use SendGrid for production.

---

### Optional APIs (Ticker Matching)

These APIs enable AI-assisted ticker matching for company names. While optional, they significantly improve the experience when importing CSV data.

#### DeepSeek API (AI Ticker Matching)

DeepSeek provides AI-powered company name to ticker symbol resolution.

**Setup Steps:**
1. Go to [https://platform.deepseek.com](https://platform.deepseek.com) and sign up
2. Complete account verification (email + phone)
3. Go to **API Keys** section in the dashboard
4. Click "Create API Key"
5. Name it `KI Asset Management` and copy the key
6. Add to your `.env` file:
   ```bash
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Pricing:** DeepSeek offers free tier credits for new users. Check their pricing page for current rates.

#### Brave Search API (Ticker Lookup Fallback)

Brave Search is used as a fallback when DeepSeek cannot find a ticker. It searches the web for ticker information.

**Setup Steps:**
1. Go to [https://api.search.brave.com](https://api.search.brave.com) and sign up
2. Create a free account
3. Go to **API Keys** section
4. Generate a new API key
5. Copy the key (format: long alphanumeric string)
6. Add to your `.env` file:
   ```bash
   BRAVE_SEARCH_API_KEY=BSxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

**Pricing:** Brave offers 2,000 free queries/month on the free tier.

---

## 📖 Usage Guide

### For Administrators

#### 1. Upload Analysis Schedule
1. Navigate to **Admin → CSV Upload**
2. Upload the Notion-exported analysis schedule (CSV format)
3. System automatically parses and creates analyses

#### 2. Manage Company Tickers
1. Go to **Admin → Company Ticker Mappings**
2. For companies without tickers, either:
   - Manually set the ticker symbol
   - Use "Auto-fill with DeepSeek" for AI-assisted matching
   - Mark as "Other Event" for non-stock items

#### 3. Board Voting
1. Go to **Admin → Board**
2. Vote "Yes" or "No" on each analysis
3. If Yes votes > No votes, stock is considered "Purchased"
4. Adjust purchase dates as needed
5. Click "Calculate Performance" to see portfolio returns

#### 4. View Performance
1. Go to **Admin → Performance**
2. Filter by decision type (Approved only, Neutral+Approved, All)
3. Toggle annualized returns for long-term holdings
4. Click "Details" on any analyst for deep-dive comparison charts

#### 5. Export Data
- Click "Export CSV" on Performance page for analyst rankings
- Click "Export CSV" on Board page for portfolio details

### For Analysts

1. **Register** with your `@klubinvestoru.com` email
2. **Set password** via the email link
3. **Log in** to view your personal dashboard
4. **Track performance** of your approved analyses
5. **Compare** your returns against club average and benchmarks

### For Blog Writers

#### Writing Articles

1. **Create New Post**: Go to **Blog → New Post**
2. **Write Content**: Use the HTML editor with toolbar for formatting
3. **SEO Optimization**: Click "Auto-Generate with AI" to:
   - Generate meta description and keywords
   - Create excerpt and suggested tags
   - Search 6 relevant Unsplash images (select your favorite)
4. **Save & Publish**: Save as draft or publish immediately

#### AI-Powered Document Import

Convert stock analyses and research documents into blog articles:

1. **Upload Document**: On the New Post page, select your PDF or DOCX file
2. **Choose Style**:
   - **Investment Pitch**: For stock analyses (includes BUY/HOLD/SELL recommendation)
   - **SEO Article**: For web-optimized content
   - **Academic Paper**: For formal research reports
   - **Blog Post**: For casual, conversational content
3. **Generate**: AI will extract content and create a complete article
4. **Review & Edit**: Check the generated content, modify as needed
5. **Add Images**: Select from 6 AI-suggested Unsplash images

#### Security Limits
- Maximum file size: 10MB
- Allowed formats: PDF, DOCX, DOC
- Rate limits: 5 document uploads, 20 SEO generations per hour

---

## 🎨 Design System

### Color Palette
```
Primary:    #0d6efd (Bootstrap Blue)
Secondary:  #6c757d (Gray)
Success:    #198754 (Green)
Danger:     #dc3545 (Red)
Warning:    #ffc107 (Yellow)
Info:       #0dcaf5 (Cyan)
Light:      #f8f9fa (Light Gray)
Dark:       #212529 (Dark)

Custom Gradients:
- Hero: linear-gradient(135deg, #0d6efd 0%, #198754 100%)
- Dark: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
- Gold: linear-gradient(135deg, #f5af19 0%, #f12711 100%)
```

### Typography
- **Headings**: Inter, system-ui, sans-serif
- **Body**: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- **Monospace**: SF Mono, Monaco, Consolas for data

### Components
- **Cards**: `border-radius: 1rem`, subtle shadows
- **Buttons**: `border-radius: 0.5rem`, hover transforms
- **Tables**: Striped with hover states
- **Forms**: Floating labels, validation feedback

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest test_performance.py
```

---

## 🚢 Deployment

### Recommended Deployment Options (Free)

Two excellent options for deploying this application:

| Platform | Best For | Documentation |
|----------|----------|---------------|
| **Render + neon.tech** | Beginners, extensive docs | [DEPLOYMENT.md](DEPLOYMENT.md) |
| **Koyeb + neon.tech** | Always-on, no cold starts | [KOYEB.md](KOYEB.md) |

Both use **neon.tech** for the PostgreSQL database (free tier with automatic backups).

---

#### Option 1: Render + neon.tech

| Service | Purpose | Cost |
|---------|---------|------|
| **Render** | Web hosting | Free tier |
| **neon.tech** | PostgreSQL database | Free tier |

**Why this combination?**
- ✅ Render free tier runs reliably with 100GB bandwidth
- ✅ neon.tech provides reliable PostgreSQL with automatic backups
- ✅ Both have generous free tiers (sufficient for 20-50 users)
- ✅ Easy GitHub integration (auto-deploy on push)
- ✅ **Neon-optimized**: Aggressive caching minimizes DB compute units (CU-hours)

**⚠️ Important**: Render free tier spins down after 15 min inactivity. Use [UptimeRobot](https://uptimerobot.com) (free) to ping your site every 5 minutes and keep it awake 24/7.

### Quick Deploy (3 Steps)

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Create neon.tech Database**
   - Sign up at https://neon.tech (GitHub login)
   - Create project → Copy connection string

3. **Deploy to Render**
   - Sign up at https://render.com (GitHub login)
   - New Web Service → Select your repo
   - Set environment variables → Deploy

📖 **Detailed Instructions**: See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step guide with screenshots.

📖 **Quick Reference**: See [QUICKSTART.md](QUICKSTART.md) for command cheat sheet.

---

### 🚀 Neon.tech Optimization (Auto-Enabled)

The application is **automatically optimized** for Neon.tech serverless PostgreSQL to minimize compute unit (CU-hours) usage:

| Feature | Benefit |
|---------|---------|
| **In-Memory Caching** | Public pages served from memory (no DB calls) |
| **Aggressive Cache TTL** | 1 hour for most content, 24 hours for static data |
| **Health Check Endpoint** | `/health` returns 200 without hitting the database |
| **Auto Cache Warming** | Caches pre-populated on startup and weekly refresh |
| **Smart Invalidation** | Cache cleared only when data changes |

**Result**: ~80-90% reduction in database queries for public traffic.

📖 **Full Documentation**: See [NEON_OPTIMIZATION.md](NEON_OPTIMIZATION.md)

#### Option 2: Koyeb + neon.tech (Recommended for Always-On)

Koyeb is a modern serverless platform with **no cold starts** on the free tier.

**Why Koyeb?**
- ✅ Always-on service (no sleeping, no wake-up delays)
- ✅ Fast deployments and builds
- ✅ European servers (Frankfurt, Paris) - great for Prague
- ✅ Free tier includes 1 always-on web service

**Quick Deploy (4 Steps)**

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Create neon.tech Database**
   - Sign up at https://neon.tech (GitHub login)
   - Create project → Copy connection string

3. **Deploy to Koyeb**
   - Sign up at https://www.koyeb.com (GitHub login)
   - Create Web Service → Select your repo
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:create_app()`

4. **Set Environment Variables**
   ```
   SECRET_KEY=your-random-key
   USE_LOCAL_SQLITE=False
   DATABASE_URL=postgresql://... (from neon.tech)
   FLASK_ENV=production
   PORT=8000
   ```

📖 **Detailed Koyeb Instructions**: See [KOYEB.md](KOYEB.md) for complete guide.

### Alternative Deployment Options

#### 🐳 Docker Deployment

Docker provides a consistent, portable environment that works identically across all platforms.

**Prerequisites:**
- Docker Engine 20.10+ installed on your system
- Docker Compose 2.0+ (usually included with Docker Desktop)

**Step-by-Step Setup:**

1. **Install Docker** (if not already installed):
   - **Debian/Ubuntu**: Follow the detailed guide in "Debian Linux Server Setup" section below
   - **macOS**: Download Docker Desktop from https://www.docker.com/products/docker-desktop
   - **Windows**: Download Docker Desktop from https://www.docker.com/products/docker-desktop

2. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd analyst_website
   ```

3. **Build and run with Docker Compose:**
   ```bash
   # Build the image and start containers
   docker-compose up -d --build
   
   # View logs
   docker-compose logs -f
   
   # Initialize database (first time only)
   docker-compose exec web flask init-db
   docker-compose exec web flask create-admin
   ```

4. **Access the application:**
   - Open http://localhost:5000 in your browser
   - Admin interface: http://localhost:5000/admin

5. **Common Docker commands:**
   ```bash
   # Stop containers
   docker-compose down
   
   # Restart containers
   docker-compose restart
   
   # Update after code changes
   docker-compose up -d --build
   
   # Access container shell
   docker-compose exec web /bin/bash
   ```

**Production Docker Deployment:**

For production with PostgreSQL:

```bash
# Create a production docker-compose file
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/analyst_db
      - SENDGRID_API_KEY=${SENDGRID_API_KEY}
    depends_on:
      - db
    restart: always

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=analyst_db
    restart: always

volumes:
  postgres_data:
EOF

# Run with production config
docker-compose -f docker-compose.prod.yml up -d
```

---

#### ☁️ Fly.io Deployment

Fly.io is a modern platform that runs applications close to users globally. Great for low-latency access across Europe.

**Step-by-Step Setup:**

1. **Install Fly.io CLI:**
   ```bash
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   
   # Add to PATH
   export PATH="$HOME/.fly/bin:$PATH"
   ```

2. **Sign up and login:**
   ```bash
   fly auth signup    # If you don't have an account
   fly auth login     # If you already have an account
   ```

3. **Prepare your application:**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd analyst_website
   
   # The repository already includes a fly.toml configuration file
   # Review it to ensure it matches your needs:
   cat fly.toml
   ```

4. **Create the app on Fly.io:**
   ```bash
   fly apps create ki-asset-management
   ```

5. **Create a PostgreSQL database:**
   ```bash
   fly postgres create \
     --name ki-asset-management-db \
     --region fra \
     --vm-size shared-cpu-1x
   
   # Attach database to your app
   fly postgres attach ki-asset-management-db --app ki-asset-management
   ```

6. **Set environment variables:**
   ```bash
   fly secrets set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
   fly secrets set FLASK_ENV=production
   fly secrets set SENDGRID_API_KEY=your-sendgrid-api-key
   fly secrets set MAIL_DEFAULT_SENDER=your-email@klubinvestoru.com
   fly secrets set ADMIN_EMAIL=admin@klubinvestoru.com
   ```

7. **Deploy the application:**
   ```bash
   fly deploy
   ```

8. **Initialize the database:**
   ```bash
   fly ssh console -C "flask init-db"
   fly ssh console -C "flask create-admin"
   ```

9. **Access your application:**
   ```bash
   fly open
   ```
   Or visit: `https://ki-asset-management.fly.dev`

10. **View logs:**
    ```bash
    fly logs
    ```

**Updating your deployment:**
```bash
# After making code changes
git add .
git commit -m "Your changes"
fly deploy
```

---

#### 🖥️ Debian Linux Server Setup

Complete guide for setting up the application on a Debian/Ubuntu server (DigitalOcean, AWS EC2, Linode, etc.).

**Prerequisites:**
- A Debian 11+ or Ubuntu 22.04+ server
- SSH access to the server
- Domain name (optional but recommended)

**Step-by-Step Server Setup:**

**Step 1: Connect to Your Server**
```bash
ssh root@your-server-ip
```

**Step 2: Update System Packages**
```bash
apt update && apt upgrade -y
```

**Step 3: Install Required Software**
```bash
# Install Python, Git, Nginx, and other dependencies
apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib supervisor

# Verify installations
python3 --version   # Should be 3.10+
git --version
nginx -v
```

**Step 4: Configure PostgreSQL Database**
```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE analyst_db;
CREATE USER analyst_user WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE analyst_db TO analyst_user;
\q
```

**Step 5: Create Application User**
```bash
# Create a dedicated user for the application
useradd -m -s /bin/bash analyst
usermod -aG sudo analyst

# Switch to the new user
su - analyst
```

**Step 6: Clone and Setup Application**
```bash
# Clone repository
git clone <repository-url>
cd analyst_website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create environment file
cat > .env << 'EOF'
FLASK_ENV=production
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
USE_LOCAL_SQLITE=False
DATABASE_URL=postgresql://analyst_user:your-secure-password@localhost:5432/analyst_db
SENDGRID_API_KEY=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=your-email@klubinvestoru.com
ADMIN_EMAIL=admin@klubinvestoru.com
EOF
```

**Step 7: Initialize Database**
```bash
# Run while in the application directory with venv activated
flask init-db
flask create-admin
```

**Step 8: Configure Gunicorn Service**

Create a systemd service file (run as root or with sudo):
```bash
sudo tee /etc/systemd/system/ki-asset-management.service << 'EOF'
[Unit]
Description=KI Asset Management Flask Application
After=network.target

[Service]
User=analyst
Group=analyst
WorkingDirectory=/home/analyst/analyst_website
Environment="PATH=/home/analyst/analyst_website/venv/bin"
EnvironmentFile=/home/analyst/analyst_website/.env
ExecStart=/home/analyst/analyst_website/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 "app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable ki-asset-management
sudo systemctl start ki-asset-management

# Check status
sudo systemctl status ki-asset-management
```

**Step 9: Configure Nginx as Reverse Proxy**
```bash
sudo tee /etc/nginx/sites-available/ki-asset-management << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # Or your server IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/analyst/analyst_website/app/static;
        expires 30d;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/ki-asset-management /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

**Step 10: Set Up SSL with Let's Encrypt (Recommended)**
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Follow the interactive prompts
# Certbot will automatically update Nginx configuration
```

**Step 11: Configure Firewall**
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

**Maintenance Commands:**
```bash
# View application logs
sudo journalctl -u ki-asset-management -f

# Restart application
sudo systemctl restart ki-asset-management

# Update application (after code changes)
cd ~/analyst_website
git pull
source venv/bin/activate
pip install -r requirements.txt
flask init-db  # If there are database migrations
sudo systemctl restart ki-asset-management

# Backup database
sudo -u postgres pg_dump analyst_db > backup_$(date +%Y%m%d).sql

# Restore database
sudo -u postgres psql analyst_db < backup_file.sql
```

**Troubleshooting:**
- **Application won't start**: Check logs with `sudo journalctl -u ki-asset-management -n 50`
- **Nginx 502 error**: Ensure Gunicorn is running on port 8000
- **Permission denied**: Check that the `analyst` user owns all application files
- **Database connection failed**: Verify PostgreSQL is running with `sudo systemctl status postgresql`

---

### Other Deployment Options

- **Heroku**: See [DEPLOYMENT.md](DEPLOYMENT.md#heroku-deployment)
- **VPS (General)**: See [DEPLOYMENT.md](DEPLOYMENT.md#vps-deployment)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Git workflow
- Pull request process
- Code review checklist

---

## 👥 Team

### Leadership

<table>
<tr>
<td align="center">
<img src="app/images/Analythical Team leader - Adam Kolomazník picture for main page.jpg" width="150" style="border-radius: 50%"><br>
<strong>Adam Kolomazník</strong><br>
<em>President of the Investment Committee</em><br>
CTU & WU Alumni<br>
Leading strategic vision and investment decisions
</td>
<td align="center">
<img src="app/images/Qualified Analyst member image for the main page - has a comment.png" width="150" style="border-radius: 50%"><br>
<strong>Šimon Havlík</strong><br>
<em>Analyst & Lead Developer</em><br>
VŠE Economics Student<br>
"Join us and gain real-world investment experience while building production-grade financial technology"
</td>
</tr>
</table>

---

## 📊 Performance Highlights

*First Year Achievements:*
- 📈 **60+** Analytical Meetings
- 📊 **60+** Workshops
- 📝 **12** Deep-dive Analyses
- 🎯 **Active portfolio** of 15-25 carefully selected stocks

---

## 🐛 OS-Specific Troubleshooting

### Arch Linux / Manjaro

**Issue: `pip install` fails with "externally-managed-environment"**
```bash
# Solution: Use pip with --break-system-packages flag
pip install -r requirements.txt --break-system-packages

# OR use a virtual environment (recommended - see Quick Start)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Issue: `python` command not found**
```bash
# Arch uses python3 by default
sudo ln -s /usr/bin/python3 /usr/bin/python
# OR use python3 explicitly
python3 -m venv venv
```

### Debian / Ubuntu / Linux Mint

**Issue: `pip: command not found`**
```bash
# Install pip
sudo apt update
sudo apt install python3-pip -y

# For venv support
sudo apt install python3-venv -y
```

**Issue: Permission denied when installing packages**
```bash
# Always use virtual environment - never sudo pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Issue: Missing Python development headers**
```bash
# If installing psycopg2 fails
sudo apt install python3-dev libpq-dev -y
```

### Windows

**Issue: `venv\Scripts\activate` doesn't work**
```powershell
# In PowerShell, use:
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue: `pip is not recognized`**
```cmd
# Reinstall Python and check "Add Python to PATH" during installation
# Or manually add to PATH:
# C:\Users\YOURNAME\AppData\Local\Programs\Python\Python311\Scripts\
# C:\Users\YOURNAME\AppData\Local\Programs\Python\Python311\
```

**Issue: SQLite database locked**
```cmd
# Windows sometimes has file locking issues
# Solution: Close all terminal windows, reopen, try again
# Or use PostgreSQL instead of SQLite for production
```

### All Operating Systems

**Issue: Database errors after pulling new code**
```bash
# Reset database (WARNING: loses all data)
rm instance/analyst.db  # Linux/Mac
del instance\analyst.db  # Windows
flask init-db
flask create-admin
```

**Issue: Port 5000 already in use**
```bash
# Use different port
flask run --port=5001
```

---

## 📜 License

This project is developed for internal use by the **Prague Club of Investors (Klub Investorů)**. All rights reserved.

---

## 🆘 Support

For technical support or questions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Create an issue in the repository
3. Contact the Investment Committee

---

<p align="center">
  <strong>Built with 💚 by the Prague Club of Investors</strong><br>
  <em>Empowering the next generation of investment professionals</em>
</p>
