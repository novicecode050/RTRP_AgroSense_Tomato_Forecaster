from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
from datetime import datetime
import re
import os

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Open BigBasket tomato page
driver.get("https://www.bigbasket.com/ps/?q=tomato")
time.sleep(5)

# Scroll to load products
for _ in range(3):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

products = driver.find_elements(By.XPATH, "//h3")

data = []

# Time info
now = datetime.now()
date = now.strftime("%Y-%m-%d")
day = now.strftime("%A")
month = now.month

for p in products:
    try:
        full_name = p.text.lower()

        # ✅ FILTER ONLY RAW TOMATO
        if "tomato" not in full_name:
            continue

        if any(word in full_name for word in [
            "puree", "ketchup", "sauce", "paste", "chutney", "juice"
        ]):
            continue

        parent = p.find_element(By.XPATH, "./ancestor::div[2]")

        # PRICE
        price = parent.find_element(By.XPATH, ".//span[contains(text(),'₹')]").text
        price_val = float(price.replace("₹", "").replace(",", ""))

        # MRP (optional)
        try:
            mrp = parent.find_element(By.XPATH, ".//span[contains(@class,'line-through')]").text
            mrp_val = float(mrp.replace("₹", "").replace(",", ""))
        except:
            mrp_val = price_val

        # ✅ DISCOUNT from OFF label
        try:
            discount_text = parent.find_element(
                By.XPATH,
                ".//span[contains(text(),'OFF')]"
            ).text
            discount = float(discount_text.replace("%", "").replace("OFF", "").strip())
        except:
            discount = round(((mrp_val - price_val) / mrp_val) * 100, 2) if mrp_val > price_val else 0

        # WEIGHT
        weight_match = re.search(r'(\d+\.?\d*)\s?(kg|g)', full_name)
        if weight_match:
            qty = float(weight_match.group(1))
            unit = weight_match.group(2)

            if unit == "g":
                weight_kg = qty / 1000
            else:
                weight_kg = qty
        else:
            weight_kg = 1

        # BRAND
        if "fresho" in full_name:
            brand = "Fresho"
        elif "organic" in full_name:
            brand = "Organic"
        else:
            brand = "Generic"

        # CLEAN PRODUCT NAME
        name = full_name
        name = re.sub(r'fresho!?', '', name)
        name = re.sub(r'organic', '', name)
        name = re.sub(r'\d+\.?\d*\s?(kg|g)', '', name)
        name = name.strip().title()

        # PRICE PER KG
        price_per_kg = round(price_val / weight_kg, 2)

        data.append([
            name, brand, weight_kg, price_val,
            mrp_val, discount, price_per_kg,
            date, day, month
        ])

    except:
        continue

driver.quit()

# ✅ SAVE CSV (APPEND MODE)
file_exists = os.path.isfile("bigbasket_dataset.csv")

with open("tomato_dataset.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            "Product_Name", "Brand", "Weight_kg", "Price",
            "MRP", "Discount_%", "Price_per_kg",
            "Date", "Day", "Month"
        ])

    writer.writerows(data)

print("✅ Clean tomato dataset updated!")