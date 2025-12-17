import time
from initialisation import initialize
from strategy import (
    get_current_cookies,
    calculate_estimated_cps,
    click_golden_cookie,
    buy_upgrade,
    evaluate_buildings,
    buy_best_building
)


def main():
    driver, big_cookie = initialize()

    last_check = time.time()

    while True:
        for _ in range(40):
            big_cookie.click()

        if time.time() - last_check < 0.5:
            continue
        last_check = time.time()

        click_golden_cookie(driver)
        buy_upgrade(driver)

        cookies = get_current_cookies(driver)
        estimated_cps = calculate_estimated_cps()

        candidates = evaluate_buildings(driver, cookies, estimated_cps)
        buy_best_building(candidates)


if __name__ == "__main__":
    main()
