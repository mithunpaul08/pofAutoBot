import requests

url="https://www.okcupid.com/login"

payload={
    "username":"mpaul588",
    "password":"Alohomora1"
}

session=requests.session()
response=requests.get(url).content
print(response)


