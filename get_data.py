import requests
import json
import komoot

email = "test@example.com"
password = "123456"
client_id = "111111111111"
login_url = "https://account.komoot.com/v1/signin"
tour_url = f"https://www.komoot.de/user/{client_id}/tours"

s = requests.Session()

res = requests.get(login_url)
cookies = res.cookies.get_dict()

headers = {
	"Content-Type": "application/json"
}

payload = json.dumps({
	"email": email,
	"password": password,
	"reason": "null"
})

s.post(login_url, headers=headers,
	   data=payload, cookies=cookies)

url = "https://account.komoot.com/actions/transfer?type=signin"
s.get(url)

headers = {"onlyprops": "true"}

response = s.get(tour_url, headers=headers)
if response.status_code != 200:
	print("Something went wrong...")
	exit(1)
data = response.json()

tours = data["kmtx"]["session"]["_embedded"]["profile"]["_embedded"]["tours"]["_embedded"]["items"]


for idx in range(len(tours)):
	print(f"({idx+1}) {tours[idx]['name']}")


tour_nr = int(input("Tour ID: "))
tour_id = tours[tour_nr-1]['id']
tour_url = f"https://www.komoot.de/tour/{tour_id}"
response = s.get(tour_url, headers=headers)
tour_data = json.loads(response.text)

T = komoot.Tour(tour_data)
print("Title:", T.name())
print(f"Duration: {T.duration()}s")
