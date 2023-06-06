# CashFlow Dashboard

The CashFlow Dashboard is a powerful financial tool designed to provide you with a comprehensive overview of your bank accounts. With this user-friendly dashboard, you can effortlessly track and analyze your financial transactions, gain insights into your spending habits, and make informed decisions about your personal finances.

By utilizing a .csv file from different banks that contains your spending and income data, the dashboard algorithms categorize your transactions based on the keywords you provide. This categorization enables the dashboard to generate intuitive and interactive graphics, offering a visual representation of where your money is being spent.

The dashboard's interface allows for easy customization and interaction. You can filter data by month, year or category 

## Getting Started

### Installation and run an example file
To install and set up the dashboard, follow these steps:
- Clone the repository: ``` git clone https://github.com/MIRIPP/CashFlow-Dashboard.git ```
- install Python 3.9 on your machine. ``` python --versiont ```
- Install the necessary libraries: ``` pip install dash  panda dash_bootstrap_components```
- Run Application
  
### Set your personal source Data
Once you have run the dashboard with the demo data, you can add your own personal .csv files from different banks that contain your spending and income data. Follow these steps:
- Create a directory (named by year) for each year you can provide source data: e.g 2022 ``` mkdir   .\SourceFile\data\2022```
- Add a file named "user_settings.json" to store your user-spesific input data.   ``` cp .\SourceFile\data\2020\user_settings.json .\SourceFile\data\2022\```
  (You can copy the "user_settings.json" file from the existing "2020" directory to the new year's directory)
- Store the .csv file containing your bank account's spending and income data in the respective year directory.

  
## Demo
