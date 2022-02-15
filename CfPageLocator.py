from selenium.webdriver.common.by import By


class CfPageLocator(object):
    PRIVACY_ACCEPT = (By.XPATH, '//*[@title="Accept"]')
    DEPART_START_TIME = (By.XPATH,'//ol/li[1]/div/div/div[3]/div/span[1]/span')
    DEPART_TIME = (By.XPATH,'//*[@class="depart-time base-time"]')
    ARRIVAL_START_TIME = (By.XPATH,'//ol/li[1]/div/div/div[3]/div/span[3]/span')
    ARRIVAL_TIME = (By.XPATH,'//*[@class="arrival-time base-time"]')
    PRICE = (By.XPATH, '//*[@class="above-button"]//child::div//child::a//child::span//child::span'
                       '[@class="price-text"]')
    #
    DURATION = (By.XPATH, '//*[@class="section duration allow-multi-modal-icons"]')
    ARR_DURATION = (By.XPATH,'//ol/li[1]/div/div/div[5]/div[@class="top"]')
    BCK_DURATION = (By.XPATH,'//ol/li[2]/div/div/div[5]/div[@class="top"]')

    AIRLINE = (By.XPATH,'//*[@class="codeshares-airline-names"]')
    ARRIVAL_RETURN_TIME = (By.XPATH,'//ol/li[2]/div/div/div[3]/div/span[3]/span')
    DEPART_RETURN_TIME = (By.XPATH, '//ol/li[2]/div/div/div[3]/div/span[1]/span')
    SHOW_MORE = (By.XPATH,'//a[@class="moreButton"]')

