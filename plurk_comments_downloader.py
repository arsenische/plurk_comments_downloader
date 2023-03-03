from plurk_oauth import PlurkAPI
from datetime import datetime, timedelta
import os
import urllib.parse
import re
import time
import numpy as np

class PlurkCommentsDownloader:
    def __init__(self, api_key_path="API.keys", plurk_dir="plurks", plurk_offset=datetime.now(), plurk_offset_step=timedelta(hours=24), plurk_users={}):
        self.api = PlurkAPI.fromfile(api_key_path)
        if not os.path.exists(plurk_dir):
            os.makedirs(plurk_dir)
        self.plurk_dir = plurk_dir
        self.plurk_offset = plurk_offset
        self.plurk_offset_step = plurk_offset_step
        self.plurk_users = plurk_users

    def replace_user_links_with_mentions(self, message):
        user_link_pattern = r'<a href="https://www\.plurk\.com/(\w+)" class="ex_link">.*?</a>'
        for match in re.finditer(user_link_pattern, message):
            user_id = match.group(1)
            message = message.replace(match.group(0), f"@{user_id}")
        return message

    def plurk_api_call(self, api_url, params):
        url_params = urllib.parse.urlencode(params)
        url = f"{api_url}?{url_params}"
        print(f"\nRequest URL: {url}")
        response = self.api.callAPI(api_url, params)
        err = self.api.error()
        if err['code']!=200:
            print(err)
        time.sleep(0.1)
        return response

    def get_nick_names(self, users):
        for user_id, user_info in users.items():
            self.plurk_users[int(user_id)] = user_info["nick_name"]
        return self.plurk_users


    def get_nick_name(self, user_id):
        if user_id not in self.plurk_users:
            print(f"{user_id} not in {self.plurk_users}")
            response = self.plurk_api_call("/APP/Profile/getPublicProfile", {"user_id": user_id})
            self.plurk_users[user_id] = response["user_info"]["nick_name"]
        return self.plurk_users[user_id]

    def download_plurk_comments(self):
        while True:
            params = {"minimal_data": "true", "minimal_user": "true", "offset": self.plurk_offset.strftime('%Y-%m-%dT%H:%M:%S'), "limit": 30}
            self.plurk_offset -= self.plurk_offset_step
            response = self.plurk_api_call("/APP/Timeline/getPlurks", params)
            if not response["plurks"]:
                print(f"No plurks for {params}")
                break

            self.get_nick_names(response["plurk_users"])

            for plurk in response["plurks"]:
                plurk_id = plurk["plurk_id"] 
                plurk_id_str = np.base_repr(plurk_id, base=36)
                print(f" {plurk_id_str} ", end='')
                filename = f"{self.plurk_dir}/{plurk_id}.{plurk_id_str}.txt"
                if os.path.exists(filename):
                    continue
                responses = self.plurk_api_call("/APP/Responses/get", {"plurk_id": plurk_id, "minimal_data": "true"})

                self.get_nick_names(responses["friends"])

                print(f"\nCreating {filename}...", end='')
                with open(filename, "w") as f:
                    nick_name = self.get_nick_name(plurk["owner_id"])
                    f.write(f"{nick_name}: {self.replace_user_links_with_mentions(plurk['content'])}\n")

                    for comment in responses["responses"]:
                        nick_name = self.get_nick_name(comment["user_id"])
                        f.write(f"{nick_name}: {self.replace_user_links_with_mentions(comment['content'])}\n")
                print(f"...created!")

        print(str(response)[:400])

#downloader = PlurkCommentsDownloader(plurk_offset=datetime(2022, 1, 1, 0, 0, 0), plurk_offset_step=timedelta(hours=6))
downloader = PlurkCommentsDownloader()
downloader.download_plurk_comments()
