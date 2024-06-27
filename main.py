import json
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from advertisement import Advertisement


def get_yandex_realty():
    with open('config.json', 'r') as f:
        config = json.load(f)
    ad_count = 0
    urls = config['urls_yandex']
    driver = get_chrome_driver()
    for base_url in urls:
        page = 0
        while True:
            url = f'{base_url}{page}'
            print(url)
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.OffersSerpItem')))

            offers = driver.find_elements(By.CSS_SELECTOR, '.OffersSerpItem')
            data = []

            for offer in offers:
                data.append(get_ad(offer, url))
                ad_count += 1

            try:
                button = driver.find_element(By.XPATH, "//a[contains(text(), 'Следующая')]")
                button.get_attribute('href')
                page += 1
            except Exception:
                break
    driver.quit()

    print(f"Количество объявлений : {ad_count}")
    print(data)


def get_ad(offer, url):
    link = offer.find_element(By.CSS_SELECTOR, '.OffersSerpItem__link').get_attribute('href')
    cost = offer.find_element(By.CSS_SELECTOR, '.OffersSerpItem__price').text.split('₽')[0]

    title = offer.find_element(By.CSS_SELECTOR, '.OffersSerpItem__title').text
    rooms_count = get_rooms_count(title)
    floor = get_floor(title)
    square = get_square(title)

    type_of_deal = get_deal_type(url)
    building_type = get_building_type(url)

    address = offer.find_element(By.CSS_SELECTOR, '.AddressWithGeoLinks__addressContainer--4jzfZ').text
    street = address.split(', ')[0]
    house = address.split(', ')[1]
    return Advertisement(
        link,
        cost,
        rooms_count,
        type_of_deal,
        building_type,
        street,
        house,
        floor,
        square
    )


def get_chrome_driver(user_agent=None):
    chrome_options = webdriver.ChromeOptions()

    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_deal_type(url):
    ad_type = url.split('/')[4]
    if ad_type == 'kupit':
        return 'Купить'
    if ad_type == 'snyat':
        if url.split('/')[6] == 'posutochno':
            return 'Снять посуточно'
        return 'Снять'


def get_building_type(url):
    b_type = url.split('/')[7]
    if b_type == 'novostroyki':
        return 'Новостройки'
    if b_type == 'vtorichniy-rynok':
        return 'Вторичка'
    else:
        return None


def get_square(title):
    square_match = re.search(r'(\d+(?:,\d+)?) м²', title)
    return float(square_match.group(1).replace(',', '.')) if square_match else None


def get_rooms_count(title):
    rooms_match = re.search(r'((\d+)-комнатная квартира|квартира-студия)', title)
    if rooms_match:
        if 'студия' in rooms_match.group(1):
            return 'Студия'
        else:
            return int(rooms_match.group(1).split('-')[0])


def get_floor(title):
    floor_match = re.search(r'(\d+) этаж из (\d+)', title)
    return int(floor_match.group(1)) if floor_match else None


if __name__ == '__main__':
    get_yandex_realty()

# def get_location(address):
#     geolocator = Nominatim(user_agent="Tester")
#     location = geolocator.geocode(address)
#     print(location)
#     print(location.latitude, location.longitude)
