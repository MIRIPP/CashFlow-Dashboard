# CashFlow Dashboard

The CashFlow Dashboard is a powerful financial tool designed to provide you with a comprehensive overview of your bank accounts. With this user-friendly dashboard, you can effortlessly track and analyze your financial transactions, gain insights into your spending habits, and make informed decisions about your personal finances.

By utilizing a .csv file from different banks that contains your spending and income data, the dashboard algorithms categorize your transactions based on the keywords you provide. This categorization enables the dashboard to generate intuitive and interactive graphics, offering a visual representation of where your money is being spent.

The dashboard's interface allows for easy customization and interaction. You can filter data by month, year or category 

## Getting Started

### Installation
To install and set up the dashboard, follow these steps:
- Clone the repository by running the following command: git clone <repository-url>
- install Python 3.9 on your machine
- Install the necessary libraries by running the following command: pip install dash, panda
  
### Inital Data Settings
Before using the dashboard, ensure the following initial data settings:
- Create a directory for each year you have source data, within the "data" directory. For example, create directories named "data/2020", "data/2021", etc.
- Store the .csv file containing your bank account's spending and income data in the respective year directory.
- Add a file named "user_settings.json" to store input data such as column translations, data format, start money, line start, bank name, and keywords. Refer to the example file for the desired format of this file.
  
### Regualary use
For regular usage of the dashboard, follow these steps:
- Update the .csv file from your bank with the latest data.
- If necessary, go to the input table section of the dashboard to modify entries if the algorithms could not correctly identify all categories. Attention, only the "Client," "Category," and "Description" columns can be changed in this section.

  
## Demo
