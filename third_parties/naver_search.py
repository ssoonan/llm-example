import requests
import os


def fetch_naver_data(stock_symbol):
    naver_api_url = f"https://openapi.naver.com/v1/search/news.json?query={stock_symbol}&sort=date&display=50"
    response = requests.get(naver_api_url, headers={"X-Naver-Client-Id": os.environ["NAVER_CLIENT_ID"], "X-Naver-Client-Secret": os.environ["NAVER_CLIENT_SECRET"]})
    return response.json()['items']