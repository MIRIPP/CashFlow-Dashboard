# -*- coding: utf-8 -*-
import pandas as pd
import pathlib


pd.options.mode.chained_assignment = None  # exclude panda warning message
PATH = pathlib.Path(__file__).parent


class DataImporter:
    def __init__(self, source_file, year, banks_raw_data, keywords_income, keywords_spending):
        # private
        self.__year = year
        self.__data_path = PATH.joinpath( source_file + '/' + year).resolve()

        # public
        self.data_path_source_file = self.__data_path.joinpath("source_file.csv")
        self.keywords_income = keywords_income
        self.keywords_spending = keywords_spending
        self.categories = list(self.keywords_income.keys()) + list(self.keywords_spending.keys())
        self.start_money = {}
        self.end_money = {}
        self.list_bank_names = []
        self.list_df_banks = []

        self.df = None
        self.df_spending = None
        self.df_income = None
        self.df_saving = None
        self.df_saved = None
        self.gr_spending_by_categories_ges = None
        self.gr_income_by_categories_ges = None
        self.gr_spending_by_categories_average = None
        self.gr_spending_by_categories_month_list = None
        self.gr_combined_by_month_and_category = None
        self.gr_spending_by_moth = None
        self.gr_income_by_moth = None
        self.gr_saving_by_month = None
        self.list_df_bank_balance = []

        # 1. Read already saved source data
        df_source_file = pd.read_csv(self.data_path_source_file, delimiter=",", encoding="utf-8-sig")
        df_source_file["Date"] = pd.to_datetime(df_source_file["Date"], format="%Y-%m-%d")

        # 2. Read new bank data
        df_banks_raw = []
        for bank in banks_raw_data:
            self.list_bank_names.append(bank['name'])
            self.start_money[bank['name']] = int(bank['start_money'])
            df_bank = get_new_source_data(self.__data_path,
                                               bank['name'],
                                               bank['line_start'],
                                               bank['start_money'],
                                               bank['date_format'],
                                               bank['colums_translation'])
            df_banks_raw.append(df_bank)
        df_banks_raw.append(df_source_file)

        # 3. Refactor dataframe
        df = merge_source_data(df_banks_raw)

        df = set_auto_category(df, {**self.keywords_income, **self.keywords_spending})

        # 4. save given data
        df.to_csv(self.data_path_source_file, encoding="utf-8-sig", index=False)

        # 5. Create Dataframes for different graphs
        self.create_all_dataframe(df)

        # 6. Print
        # print(self.df.to_csv)

    def create_all_dataframe(self, dataframe):
        """
        create all different kind of dataframe for the graphics later
        """
        # General
        self.df = dataframe

        self.df_spending = self.df[self.df['Category'].isin(self.keywords_spending.keys())]
        self.df_spending = self.df_spending.loc[self.df_spending["Category"] != "Transaktionen"]
        self.df_spending = self.df_spending.loc[self.df_spending["Category"] != "Savings"]
        self.df_income = self.df[self.df['Category'].isin(self.keywords_income.keys())]
        self.df_saving = self.df.loc[self.df["Category"] != "Transaktionen"]
        self.df_saving = self.df_saving.loc[self.df_saving["Category"] != "Savings"]

        # 1. Spending by Category
        # 1.1 Group_spending_by_categories_sum
        df_spending_amount_category = self.df_spending[['Amount', 'Category']]
        self.gr_spending_by_categories_ges = df_spending_amount_category.groupby(["Category"]).sum().sort_values(
            "Amount")
        self.gr_spending_by_categories_ges["Amount"] = self.gr_spending_by_categories_ges["Amount"].mul(-1)

        df_income_amount_category = self.df_income[['Amount', 'Category']]
        self.gr_income_by_categories_ges = df_income_amount_category.groupby(["Category"]).sum().sort_values(
            "Amount")


        # 1.2 Group_spending_by_categories_average
        self.gr_spending_by_categories_average = df_spending_amount_category.groupby(["Category"]).sum().sort_values(
            "Amount")
        last_element = float(self.df['Date'].max().month) - 1 + (float(self.df['Date'].max().day) / 30)
        self.gr_spending_by_categories_average["Amount"] = self.gr_spending_by_categories_average["Amount"].div(
            last_element)
        self.gr_spending_by_categories_average["Amount"] = self.gr_spending_by_categories_average["Amount"].mul(-1)

        # 1.3 Group_sending_by_categories_each month
        self.gr_spending_by_categories_month_list = list()
        for month_no in range(1, 13):
            df_spending_month = self.df_spending[self.df_spending['Date'].dt.month == month_no]
            df_spending_month_amount_category = df_spending_month[['Amount', 'Category']]
            list_item = df_spending_month_amount_category.groupby(["Category"]).sum().sort_values("Amount")
            list_item["Amount"] = list_item["Amount"].mul(-1)
            self.gr_spending_by_categories_month_list.append(list_item)

        # 1.4 gr_combined_by_month_and_category

        combined_df = self.df_saving
        combined_df['Month'] = combined_df['Date'].dt.to_period('M')
        self.gr_combined_by_month_and_category = combined_df.groupby(['Month', 'Category']).sum().reset_index()

        # 2. Income / Spending (by month)
        self.gr_spending_by_moth = self.df_spending.groupby(pd.Grouper(key="Date", freq="M")).sum()  # mean()
        self.gr_income_by_moth = self.df_income.groupby(pd.Grouper(key="Date", freq="M")).sum()  # mean()

        # 3. Savings (by month)
        self.gr_saving_by_month = self.df_saving.groupby(pd.Grouper(key="Date", freq="M")).sum()  # mean()

        # 4. Bank balance

        # 4.1 Banks
        self.list_df_bank_balance = []
        for banks_name in self.list_bank_names:
            df_bank = self.df.loc[self.df["Bank"] == banks_name]  # filter for certain bank name

            # add start value
            start_row = pd.DataFrame(
                {'Date': [pd.Timestamp(self.__year + '-01-01 00:00:00')], 'Amount': [self.start_money[banks_name]]},
                index=[0])
            df_bank = pd.concat([start_row, df_bank])

            df_bank = df_bank.reset_index(drop=True)  # reset index since new df is created
            df_bank['cum_sum'] = df_bank["Amount"].cumsum()  # add new column "cum_sum"
            self.list_df_banks.append(df_bank)
            self.list_df_bank_balance.append(pd.DataFrame(df_bank, columns=['Date', 'cum_sum']))
            self.end_money[banks_name] = df_bank['cum_sum'].iloc[-1]

        # 4.2 Saved Money
        self.df_saved = self.df.loc[self.df["Category"] == "Savings"]
        self.df_saved["Amount"] *= -1

        df_sum_of_saved = self.df_saved
        start_row = pd.DataFrame(
            {'Date': [pd.Timestamp(self.__year + '-01-01 00:00:00')], 'Amount': 0}, index=[0])

        df_sum_of_saved = pd.concat([start_row, df_sum_of_saved])
        df_sum_of_saved = df_sum_of_saved.reset_index(drop=True)
        df_sum_of_saved['cum_sum'] = df_sum_of_saved["Amount"].cumsum()
        self.list_bank_names.append("Saved")
        self.list_df_banks.append(df_sum_of_saved)
        self.end_money["Saved"] = 0
        self.start_money["Saved"] = 0
        self.list_df_bank_balance.append(pd.DataFrame(df_sum_of_saved, columns=['Date', 'cum_sum']))
        self.end_money["Saved"] = df_sum_of_saved['cum_sum'].iloc[-1]
        self.start_money["Saved"] = 0

        # 4.3 Sum of Bank
        df_sum_of_banks = pd.concat([self.df, self.df_saved], ignore_index=False)
        # df_sum_of_banks = self.df
        sum_start_money = sum(self.start_money.values())
        start_row = pd.DataFrame(
            {'Date': [pd.Timestamp(self.__year + '-01-01 00:00:00')], 'Amount': sum_start_money}, index=[0])
        df_sum_of_banks = pd.concat([start_row, df_sum_of_banks])
        df_sum_of_banks = df_sum_of_banks.reset_index(drop=True)
        df_sum_of_banks = df_sum_of_banks.sort_values("Date", ascending=True, ignore_index=True)
        df_sum_of_banks['cum_sum'] = df_sum_of_banks["Amount"].cumsum()
        self.list_bank_names.append("Sum")
        self.list_df_banks.append(df_sum_of_banks)
        self.list_df_bank_balance.append(pd.DataFrame(df_sum_of_banks, columns=['Date', 'cum_sum']))
        self.end_money["Sum"] = df_sum_of_banks['cum_sum'].iloc[-1]
        self.start_money["Sum"] = sum_start_money


