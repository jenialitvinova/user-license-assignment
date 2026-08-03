from pprint import pprint

from app.api_client import get_licenses

licenses = get_licenses()

print(type(licenses))
print()

for item in licenses:
    pprint(item)