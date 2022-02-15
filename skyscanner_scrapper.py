from bs4 import BeautifulSoup
from lxml import etree
from time import sleep
import requests
import re
import pandas as pd
import xlsxwriter

class BSoupFlight:
    def __init__(self, city_from,city_to, date_from, date_to = ''):
        self.url = 'https://www.kayak.co.uk/flights/{0}-{1}/{2}/{3}'. format(city_from
                                                                             ,city_to
                                                                             ,date_from
                                                                             ,date_to)
        self.headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
                         }

    def one_way_flight(self):

        self.page = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.page.text,"html.parser")
        sleep(15)
        self.departure_times = self.soup.find_all('span', {'class': 'depart-time base-time'})
        self.arrival_times = self.soup.find_all('span', {'class': 'arrival-time base-time'})
        self.durations = self.soup.find_all('div', {'class': 'section duration allow-multi-modal-icons'})
        self.airlines_as_html = self.soup.find_all('span', {'class': 'codeshares-airline-names'})
        self.dom = etree.HTML(str(self.soup))
        self.prices_as_html = self.dom.xpath(
            '//*[@class="above-button"]//child::div//child::a//child::span//child::span [@class="price-text"]')

        self.departures = [depart.string for depart in self.departure_times]
        self.arrivals = [arrival.string for arrival in self.arrival_times]
        self.flight_durations = [duration.text.strip() for duration in self.durations]
        self.airline_list = [airline.text for airline in self.airlines_as_html]
        self.prices = [price.text.strip() for price in self.prices_as_html]

        self.airlines = []
        for string in self.airline_list:
            if "," in string:
                self.airlines.append("MultipleAirlines")
            else:
                string = re.sub(r"\s+", '', string)
                self.airlines.append(string)
        if len(self.prices) == len(self.departures):
            df = pd.DataFrame({'dTime': self.departures,
                               'aTime': self.arrivals,
                               'airline': self.airlines,
                               'price': self.prices,
                               'duration': self.flight_durations
                               })
            return df
        else:
            return

    def multi_way_flight(self):
        page = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(page.text,"html.parser")
        sleep(15)
        #self.durations = self.soup.find_all('div', {'class': 'section duration allow-multi-modal-icons'})
        airlines_as_html = soup.find_all('span', {'class': 'codeshares-airline-names'})
        dom = etree.HTML(str(soup))
        prices_as_html = dom.xpath(
            '//*[@class="above-button"]//child::div//child::a//child::span//child::span [@class="price-text"]')
        back_departure_times = dom.xpath(
            '//ol/li[2]/div/div/div[3]/div/span[1]/span')
        back_arrival_times = dom.xpath(
            '//ol/li[2]/div/div/div[3]/div/span[3]/span')
        departure_times = dom.xpath('//ol/li[1]/div/div/div[3]/div/span[1]/span')
        arrival_times = dom.xpath('//ol/li[1]/div/div/div[3]/div/span[3]/span')
        #durations = dom.xpath('//ol/li[1]/div/div/div[5]/child::div[@class="top"]')
        adurations = dom.xpath('//ol/li[1]/div/div/div[5]/div[@class="top"]')
        bdurations = dom.xpath('//ol/li[2]/div/div/div[5]/div[@class="top"]')

        departures = [depart.text.strip() for depart in departure_times]
        arrivals = [arrival.text.strip() for arrival in arrival_times]
        back_departures = [depart.text.strip() for depart in back_departure_times]
        back_arrivals = [arrival.text.strip() for arrival in back_arrival_times]
        arr_durations = [aduration.text.strip() for aduration in adurations]
        bck_durations = [bduration.text.strip() for bduration in bdurations]
        #flight_durations = [duration.text.strip() for duration in durations]
        airline_list = [airline.text for airline in airlines_as_html]
        prices = [price.text.strip() for price in prices_as_html]

        airlines = []
        print(len(departures),len(arrivals),len(back_departures),len(back_arrivals))

        for string in airline_list:
            if "," in string:
                airlines.append("MultipleAirlines")
            else:
                string = re.sub(r"\s+", '', string)
                airlines.append(string)
        if len(prices) == len(departures):
            df = pd.DataFrame({'dTime': departures,
                               'aTime': arrivals,
                               'aDuration': arr_durations,
                               'backDtime': back_departures,
                               'backAtime': back_arrivals,
                               'duration' : bck_durations,
                               'airline': airlines,
                               'price': prices

                               })

            return df
        else:
            return



#bs = BSoupFlight('WAW', 'VIE', '2022-02-28','2022-03-07')
#df = bs.multi_way_flight()

#df.to_excel('WAW-VIE.xlsx', engine='xlsxwriter')

