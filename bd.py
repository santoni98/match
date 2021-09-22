import requests

AIRTABLE_BASE_ID = "app73rMbUcl0A2i6A"
AIRTABLE_API_KEY = "key516PDNmFwGdQMg"
AIRTABLE_TABLE_NAME = "pytable"

endpoint = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"


# # Python request headers
# headers = {
#     "Authorization": f"Bearer {AIRTABLE_API_KEY}",
#     "Content-Type": "application/json",
# }
#
# data = {
#     "records": [
#         {
#             "fields": {
#                 "Name": "Just",
#                 "username": "barmaley9",
#                 "City": "saint",
#                 "Status": "Done"
#             }
#         },
#         {
#             "fields": {
#                 "Name": "Just",
#                 "username": "barmaley9",
#                 "City": "saint",
#                 "Status": "Done"
#             }
#         }
#     ]
# }


def add_to_airtable(name="", username="", link="", city="", theme="", status=""):

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "records": [
            {
                "fields": {
                    "Name": name,
                    "username": username,
                    "link": link,
                    "City": city,
                    "Theme": theme,
                    "Status": status
                }
            }
        ]
    }
    r = requests.post(endpoint, json=data, headers=headers)
    return r.status_code == 200
