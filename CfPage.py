from BasePage import BasePage
from CfPageLocator import CfPageLocator
import pandas as pd
import time
class CfPage(BasePage) :
    def __init__(self,driver):
        self.driver = driver

    def accept_recs(self):
        self.do_click(CfPageLocator.PRIVACY_ACCEPT)
        self.driver.maximize_window()

    def fill_dataset(self):

        self.check_exists_by_xpath(CfPageLocator.SHOW_MORE)

        dep_times_list = self.save_to_list(CfPageLocator.DEPART_TIME)
        arrival_times_list = self.save_to_list(CfPageLocator.ARRIVAL_TIME)
        airline_list = self.save_multi_to_single(CfPageLocator.AIRLINE)
        time.sleep(5)
        duration_list = self.save_to_list(CfPageLocator.DURATION)
        price_list = self.save_to_list(CfPageLocator.PRICE)
        dataset = pd.DataFrame()
        for i in range(len(dep_times_list)):
            try:
                dataset.loc[i, 'dTime'] = dep_times_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'aTime'] = arrival_times_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'airline'] = airline_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'price'] = price_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'duration'] = duration_list[i]
            except:
                pass
        return dataset

    def fill_tway_dataset(self):
        # global dep_times_list

        self.check_exists_by_xpath(CfPageLocator.SHOW_MORE)


        time.sleep(15)

        dep_times_list = self.save_to_list(CfPageLocator.DEPART_START_TIME)
        arrival_times_list = self.save_to_list(CfPageLocator.ARRIVAL_START_TIME)
        time.sleep(5)
        airline_list = self.save_multi_to_single(CfPageLocator.AIRLINE)
        time.sleep(5)
        return_arrival_list = self.save_to_list(CfPageLocator.ARRIVAL_RETURN_TIME)
        return_depart_list = self.save_to_list(CfPageLocator.DEPART_RETURN_TIME)

        #TODO duration lists
        a_duration_list = self.save_to_list(CfPageLocator.ARR_DURATION)
        b_duration_list = self.save_to_list(CfPageLocator.BCK_DURATION)

        price_list = self.save_to_list(CfPageLocator.PRICE)
        dataset = pd.DataFrame()
        for i in range(len(dep_times_list)):
            try:
                dataset.loc[i, 'dTime'] = dep_times_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'aTime'] = arrival_times_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'aDuration'] = a_duration_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'backDtime'] = return_depart_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'backAtime'] = return_arrival_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'duration'] = b_duration_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'airline'] = airline_list[i]
            except:
                pass
            try:
                dataset.loc[i, 'price'] = price_list[i]
            except:
                pass

        return dataset