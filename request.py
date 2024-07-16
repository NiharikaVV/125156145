import requests
url='http://20.244.56.144/test/register'
payload={
    "companyName":"Sastra",
    "ownerName":"Venkamsetty Venkata Niharika",
    "rollNo":"125156145",
    "ownerEmail":"125156145@sastra.ac.in",
    "accessCode":"LGcHvG"
    
}
response=requests.post(url,json=payload)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")