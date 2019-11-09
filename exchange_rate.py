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

def convertStringToDate(dateString):
    dateFormat = "%Y-%m-%d"
    convertedDateTime = datetime.strptime(dateString, dateFormat)
    return convertedDateTime.date()

def createChart(chartData, fileName):
    startDate = convertStringToDate(chartData["start_at"])
    endDate = convertStringToDate(chartData["end_at"])
    baseCurrency = chartData["base"]

    chartTitle = 'Exchange rate for {0}'.format(baseCurrency)
    chart = leather.Chart(chartTitle)
    chart.add_x_axis(tick_formatter = lambda a, b, c : convertDateToString(a))
    chart.add_x_scale(startDate, endDate)

    ratesData = chartData["rates"]
    datesList = list(ratesData.keys())
    datesList.sort()
    lineDataset = []
    
    tempDate = datesList[0]
    labelsList = list(ratesData[tempDate].keys())
    labelsList.sort()

    numberOfLines = len(labelsList)
    for _ in range(numberOfLines):
        lineDataset.append([])

    for i in range(numberOfLines):
        for date in datesList:
            tempLabel = labelsList[i]
            dayRate = ratesData[date][tempLabel]
            lineDataset[i].append(dayRate)

    datesList = [ convertStringToDate(dateString) for dateString in datesList ]
    for i in range(numberOfLines):
        lineData = tuple(zip(datesList, lineDataset[i]))
        chart.add_line(lineData, name = labelsList[i])

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

if __name__ == "__main__":
    options = get_options()
    exchange_rate_cmd(options)
