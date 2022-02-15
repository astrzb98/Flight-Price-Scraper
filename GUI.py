from datetime import datetime, time
from tkinter import *
from tkinter import ttk, filedialog
from tkcalendar import *
import pandas as pd

from Flight import cheap_flights, kayak


class App(Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Flight scrapper')
        self.minsize(900, 600)
        self.fly_from = StringVar()
        self.fly_to = StringVar()
        self.flight_var = StringVar()

        # TODO add new labels
        label = Label(self, text="Znajdz najlepsze połączenie:")
        label.pack(side="top", fill="x")

        # TODO add dicitonary values as records
        self.fly_from.set("WAW")
        arrival_drop = OptionMenu(self, self.fly_from, "WAW", "VIE", "BEG", "SKP")
        arrival_drop.pack(side="left", fill="x")

        # miejsce przylotu
        self.fly_to.set("BEG")
        depart_drop = OptionMenu(self, self.fly_to, "WAW", "VIE", "BEG", "SKP")
        depart_drop.pack(side="right", fill="x")

        self.arrivalCal = Calendar(self, setmode="day", date_pattern='yyyy-mm-dd')
        self.arrivalCal.pack()

        # TODO opcja jednokierunkowa
        self.flight_var.set("z powrotem")
        flight_type = OptionMenu(self, self.flight_var, "jednokierunkowy", "z powrotem")
        flight_type.pack()

        # data wylotu
        self.departCal = Calendar(self, setmode="day", date_pattern='yyyy-mm-dd')
        self.departCal.pack()

        submit = Button(self, text="Szukaj lotów", command=self.searchFlight)
        submit.pack()

    def searchFlight(self):

        today = datetime.today().strftime('%Y-%m-%d')
        arr_date = self.arrivalCal.get_date()
        dep_date = self.departCal.get_date()

        city_from = self.fly_from.get()
        city_to = self.fly_to.get()

        assert city_from != city_to, Label(self, text="Miasto wylotu musi być od miasta przylotu:").pack()

        assert today <= arr_date and today <= dep_date and arr_date <= dep_date, Label(self, text="Data powrotu nie może być pozniejsza niż odlotu").pack()

        if (self.flight_var.get() == 'jednokierunkowy'):
            dep_date = ''

        cheap_df = cheap_flights(city_from, city_to, arr_date, dep_date)

        kayak_df = kayak(city_from, city_to, arr_date, dep_date)

        if len(kayak_df.columns) <= 1:
            kayak_df = kayak(city_from, city_to, arr_date, dep_date)

        dataset = pd.concat([cheap_df, kayak_df])

        # self.dataset.to_excel('{0}-{1} For {2}.xlsx'.format(city_from, city_to,today),
        # engine='xlsxwriter')

        result_window = Toplevel(self)
        self.my_tree = ttk.Treeview(result_window)

        # TODO test na datasecie
        # dataset = pd.read_excel('VIE-BEG For 2022-01-21.xlsx')

        self.fill_treeview(dataset, result_window)

        s = ttk.Style(result_window)
        s.theme_use("clam")
        dataset.loc[:, 'conprice'] = ["".join(filter(str.isnumeric, x)) for x in dataset['price']]

        dataset['conprice'] = pd.to_numeric(dataset['conprice'], errors='coerce')

        self.convert_pdtype(dataset, self.flight_var.get())

        idx = dataset['conprice'].idxmin()

        save = Button(result_window, text="Najtańszy LOT",
                      command=lambda: Label(result_window,
                                            text="Najtańszy lot {0} : {1} "
                                            .format(dataset['airline'][idx]
                                                    , dataset['price'][idx])
                                            ).pack())
        save.pack()

        report = Button(result_window, text="LOTY o średniej cenie jednej linii lotniczej",
                        command=lambda: self.query1(dataset, result_window))
        report.pack()

        times = Button(result_window, text="LOTY po godz.18  ze najkrótszym czasem lotu ",
                       command=lambda: self.query2(dataset, result_window))
        times.pack()

    def query1(self, df, Tl):
        filter1 = df['conprice'] <= df['conprice'].mean()
        filter2 = df['airline'] != "MultipleAirlines"
        new_df = df.where(filter1 & filter2)

        new_df.dropna(inplace=True)
        new_df.drop(columns=['conprice'], inplace=True)

        # df.loc[(df['conprice'] >= df['conprice'].mean())]
        self.fill_treeview(new_df, Tl)

    def query2(self, df, Tl):

        df['durationInt'] = df['duration'].str.replace('\D+', '')
        df['durationInt'] = pd.to_numeric(df['durationInt'], errors='coerce')

        compare_time = time(hour=18, minute=00, second=00)
        filter1 = df['dTime'] > compare_time
        filter2 = df['durationInt'] == df['durationInt'].min()
        new_df = df.where(filter1 & filter2)
        new_df.dropna(inplace=True)

        new_df.drop(columns=['durationInt'], inplace=True)
        df.drop(columns=['durationInt'], inplace=True)

        self.fill_treeview(new_df, Tl)

    def fill_treeview(self, df, Tl):
        tree = ttk.Treeview(Tl)
        tree["column"] = list(df.columns)
        tree["show"] = "headings"

        for column in tree["column"]:
            tree.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            tree.insert("", "end", values=row)
        tree.pack()

    def convert_pdtype(self, dataset, flight_type):
        dataset['dTime'] = pd.to_datetime(dataset['dTime'])
        dataset['aTime'] = pd.to_datetime(dataset['aTime'])

        dataset['dTime'] = dataset['dTime'].dt.time
        dataset['aTime'] = dataset['aTime'].dt.time

        if flight_type != "jednokierunkowy":
            dataset['backAtime'] = pd.to_datetime(dataset['backAtime'])
            dataset['backDtime'] = pd.to_datetime(dataset['backDtime'])

            dataset['backAtime'] = dataset['backAtime'].dt.time
            dataset['backDtime'] = dataset['backDtime'].dt.time


if __name__ == "__main__":
    app = App()
    app.mainloop()