def get_new_source_data(data_path, bank_name, first_data_row, start_money, date_format, dict_old_new_col):
    """
        create a new df with the given source data
    """
    # 1. read data from excel
    new_source_df = pd.read_csv(data_path.joinpath(bank_name + ".csv"), delimiter=";",
                                encoding="ISO-8859-1", skiprows=first_data_row-2)

    # 2. create new Category for column Bank, Category and Description
    new_source_df.insert(1, "Bank", bank_name)
    new_source_df.insert(2, "Category", "aaa")
    new_source_df.insert(3, "Description", "aaa")

    # print(new_source_df)

    # 3. Rename column in standard format
    for old_column_name in new_source_df.columns:
        new_column_name = old_column_name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
        new_source_df.rename(columns={old_column_name: new_column_name}, inplace=True)
    swapped_dict_old_new_col = {v: k for k, v in dict_old_new_col.items()}
    new_source_df = new_source_df.rename(columns=swapped_dict_old_new_col)

    # print(new_source_df)

    # 4. add colum if missing
    if 'Client' not in new_source_df:
        new_source_df["Client"] = "aaa"

    # 5. formate date so it able to read later
    new_source_df["Date"] = pd.to_datetime(new_source_df["Date"], format=date_format)

    return clean_dataframe(new_source_df)


