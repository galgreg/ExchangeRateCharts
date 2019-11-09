from docopt import docopt
from datetime import datetime
import requests
import leather

def get_options():
    APP_USAGE_DESCRIPTION = """
Generate exchange rates chart based on data provided by Exchange Rates API.

Usage:
    exchange_rate.py --start-at=<start-date> --end-at=<end-date> [options]
    exchange_rate.py -h | --help

Options:
    --start-at=<start-date>             Specify date of chart's begin
    --end-at=<end-date>                 Specify date of chart's end
    --base=<base-currency>              Specify base currency [default: PLN].
    --symbols=<currency-symbols>        Specify currency symbols [default: EUR,USD,GBP,CHF].
    --chart-path=<path-for-new-chart>   Specify path for new chart [default: exchange_rate.svg]
"""
    options = docopt(APP_USAGE_DESCRIPTION)
    return options

def convertDateToString(date):
    dateString = "{0}-{1}-{2}".format(
            date.year,
            str(date.month).zfill(2),
            str(date.day).zfill(2))
    return dateString

def exchange_rate(startDate, endDate, base, symbols, chartPath):
    startDateString = convertDateToString(startDate)
    endDateString = convertDateToString(endDate)
    
    symbolString = ""
    for symbol in symbols:
        symbolString += "{0},".format(symbol)
    symbolString = symbolString.strip(",")
    
    options = {
        "--start-at" : startDateString,
        "--end-at" : endDateString,
        "--base" : base,
        "--symbols" : symbolString,
        "--chart-path" : chartPath
    }
    exchange_rate_cmd(options)

def tick_formatter(value, index, tick_count):
    return '{0}-{1}-{2}'.format(
            value.year,
            str(value.month).zfill(2),
            str(value.day).zfill(2))

def createChart(chartData, fileName):
    startDate = datetime.strptime(chartData["start_at"], "%Y-%m-%d").date()
    endDate = datetime.strptime(chartData["end_at"], "%Y-%m-%d").date()
    baseCurrency = chartData["base"]

    chart = leather.Chart('Exchange rate for {0}'.format(baseCurrency))
    chart.add_x_axis(tick_formatter=tick_formatter)
    chart.add_x_scale(startDate, endDate)

    datesList = list(chartData["rates"].keys())
    datesList.sort()
    lineData = []
    
    numberOfLines = len(chartData["rates"][datesList[0]].keys())
    for _ in range(numberOfLines):
        lineData.append([])
    
    labelsList = list(chartData["rates"][datesList[0]].keys())
    labelsList.sort()
    
    for i in range(numberOfLines):
        for date in datesList:
            dayRate = chartData["rates"][date][labelsList[i]]
            lineData[i].append(dayRate)

    datesList = [datetime.strptime(date, "%Y-%m-%d").date() for date in datesList]
    for i in range(numberOfLines):
        chart.add_line(tuple(zip(datesList, lineData[i])), name = labelsList[i])

    chart.to_svg(fileName)

def exchange_rate_cmd(options):
    startDate = options["--start-at"]
    endDate = options["--end-at"]
    base = options["--base"]
    symbols = options["--symbols"]
    
    linkToResources = \
            "https://api.exchangeratesapi.io/history?start_at={0}&end_at={1}" \
            "&base={2}&symbols={3}".format(startDate, endDate, base, symbols)
    
    try:
        response = requests.get(linkToResources)
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API, check your internet connection!")
        exit()
    
    if response.status_code != 200:
        print("Something went wrong! Cannot request API! " \
                "(linkToResources = '{0}', response.status_code = {1}.".format(
                linkToResources, response.status_code))
        exit()
    
    responseContent = response.json()
    
    for date in responseContent["rates"].keys():
        for currency in responseContent["rates"][date]:
            rate = responseContent["rates"][date][currency]
            responseContent["rates"][date][currency] = round(1 / rate, 6)

    pathToChart = options["--chart-path"]
    createChart(responseContent, pathToChart)

if __name__ == "__main__":
    options = get_options()
    exchange_rate_cmd(options)
