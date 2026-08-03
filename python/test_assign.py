from app.api_client import assign_license

USER_ID = "2aa5c500-237f-5351-8e3f-41b5881bc8c3"
LICENSE_ID = "11111111-1111-1111-1111-111111111111"

try:
    result = assign_license(USER_ID, LICENSE_ID)
    print(result)
except Exception as e:
    print(e)