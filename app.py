import tkinter as tk
from tkinter import ttk
import threading
import logging
from models import Listing
from database import Database
from scoring import QualityScorer
from scraper import fetch_listings

logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')

class App:
    def __init__(self, root):
        self.root = root
        root.title("Books to Scrape Scraper")

        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.insert(0, "http://books.toscrape.com/")
        self.url_entry.pack()

        self.btn_scrape = tk.Button(root, text="Lets Go", command=self.start_scraping)
        self.btn_scrape.pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("Title", "Price", "Images", "Score"), show="headings", height=12)
        for col in ("Title", "Price", "Images", "Score"):
            self.tree.heading(col, text=col)
        self.tree.pack()

        self.log = tk.Label(root, text="", fg="red")
        self.log.pack(pady=5)

    def start_scraping(self):
        threading.Thread(target=self._scrape_thread, daemon=True).start()

    def _scrape_thread(self):
        url = self.url_entry.get().strip()
        if not url.startswith(("http://", "https://")):
            self.safe_log("Invalid URL")
            return

        listings = fetch_listings(url)
        if not listings:
            self.safe_log("No listings found.")
            return

        db = Database()
        scorer = QualityScorer()

        # Clear treeview safely
        self.root.after(0, lambda: [self.tree.delete(row) for row in self.tree.get_children()])

        for listing in listings:
            try:
                points, missing = scorer.score(listing)
                db.add({
                    "title": listing.title,
                    "price": listing.price,
                    "description": listing.description,
                    "images": ",".join(listing.images),
                    "score": points,
                    "missing": "; ".join(missing)
                })
                try:
                    self.root.after(0, lambda l=listing, p=points:
                                    self.tree.insert("", "end", values=(l.title, l.price, len(l.images), p)))
                except Exception as e:
                    logging.error(f"GUI update error: {e}")
            except Exception as e:
                logging.error(f"Error inserting listing: {e}")

        self.safe_log(f"{len(listings)} listings found and saved.")

    def safe_log(self, text: str):
        """Update GUI log safely and log to file."""
        self.root.after(0, lambda: self.log.config(text=text))
        logging.info(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()