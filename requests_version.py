#!/usr/bin/env python3
import requests

res = requests.get("http://www.google.com/")

print(res.text)