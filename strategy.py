from selenium.webdriver.common.by import By
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


def get_current_cookies(driver):
    return parse_number(driver.find_element(By.ID, "cookies").text.split()[0])


def calculate_estimated_cps():
    return 1.0 + sum(BASE_CPS.get(n, 0) * c for n, c in building_count.items())


def click_golden_cookie(driver):
    golden = driver.find_elements(By.CSS_SELECTOR, ".shimmer")
    if golden:
        golden[0].click()


def buy_upgrade(driver):
    upgrades = driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
    if upgrades:
        upgrades[0].click()


def evaluate_buildings(driver, cookies, estimated_cps):
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

    return candidates


def buy_best_building(candidates):
    if not candidates:
        return False

    best = min(candidates, key=lambda x: x["total"])

    if best["afford"]:
        best["el"].click()
        building_count[best["name"]] = building_count.get(best["name"], 0) + 1
        return True

    return False
