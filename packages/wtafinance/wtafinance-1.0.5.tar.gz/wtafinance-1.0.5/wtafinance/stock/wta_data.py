from wtafinance.finance_api import stock


def wta_api(secret_key,secret_id):
    instance = stock.DataApi(secret_key,secret_id)
    return instance