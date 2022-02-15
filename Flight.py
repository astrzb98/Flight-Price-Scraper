from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import xlsxwriter
from CfPage import CfPage
from time import sleep

from skyscanner_scrapper import BSoupFlight


def cheap_flights(city_from,city_to,arr_date,dep_date):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get('https://www.cheapflights.co.uk/flight-search/{0}-{1}/{2}/{3}?sort=price_a'.format(
        city_from,
        city_to,
        arr_date,
        dep_date
    ))
    sleep(5)
    cheap_flight = CfPage(driver)
    cheap_flight.accept_recs()
    if not dep_date:
        dataset = cheap_flight.fill_dataset()
    else:
        dataset = cheap_flight.fill_tway_dataset()
    return dataset

def kayak(city_from,city_to,arr_date,dep_date):
    sleep(10)
    bs = BSoupFlight(city_from, city_to, arr_date,dep_date)

    if not dep_date:
        dataset = bs.one_way_flight()
    else:
        dataset = bs.multi_way_flight()
    return dataset