import requests
response = requests.get("https://google.com", timeout=5)
print(f"Status Code: {response.status_code}")