def clean_dataframe(dataframe):
    """
    Parameters:
        dataframe: dataframe to clean up (delete unused column, change format for "date" and "amount"
    """
    # 1. delete all unnecessary columns
    dataframe = dataframe[['Date', 'Bank', 'Amount', 'Purpose', 'Client', 'Category', 'Description']]

    # 2. change the Amount in float number (delete first the comma and dot and divide the number by 100)
    dataframe["Amount"] = dataframe["Amount"].apply(str)  # convert to string
    dataframe["Amount"] = dataframe["Amount"].str.replace(",", "", regex=False)  # change "," to ""
    dataframe["Amount"] = dataframe["Amount"].str.replace(".", "", regex=False)  # change "." to ""
    dataframe["Amount"] = pd.to_numeric(dataframe["Amount"])  # convert to float
    dataframe["Amount"] = dataframe["Amount"].div(100)

    # 3. change the date in date format
    dataframe["Date"] = pd.to_datetime(dataframe["Date"], dayfirst=True)  # convert to date

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


def merge_source_data(list_of_source_df):
    """
    Parameters:
        list_of_source_df: list of all source dataframes
    """
    # 1. merge to one file
    dataframe = pd.concat(list_of_source_df, ignore_index=False)  # merge

    # 2. delete double lines
    columns_never_changed = ["Date", "Bank", "Amount", "Purpose"]  # "Client"
    dataframe.drop_duplicates(subset=columns_never_changed, inplace=True, keep='last')
    dataframe = dataframe.sort_values("Date", ascending=True, ignore_index=True)

    return dataframe


def set_auto_category(dataframe, all_keywords):
    """
    Parameters:
         dataframe: dataframe to add the categories
         all_keywords: keywords for the dataframe

    """
    # 1 add Category by Keywords in Purpose
    for key, items in all_keywords.items():
        for item in items:
            # 1.1 Check if Keyword of certain category is mentioned in col "Purpose"
            x = dataframe[dataframe['Purpose'].str.contains(item, case=False, na=False, regex=False)].index.values
            # x: indexes of all cells with the keyword in
            if len(x):  # if len(x) a keyword is found in one or multiple lines
                for x_index in x:
                    # Debug line: print(str(x_index) + " " + str(dataframe.iloc[x_index]['Purpose']) + " - " + str(dataframe.iloc[x_index]['Client']))
                    # add category
                    if dataframe.iloc[x_index]['Category'] == "aaa":
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
