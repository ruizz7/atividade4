from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "united-creek-382823",
  "private_key_id": "2c4b5ef271fa7484fa3c003a55128afb994acf61",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7RXxhM3rFv37H\nkwH2QgT6lfCoWHv3/Owq86/iwpdhFK+Tch+D37f/dJP6N9xOoCveKoCe14sXfUP6\nySe9jxEE1v3A3QGEBUK03UfdpPMNq9ap//M3lw/z4i1Naxos1cVEWS0sLIgdTPgf\n1XiJ6kMHKRngIIkwqKaEgQVsV7smZlRg5r5IS1R+oFO3fc7I/dtcQpDug6+YcuJ2\nkIjs52iqvwqCOYgDFt/DbQ/H5ajvcflcRlZVdH4KviatHcDY0yCyWv4C6IwisGFA\ndCbM3qZ2tupWAyvRkBB0UNy4Vq3nk+RcJmv5Pz4LhFs3aICD/nEmmz5tAVP+uads\npVEfJnaRAgMBAAECggEALtqyxOsJY6KGyM4aJo/cCQosvSHuWlx4hkKUFgsTruFr\nEFv0UJ1PvuVfBLKnNzDR6PL/XT6WeVkJAh0ECWRbILfdozxoXaynRPM8QNM9UIVW\n3w+/vX/ZKO7E4OLUGLWfdntNVwkJQTN5vRU+5FqtTIRXCgF58aewieRyA+prU67G\nyGn9s9Fek9a/CtBEp8leozSj4OgJ0+OpxyZswweFNjXUA75i5sxoXOLxycnpPCmy\nhTuDI/fxFcwTNFvFMDqyo6+KPuXXwNS97Fm1Qndsxcl+34ZZCAne0+SKb6KCOHVr\nXEosmK/6C3fsAM0+4hoNkc0uCC+tdwXlZx5wEIOUJQKBgQDqmHJTcJVwE8kAmcCI\nSfxjc7zO+YbypdIIRrS8MbBLqKApVm7/aJQ+yKyheXzzjfPKmvYJNFIs7CTxNSYZ\nM4V2Yk82p/bFmdmYdUNdTpRfyh6dDtNy/EdWGDEGmHJdNbuxUt/IIQ6pttZG7h/g\nYblZZtWYGXBBCcoJFokMpJ/3GwKBgQDMW6trNGbG6ACbNNtWg4hyy0KXQ3kgvqVy\nlaZP8r60gG0QY+mHufMBgfe8X55qYG6rLFJvNEoY0xPoidwfDQ0L9q021oxQihyL\nmz//9ocdXCOSWRM0ZqOYb/ZVPV6McdakE3ptx7mhkDYexEKmm5C1tET9IHidUgdD\n1G8+49qHwwKBgQCTDoEMIRTsLtrfT4JLbOWTiiefLvgS/zNMENaW6ibzJn9Pqmjm\nHi5ftPfSOQ/EtQVPyhfU6UFh+52kvoZlYdCVx0aUonGkqK6oTUmvIeUMruzF01dl\nSxOEuqFw2vtFxrsjiynQkDha1sw3pmnBBEFl83qNX9ToUDSfwcqjbEcCZQKBgCFA\nqVwAYtjq125p42bocEN9n5BNgmA5pWJHx5Aqx61HWHfaSh2zvD76jv0v8e8NUfS4\neZFuyL/RWOP1ysOitATGVtkdgCd60bpFwNw9mS7F12Pw6pcUPHqJfWPRYJkpzOtV\n4A4M+b+4X5YSCWZi2eE3PCKULgwrVNNMte1d1ilRAoGBAKEfzd2sVZ1BzQ+00YiM\nbrCNiUKue81VkEmDfD0adkz7i2RVp/kOlyn4cIc8ithHJQ/fPQldcKOcMeEunsgO\nwfft2Shd8qCp+QZ1m+GaelzffJyw2p75bifgrg7rN91AGm8sRgCmo69JfmjwSmZ+\nyYXHejr6zQlOAMcKSKiWhCQg\n-----END PRIVATE KEY-----\n",
  "client_email": "922093530067-compute@developer.gserviceaccount.com",
  "client_id": "114410630456998633776",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/922093530067-compute%40developer.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names_mari') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
