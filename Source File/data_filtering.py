# -*- coding: utf-8 -*-
import dash
import plotly.express as px
import pandas as pd

pd.options.mode.chained_assignment = None  # exclude panda warning message
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import os
import numpy as np
import pathlib

# todo:
# 2. design dashboard 2h
# 3. interactive graph 3h
# 4 interactive table, add category https://dash.plotly.com/datatable ---- https://plotly.com/python/table/ ----- https://coderzcolumn.com/tutorials/data-science/how-to-create-basic-dashboard-in-python-with-widgets-plotly-dash
# 5. dynamic fist line finder, dynamic csv file adder    https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-study-browser

PATH = pathlib.Path(__file__).parent


class SourceData:
    def __init__(self, year="2020"):
        self.__year = year
        self.keywords = {}
        self.set_keywords()
        self.data_path = PATH.joinpath("data/" + year).resolve()

        self.df = pd.read_csv(self.data_path.joinpath("source_file.csv"), delimiter=",", encoding="utf-8-sig")

        df_dkb = self.get_new_source_data("dkb", 8, {"Buchungstag": "Date", "Betrag (EUR)": "Amount",
                                                     "Verwendungszweck": "Purpose",
                                                     "Auftraggeber / Begünstigter": "Client"})
        df_ksk = self.get_new_source_data("ksk", 0,
                                          {"Valutadatum": "Date", "Betrag": "Amount", "Verwendungszweck": "Purpose",
                                           "Beguenstigter/Zahlungspflichtiger": "Client"}, '%d.%m.%y')
        df_credit_card_dkb = self.get_new_source_data("credit_card", 6, {"Belegdatum": "Date", "Betrag (EUR)": "Amount",
                                                                         "Beschreibung": "Purpose"})

        self.df = self.merge_source_data([df_dkb, df_ksk, df_credit_card_dkb])
        self.df = self.clean_dataframe(self.df)
        self.df = self.set_auto_category(self.df)

        self.df.to_csv(self.data_path.joinpath("source_file.csv"), encoding="utf-8-sig", index=False)

        self.create_all_dataframe()

        print(self.df.to_csv)

    """
    def create_all_dataframe
    create all different kind of dataframe for the graphics later
    """

    def create_all_dataframe(self):
        # create dataframes
        self.df_spending = self.df.loc[self.df["Amount"] < 0]
        self.df_spending = self.df_spending.loc[self.df_spending["Category"] != "Transaktionen"]
        self.df_income = self.df.loc[self.df["Amount"] > 0]
        self.df_income = self.df_income.loc[self.df_income["Category"] != "Transaktionen"]
        self.df_saving = self.df.loc[self.df["Category"] != "Transaktionen"]
        self.df_dkb = self.df.loc[self.df["Bank"] == "DKB"]
        self.df_credit_card = self.df.loc[self.df["Bank"] == "DKB credit card"]
        self.df_ksk = self.df.loc[self.df["Bank"] == "KSK"]

        self.df_saving.to_csv(self.data_path.joinpath("spending.csv"), encoding="utf-8-sig", index=False)

        # group data for graphics

        # Group_spending_by_categories_sum
        self.gr_spending_by_categories_ges = self.df_spending.groupby(["Category"]).sum().sort_values(
            "Amount")  # mean()
        # self.gr_spending_by_categories_ges = self.gr_spending_by_categories_ges.loc[self.df["Amount"] == -20]

        # Group_spending_by_categories_average
        self.gr_spending_by_categories_average = self.gr_spending_by_categories_ges
        last_element = float(self.df['Date'].max().month) - 1 + (float(self.df['Date'].max().day) / 30)
        self.gr_spending_by_categories_average["Amount"] = self.gr_spending_by_categories_ges["Amount"].div(
            last_element)
        self.gr_spending_by_categories_average["Amount"] = self.gr_spending_by_categories_ges["Amount"].mul(-1)

        # Group_sending_by_categories_each month
        self.gr_spending_by_categories_monthlist = list()
        for month_no in range(1, 12):
            self.df_month = self.df_spending[self.df_spending['Date'].dt.month == month_no]
            list_item = self.df_month.groupby(["Category"]).sum().sort_values("Amount")
            list_item["Amount"] = list_item["Amount"].mul(-1)
            self.gr_spending_by_categories_monthlist.append(list_item)

        # Group_spending_by_month_sum
        self.gr_spending_by_moth = self.df_spending.groupby(pd.Grouper(key="Date", freq="M")).sum()  # mean()
        self.gr_income_by_moth = self.df_income.groupby(pd.Grouper(key="Date", freq="M")).sum()  # mean()

        # Group_spending_by_month_sum
        self.gr_saving_by_month = self.df_saving.groupby(pd.Grouper(key="Date", freq="M")).sum()  # mean()

        # Group_spending_by_month_sum
        self.gr_saving_by_month = self.df_saving.groupby(pd.Grouper(key="Date", freq="M")).sum()  # mean()

        # Bank balance
        self.df['cum_sum'] = self.df["Amount"].cumsum()
        self.df_dkb = self.df_dkb.reset_index(drop=True)
        self.df_dkb['cum_sum'] = self.df_dkb["Amount"].cumsum()
        self.df_credit_card = self.df_credit_card.reset_index(drop=True)
        self.df_credit_card['cum_sum'] = self.df_credit_card["Amount"].cumsum()
        self.df_ksk = self.df_ksk.reset_index(drop=True)
        self.df_ksk['cum_sum'] = self.df_ksk["Amount"].cumsum()

    """
    def get_new_source_data
    @param:     -csv_filename = filename of the source file of the certain bank
                -first_data_row = number of lines they have to be deleted before the data comes
                -dict_old_new_col = dictionary where we replace all the old with new column
                -mspecial_date_format = not None if the date of the source file need special treatment
    
    """

    def get_new_source_data(self, csv_filename, first_data_row, dict_old_new_col, special_date_format=None):

        # 1. read data from excel
        new_source_df = pd.read_csv(self.data_path.joinpath(csv_filename + ".csv"), delimiter=";",
                                    encoding="ISO-8859-1", skiprows=first_data_row)

        # 2. create new Category for column Bank, Category and Description
        new_source_df.insert(1, "Bank", csv_filename)
        new_source_df.insert(2, "Category", "aaa")
        new_source_df.insert(3, "Description", "aaa")

        # 3. Rename column in standard format
        new_source_df = new_source_df.rename(columns=dict_old_new_col)

        # 4. add colum if missing
        if 'Client' not in new_source_df:
            new_source_df["Client"] = "aaa"

        # 8. formate date so it able to read later
        if special_date_format is not None:
            new_source_df["Date"] = pd.to_datetime(new_source_df["Date"], format='%d.%m.%y')

        return self.clean_dataframe(new_source_df)

    """
    def clean_dataframe
    @param: dataframe = dataframe to clean up (delete unused column, change format for "date" and "amount"
    """

    def clean_dataframe(self, dataframe):
        # 1. delete all unnecessary columns
        dataframe = dataframe[['Date', 'Bank', 'Amount', 'Purpose', 'Client', 'Category', 'Description']]

        # 2. change the Amount in float number (delete first the comma and dot and divide the number by 100)
        dataframe["Amount"] = dataframe["Amount"].apply(str)  # convert to string
        dataframe["Amount"] = dataframe["Amount"].str.replace(",", "", regex=False)  # change "," to ""
        dataframe["Amount"] = dataframe["Amount"].str.replace(".", "", regex=False)  # change "." to ""
        dataframe["Amount"] = pd.to_numeric(dataframe["Amount"])  # convert to float
        dataframe["Amount"] = dataframe["Amount"].div(100)

        # 3. change the date in date format
        dataframe["Date"] = pd.to_datetime(dataframe["Date"])  # convert to date

        # 4. modify the string in Purpose to avoid errors
        dataframe["Purpose"] = dataframe["Purpose"].str.replace(",", ".")
        dataframe["Purpose"] = dataframe["Purpose"].str.replace('\s+', ' ', regex=True)
        dataframe["Purpose"] = dataframe["Purpose"].str[:100]
        dataframe["Purpose"] = dataframe["Purpose"].str.rstrip()

        # 6. modify the string in Client to avoid errors
        dataframe["Client"] = dataframe["Client"].str.replace(",", ".")

        # 7. fill empty cells with "aaa" to filter later empty cells easier
        dataframe = dataframe.fillna("aaa")

        return dataframe

    """
        def merge_source_data
        @param: list_of_source_df = list of all source dataframes 
    """

    def merge_source_data(self, list_of_source_df):
        # 1. merge to one file
        dataframe = pd.concat(list_of_source_df, ignore_index=False)  # merge

        # 2. delete double lines
        columns_never_changed = ["Date", "Bank", "Amount", "Purpose", "Client"]
        dataframe.drop_duplicates(subset=columns_never_changed, inplace=True, keep='last')
        dataframe = dataframe.sort_values("Date", ascending=True, ignore_index=True)

        return dataframe

    """
        def set_keywords
        @param: keywords = list of all keywords
    """

    def set_keywords(self):
        self.keyowrds_income = {
            "Job": ["Gehalt", "EDAG Engineering GmbH"],
        }
        self.keywords_spending = {
            "Essen": ["Rewe", "ALDI SUED", "ALDI GMBH", "BUNK", "CAP Markt", "ADIS ALB-DONAU-INDUSTRIE-S", "E-CENTER",
                      "SUBWAY", "Lidl", "EDEKA", "TAKEAWAYCOM"],
            "Essen gehen": ["Restau", "MCDONALDS", "BURGER KING"],
            "Going out": ["Bargeldausz", "Food", "Finkbeiner", "Cinemaxx", "Entertainm", "Prime Video", "Zur Zill",
                          "BRAUEREI GOLD OCHSEN", "Xinedome", "ChocletUlm", "HERR BERGERULM"],
            "Job": ["Gehalt", "EDAG Engineering GmbH"],
            "Steuer": ["Finanzamt"],
            "Kleidung": ["H&M", "C&A", "Clothes", "PEEK & CLOPPENBURG", "ZALANDOSE", "SPORT-SOHN", "Puma",
                         "MARC O'POLO", "Outlet", "SPORT SOHN"],
            "Drogerie": ["Drogerie", "MUELLER"],
            "Mitgliedsbeiträge": ["Mitglieds", "Jahresbeitrag", "e.V."],
            "Projekte": ["Media Markt", "Saturn", "Electronic", "Reichelt", "Baumarkt", "MUEKRA", "MEDIAMARKT",
                         "Funduino", "BAUHAUS", "BAYWA"],
            "Versicherungen": ["Alianz", "Versicherung", "Krankenversicherung"],
            "Wohnung": ["Stuff"],
            "Auto": ["Autowerkstatt", "Bussgeldstelle"],
            "Zug": ["HANDYTICKET", "DB AUTOMAT"],
            "Fahrrad": ["Bike"],
            "Tanken": ["Aral", "MTB", "Agip", "TANKSTELLE", "ESSO"],
            "Bildung": ["Fernuni Hagen", "HEISEMEDIEN"],
            "Urlaub": ["Hotel", "Flug"],
            "Handy": ["Mobilfunknummer", "Aldi Talk"],
            "Zinsen": ["siehe Anlage"],
            "Investment": [],
            "Transaktionen": ["KREDITKARTENABRECHNUNG", "Ausgleich Kreditkarte", "Michael Rippel", "Einzahlung"]
            }

        self.keywords = {**self.keyowrds_income, **self.keywords_spending}

    """
        def set_auto_category
         @param: dataframe = dataframe to add the categories

    """

    def set_auto_category(self, dataframe):
        # 1 add Category by Keywords in Purpose
        for key, items in self.keywords.items():
            for item in items:
                # 1.1 Check if Keyword of certain catergory is mentioned in col "Purpose"
                x = dataframe[dataframe['Purpose'].str.contains(item, case=False, na=False, regex=False)].index.values
                # x: indexes of all cells with the keyword in
                if len(x):  # if len(x) a keyword is found
                    for x_index in x:
                        # Debug line: print(str(x_index) + " " + str(dataframe.iloc[x_index]['Purpose']) + " - " + str(dataframe.iloc[x_index]['Client']))
                        # add category
                        dataframe.loc[x_index, 'Category'] = key

                # 2 add Category by Keywords in Client
                x = dataframe[dataframe['Client'].str.contains(item, case=False, na=False, regex=False)].index.values
                # print('Client' + str(x))
                if len(x):
                    for x_index in x:
                        # Debug line: print(str(dataframe.iloc[x_index]['Purpose']) + " - " + str(dataframe.iloc[x_index]['Client']))
                        if dataframe.iloc[x_index]['Category'] == "aaa":
                            dataframe.loc[x_index, 'Category'] = key

        # 2 add Category by -100 €
        for index, row in dataframe.iterrows():
            if dataframe.iloc[index]['Amount'] == -100:
                dataframe.loc[index, 'Category'] = "Going out"

        # 3add time between
        # dataframe.between_time('2020-07-24', '0:45')

        # 4 add Description by description given before
        # for index, row in dataframe.iterrows():
        #    if dataframe.iloc[index]['Category'] == "aaa":
        #        purpose_of_searched_item = dataframe.iloc[index]['Purpose']
        #        x = dataframe.index[(dataframe['Purpose'] == purpose_of_searched_item) & (dataframe['Description'] != "aaa")].tolist()
        #        if len(x):
        #            for x_index in x:
        #                dataframe.loc[index, 'Description'] = dataframe.iloc[x_index]['Description']

        return dataframe


if __name__ == "__main__":
    source_date = SourceData()
