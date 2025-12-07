from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

BASE_PRICES = {
    "Cursor": 15, "Grandma": 100, "Farm": 1100,
    "Mine": 12000, "Factory": 130000, "Bank": 1400000,
}

BASE_CPS = {
    "Cursor": 0.1, "Grandma": 1, "Farm": 8,
    "Mine": 47, "Factory": 260, "Bank": 1400,
}

PRICE_MULTIPLIER = 1.15
building_count = {}


def parse_number(text):
    match = re.search(r"[\d.]+", text.replace(",", ""))
    return float(match.group()) if match else 0


def get_price(name):
    return int(BASE_PRICES.get(name, 0) * (PRICE_MULTIPLIER ** building_count.get(name, 0)))


def main():
    global building_count
    
    options = webdriver.ChromeOptions()
    options.add_argument("--mute-audio")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8000")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "langSelect-EN"))).click()
    big_cookie = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "bigCookie")))

    last_check = time.time()
    estimated_cps = 1.0

    while True:
        for _ in range(20):
            big_cookie.click()
        
        if time.time() - last_check < 0.5:
            continue
        last_check = time.time()

        golden = driver.find_elements(By.CSS_SELECTOR, ".shimmer")
        if golden:
            golden[0].click()

        upgrades = driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
        if upgrades:
            upgrades[0].click()

        cookies = parse_number(driver.find_element(By.ID, "cookies").text.split()[0])
        estimated_cps = 1.0 + sum(BASE_CPS.get(n, 0) * c for n, c in building_count.items())

        candidates = []
        for p in driver.find_elements(By.CSS_SELECTOR, ".product"):
            name = p.find_element(By.CSS_SELECTOR, ".title.productName").text.strip()
            if name not in BASE_CPS:
                continue
            
            price = get_price(name)
            payback = price / BASE_CPS[name]
            save_time = 0 if cookies >= price else (price - cookies) / max(estimated_cps, 0.1)
            
            candidates.append({
                "el": p, "name": name, "price": price,
                "total": save_time + payback,
                "afford": "enabled" in p.get_attribute("class")
            })

        if not candidates:
            continue

        best = min(candidates, key=lambda x: x["total"])
        
        if best["afford"]:
            best["el"].click()
            building_count[best["name"]] = building_count.get(best["name"], 0) + 1


if __name__ == "__main__":
    main()