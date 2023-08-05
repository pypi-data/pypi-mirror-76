"""
Generates performance reports for your stock portfolio.
"""
import csv
import argparse
import requests

def main(args = None):
    """
    Entrypoint into program.
    """
    args = ParseArgs()
    sourceData = read_portfolio(args.source)
    url = makeURL(sourceData)
    validateData(sourceData, url)
    marketData = getCurrentMarketData(url)
    mergedData = mergeMarketDataWithSourceData(sourceData, marketData)
    targetData = addValues(mergedData)
    save_portfolio(targetData, args.target)

def ParseArgs(args = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--target")
    return parser.parse_args(args)

def makeURL(data):
    url = 'https://api.iextrading.com/1.0/tops/last?symbols='
    for symbol in data:
        url += symbol['symbol'] + ","
    return url[:-1]

def validateData(data, url):
    inputSymbols = []
    validSymbols = []
    invalidSymbols = inputSymbols # start off with all the symbols used
    for symbol in data:
        inputSymbols.append(symbol['symbol'])
    response = requests.get(url)
    content = response.json()
    for row in content:
        validSymbols.append(row['symbol'])
        invalidSymbols.remove(row['symbol']) # remove valid symbols so only invalid symbols remain.
    print(f'Data was retreived for the the following valid symbols: {validSymbols}\nData was not retreived for the following invalid symbols: {invalidSymbols}')

def getCurrentMarketData(url):
    response = requests.get(url)
    content = response.json()
    for row in content:
        del row['size'], row['time']
    return content

def mergeMarketDataWithSourceData(sourceData, marketData):
    for marketrow in marketData:
        for sourcerow in sourceData:
            if marketrow['symbol'] == sourcerow['symbol']:
                sourcerow['latest_price'] = marketrow['price']
    return sourceData

def addValues(mergedData):
    for row in mergedData:
        if 'latest_price' in row:
            book_value = int(row['units']) * float(row['cost'])
            market_value = int(row['units']) * float(row['latest_price'])
            gain_loss = market_value - book_value
            change = round(gain_loss / book_value, 3)

            row['book_value'] = book_value
            row['market_value'] = market_value
            row['gain_loss'] = gain_loss
            row['change'] = change
    return mergedData


def read_portfolio(filename):
    """Returns data from a CSV file"""
    # TODO: Read the CSV file with the filename above,
    #       and return the data. Use a DictReader.
    fileData = []
    with open(filename, newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            fileData.append(row)
    return fileData


def save_portfolio(data, filename):
    """Saves data to a CSV file"""
    # TODO: Save the provided data to the provided filename. Use
    #       a DictWriter

    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    main()
