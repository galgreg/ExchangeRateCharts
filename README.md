# Exchange Rate Charts
Simple Python script, which generates exchange rate charts based on data retrieved from Exchange Rates API.
Supported currencies:
* EUR - Euro
* USD - US dollar
* JPY - Japanese yen
* BGN - Bulgarian lev
* CZK - Czech koruna
* DKK - Danish krone
* GBP - Pound sterling
* HUF - Hungarian forint
* PLN - Polish zloty
* RON - Romanian leu
* SEK - Swedish krona
* CHF - Swiss franc
* ISK - Icelandic krona
* NOK - Norwegian krone
* HRK - Croatian kuna
* RUB - Russian rouble
* TRY - Turkish lira
* AUD - Australian dollar
* BRL - Brazilian real
* CAD - Canadian dollar
* CNY - Chinese yuan renminbi
* HKD - Hong Kong dollar
* IDR - Indonesian rupiah
* ILS - Israeli shekel
* INR - Indian rupee
* KRW - South Korean won
* MXN - Mexican peso
* MYR - Malaysian ringgit
* NZD - New Zealand dollar
* PHP - Philippine peso
* SGD - Singapore dollar
* THB - Thai baht
* ZAR - South African rand
## Implementation details
Project has been implemented in Python language (version 3.6), using only few external dependencies.
Non-standard libraries used in project:
* [docopt](http://docopt.org/)
* [requests](https://requests.kennethreitz.org/en/master/)
* [leather](https://leather.readthedocs.io/en/0.3.3/)

To retrieve data about exchange rates, project calls to [**Exchange Rates API**](https://exchangeratesapi.io/).

## How to build & run the project

### 1. Clone Git repo
```
git clone https://github.com/galgreg/ExchangeRateCharts.git
```
### 2. Create virtual environment and install dependencies
#### a) Using venv and pip:
##### - Create and activate virtual environment using venv (check [documentation](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to see how to do it).
##### - Install dependencies from file:
```
pip install -r requirements_pip.txt
```
#### b) Using conda:
```
conda create --name <your-env-name> --file requirements_conda.txt
```
### 3. Check help to see how to call script
```
python exchange_rate.py -h
```
## Terms of use
Author takes no responsibility for any damage or loss caused by improper use of above application.
