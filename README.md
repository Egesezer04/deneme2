📚 Listing Quality Scoring System

A modern Python application that scrapes listing data (books, products, real estate like card layouts), analyzes listing quality, stores results in SQLite, and displays everything in a clean Tkinter GUI.

Bu proje Selenium + BeautifulSoup + SQLite + OOP + Tkinter + Threading ile tam bir “modern Python uygulaması” örneğidir.

🚀 Features
✅ Web Scraping

•Dynamic page loading using Selenium WebDriver

•HTML extraction through BeautifulSoup

•Automatically parses the first 10 product listings

•Built in retry mechanism (up to 3 attempts)

•Threading support → GUI freezes never happen

•Automatic ChromeDriver installation via webdriver-manager

✅ Object Oriented Business Logic

Models

•BaseModel – Shared base with unique ID

•Listing – A unified listing/item structure (title, price, description, images)

Scoring System

•AbstractScorer – Enforced interface for all scoring algorithms

•QualityScorer – Full quality scoring based on:

•Title

•Price

•Description length

•Image count

✅ SQLite Database

•Automatic table creation on startup

•Safe inserts using dictionary parameter binding

•Saves full listing info:

•title

•price

•description

•images

•score

•missing fields

✅ Tkinter GUI

•URL input field

•“Let’s Go” scrape button

•TreeView listing table

•Red log output panel

•Background scraping using a worker thread

•Completely responsive GUI (no freezing)

🧱 Project Architecture Overview

/ project
│── app.py               # Main Tkinter GUI application
│── models.py            # BaseModel & Listing
│── scorer.py            # Scoring interface + QualityScorer
│── scraper.py           # Selenium + BeautifulSoup scraper logic
│── database.py          # SQLite operations
│── README.md            # This file

Main Components

•BaseModel → shared base

•Listing → data structure

•AbstractScorer → scoring interface

•QualityScorer → weighted scoring rules

•Database → SQLite persistence

•App → Tkinter GUI controller

📊 Quality Scoring Logic

| Criterion   | Points | Notes                    |
| ----------- | ------ | ------------------------ |
| Title       | 0–10   | Missing → 0 points       |
| Price       | 0–20   | Low or missing → warning |
| Description | 0–20   | Based on text length     |
| Images      | 0–20   | 0, 1–2, or 3+ images     |

🛠 Installation

1️⃣ Install dependencies

pip install selenium bs4 webdriver-manager

2️⃣ Run the project

python app.py

3️⃣ GUI will open

Enter a URL → click Let’s Go → results instantly appear.

🌐 Scraping Workflow

1)ChromeDriver installs automatically

2)Selenium loads the webpage

3)BeautifulSoup parses the page source

4)First 10 product cards are detected

5)Each item becomes a Listing object

6)Items are scored using QualityScorer

7)Results are:

  •Saved to SQLite (listings.db)
  •Displayed in the GUI table

🖥️ How to Use the GUI

1)Enter any URL (default: books.toscrape.com)

2)Click Let’s Go

3)Scraper fetches & evaluates the first 10 products

4)The table displays:

   •Title
   •Price
   •Image count
   •Score

5)Errors and logs appear in the red status area

🔐 Robustness & Safety Features

•Driver startup protected with try/except

•URL validation

•Page load retry (up to 3 attempts)

•Safe DB insertion with parameter binding

•Thread-safe GUI updating (root.after)

•Logging of every important event into scraper.log

•Graceful error handling → no crashes

📦 Technologies Used

•Python 3.10+

•Selenium WebDriver

•BeautifulSoup4

•Tkinter GUI

•SQLite3

•Webdriver Manager

•Threading

•OOP architecture

🧪 Tested On

•Windows 11

•Google Chrome (latest)

•Python 3.10 / Python 3.11

🎥 Demo



