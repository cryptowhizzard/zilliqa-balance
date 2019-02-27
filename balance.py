import requests
import copy
import multiprocessing
import argparse

DENOMINATOR = 1000000000000.0

body = {
    "id": "1",
    "jsonrpc": "2.0",
    "method": "GetBalance",
    "params": []
}

zil_api = "https://api.coingecko.com/api/v3/coins/zilliqa?community_data=false&developer_data=false&sparkline=false"

def get_zilliqa_price():
    req = requests.get(zil_api)
    result = req.json()

    return result['market_data']['current_price']['usd']


def main():
    parser = argparse.ArgumentParser(description='Check the balance of multiple Zilliqa addresses.')
    parser.add_argument('--file', default="addresses",
        help='Specify the file containing a list of addresses to read from.')

    args = parser.parse_args()
    print_balances(args.file)


def print_balances(filename):
    addresses = open(filename).read().strip().split("\n")
    total = 0
    pool = multiprocessing.Pool(40)
    results = pool.map(get_balance, addresses)
    for address, current_bal in zip(addresses, results):
        print("%s: %f" % (address, current_bal/DENOMINATOR))
        total += current_bal

    current_price = get_zilliqa_price()
    zils = total/DENOMINATOR
    print("Total: %f ($%.2f USD)" % (zils, zils * current_price))


def get_balance(address):
    current_body = copy.deepcopy(body)
    current_body['params'].append(address)
    req = requests.post("https://api.zilliqa.com/", json=current_body)
    result = req.json()

    if "result" not in result:
        return 0

    return int(result['result']['balance'])


if __name__ == '__main__':
    main()
