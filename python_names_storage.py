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
  "project_id": "round-bloom-384323",
  "private_key_id": "304e51cbc247d85b31f9c6cd4f46d46b63fc5a2f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9Dbsb3Mz77dWa\nCxiI4WOXeDBxvkrnR4Jh0zk4V+Oxrd+6pF6OkKTyPxyVaF5+EUJeEA88xWkkgUhD\nr+ralCKaC3rRwVHlJJdJhmdyi7k0MiynzfELhXIBg/Pr+Im6GnZkdwoLQ3eSL+h3\nOE4BNMtreq/qUfaTJYl2HRNcbNTMveEsdUzsKdK5SMrFrT8xFPi9r2HyYYOZ9sni\nclMw6+jpxy16+O8Dk1BVL6qp3udQ0QbXIkcgq6Q/qeZAut0H2PWSJ2cVO0ZTEKpw\na5i5ZT6UcX1TugVWtL5ZFQvnW4+JNtBESrI+MW8q9JMp3+aQOZzD3haIOwJsEnoq\n+3bQ9tw5AgMBAAECggEARqW7brmP5nMlt8d+tyQW7fMNk2vLnOr1l63xu5LodSzn\nJt2msjruUNJx0YlrikvT08fHkeupk2k2gojaSC1EUvGIR5spCeqnGGRAAyegoZdA\nZcLJWYdYJ6XSQLOjcCbUaE2ttLDVHY2Gnwqs57l9bOAvne5cKPfFixxpcEgBK7MC\n2zM/lD3FMtkJusGT37URgg197lKYbjC4hhtrqogdNqmUjuJwxtkL9tHo9fka1e4l\nHFO7Yk/oOf2ieBQzbs34DKvRO/3cMIhQX7OlKw+i7yhRSSGHQiXt0XNViOzzRkQ5\ncahMxtByO7EZP5djRttC+xFcbSOawHJ4pjHrByBsAwKBgQDhPhHG4mGgOfCzpOGH\nifLuSIvF/KBDrZUiJESusR9QvmUrWNXqx8wmesZH+w59Lr+nqcDgpFKDs0kGyQuH\neIn2wbkVG2Y1Esgamt3JsULFiNoGUXVpJQfTyy/K3W0sGfmSY2SRtAk7P/HSPnWB\n2AsUhcqoEejqet2R8l416DJtlwKBgQDW3paBXaX1f14lpkcdNNG3rcIJGh7mqB3J\nZJtZenG+mjVDBrE+eYv6+lorDD4dreHyKbKKMAcLVxh0aRnkbooSfD5c2Vvk2QXr\nZbopjDNIBybW2m72NV+14fkQDZxfMDZx7j1bvT5w7lDP7vKCTIqP+Wq0NG9U8LqN\nqNkIONPerwKBgBJnivZQSx/XfCaBo3f6uqHjxaAA22uMRHJMulv31xI27HdVQ+1y\nM+k1APyis/Vgm4JsqXjxlFh0jtQCG3IPVF6YR7JE0d4mUblyzAqN9GHFo+L+RvS3\ndONGZ/pQi3oeCTl/65jIODTiLbU7K0jXyVf88qk3BWwba/1f63jGJ1CzAoGBAIKm\n8klTUliGzA6EnvVJasQPac7zDRsf2ozdGgE8jPFi/0P0S847RjykAjPuy85sLtl7\nNU8FiSMCIKKYTeAyvs4isiDvIgtzU0AhqSMeVwhTIPC//XzEU6Ba+YEjZZQT0udQ\nAAtKdS9iGc119Av60r5c4N8WiyPRBP6iTuXK+DmNAoGAKALgEkiJW63hlcJiU+oK\nUAnUU+HeoNcn/+IQ9LnySGVkIW9eDnHAi1w461PMi2Sa4aZAAYHDZ70XxZ0l3oK1\nGHaAX35H4RBsfbGco9cacN2ojRhG7+qQoF9R3qco4OBVaMybMgT5+RlrvyDUQz4S\n8/bbuHjA6aDLGpGfHhhKjnI=\n-----END PRIVATE KEY-----\n",
  "client_email": "263674655995-compute@developer.gserviceaccount.com",
  "client_id": "116555595654426463862",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/263674655995-compute%40developer.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atividade4igorr') ### Nome do seu bucket
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
