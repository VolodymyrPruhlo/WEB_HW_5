import aiohttp
import asyncio
import datetime
import sys
import json


async def fetch_currency_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            data = await response.json()
            result = {
                'EUR': {'sale': None, 'purchase': None},
                'USD': {'sale': None, 'purchase': None}
            }
            for ex in data['exchangeRate']:
                if 'currency' in ex and ex['currency'] in result:
                    result[ex['currency']]['sale'] = ex.get('saleRate')
                    result[ex['currency']]['purchase'] = ex.get('purchaseRate')
            return {date: result}


async def main():
    if len(sys.argv) < 2:
        print("Please provide the number of days as an argument")
        sys.exit(1)

    number_of_days = None

    try:
        number_of_days = int(sys.argv[1])
    except ValueError:
        print('Days should be a integer')
        sys.exit(1)

    if number_of_days > 10:
        print('Out of limit days, pls use under 10')
        sys.exit(1)

    base_date = datetime.datetime.now()
    dates = [(base_date - datetime.timedelta(days=i)).strftime('%d.%m.%Y') for i in range(number_of_days)]

    tasks = [fetch_currency_rates(date) for date in dates]
    results = await asyncio.gather(*tasks)
    formatted_results = [result for result in results if any(result.values())]

    for result in formatted_results:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
