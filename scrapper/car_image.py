import requests
from bs4 import BeautifulSoup as bs
from urllib import parse

def get_img_url(query:str):
	q = f"{query} filetype:jpg"
	q = [("q", q), ("oq", q)]
	q = parse.urlencode(q, encoding="UTF-8")

	url = f"https://www.google.com/search?{q}&sca_esv=2e9f397e799003ae&as_st=y&imgsz=m&imgar=s&udm=2&sxsrf=AHTn8zrR56N4tZG016O6xgUwmjmu6h6X3Q%3A1745736401833&ei=0dINaJPRMrGmvr0PnpL8qAY&ved=0ahUKEwjT_ejwzveMAxUxk68BHR4JH2UQ4dUDCBE&uact=5&gs_lp=EgNpbWciJzIwMjXrhYTsi50gRm9yZCBCcm9uY28gNFdEIGZpbGV0eXBlOmpwZ0iY8gFQAFjJ6QFwCXgAkAEAmAHuAaAB4x-qAQYwLjE5LjW4AQPIAQD4AQH4AQKYAgCgAgCYAwCSBwCgB7gIsgcAuAcA&sclient=img"
	resp = requests.get(url)
	print(resp.text)
	soup = bs(resp.text, "html.parser")
	first_img = soup.select_one("body > div + div > table tr > td > div > div > div > div > table tr > td > a > div > img")
	return first_img.attrs["src"]

if __name__ == "__main__":
	print(get_img_url("2024년식 Ford Bronco 4WD"))