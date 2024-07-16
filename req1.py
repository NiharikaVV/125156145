import requests
url='http://20.244.56.144/test/auth'
payload={
    "companyName":"Sastra",
    "clientID":"6c861520-f18c-48ff-b8be-33e50616bf2a",
    "clientSecret": "zstoislwnPOIYyvY",
    "ownerName":"Venkamsetty Venkata Niharika",
    "ownerEmail":"125156145@sastra.ac.in",
    "rollNo":"125156145"
    
    
    
}
response=requests.post(url,json=payload)
if response.status_code in [200, 201]:
    # Parse the JSON response
    data = response.json()
    print("Token Type:", data.get("token_type"))
    print("Access Token:", data.get("access_token"))
    print("Expires In:", data.get("expires_in"))
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)  # Print the response body for debugging