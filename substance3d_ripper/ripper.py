import os
import time
import httpx

from .constants import COLLECTION_QUERY
from .types import UserInfo, Collection


class Substance3DRipper:
    def __init__(self, ims_sid: str):
        self.session = httpx.Client(follow_redirects=True, timeout=30.0)
        self.session.headers.update(self._get_default_headers())
        self.session.cookies.set("ims_sid", ims_sid)

        self.access_token = None
        self.output_dir = "substance3d_ripper_output"

        self._ensure_output_dir()

    def _ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _get_default_headers(self):
        default_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Origin": "https://substance3d.adobe.com/",
            "Referer": "https://substance3d.adobe.com/",
        }

        return default_headers

    def handle_error(self, response):
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            error_message = (
                f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
            )
            raise Exception(error_message)
        except httpx.RequestError as e:
            raise Exception(f"Request error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

    def _gen_session(self, user_id: str = None) -> UserInfo:
        url = "https://adobeid-na1.services.adobe.com/ims/check/v6/token?jslVersion=v2-v0.31.0-2-g1e8a8a8"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }

        payload = {
            "client_id": "substance-source",
            "scope": "account_type,openid,AdobeID,read_organizations",
        }

        if user_id:
            payload["user_id"] = user_id

        response = self.session.post(url, headers=headers, data=payload)
        self.handle_error(response)
        data = response.json()
        user_info = UserInfo.from_dict(data)
        self.access_token = user_info.access_token
        return user_info

    def gen_session(self) -> UserInfo:
        user_info_1 = self._gen_session()
        if not user_info_1.access_token:
            raise ValueError(
                "Failed to retrieve access token. Please check your IMS session ID."
            )
        user_info_2 = self._gen_session(user_id=user_info_1.userId)
        if not user_info_2.access_token:
            raise ValueError(
                "Failed to retrieve access token with user ID. Please check your IMS session ID."
            )
        return user_info_2

    def get_collection(
        self, collection_id: str, limit: int = 60, page: int = 0
    ) -> Collection:
        url = "https://source-api.substance3d.com/beta/graphql"
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "operationName": "Collection",
            "variables": {
                "limit": limit,
                "sort": "sameAsIds",
                "sortDir": "asc",
                "id": collection_id,
                "page": page,
            },
            "query": COLLECTION_QUERY,
        }

        response = self.session.post(url, headers=headers, json=payload)
        self.handle_error(response)
        data = response.json()
        collection_dict = data.get("data", {}).get("collection", {})
        if not collection_dict:
            raise ValueError(f"Collection with ID {collection_id} not found.")

        collection = Collection.from_dict(collection_dict)
        return collection

    def download_asset(self, asset_url: str, filename: str = None) -> None:
        url = f"{asset_url}?accessToken={self.access_token}"

        response = self.session.get(url)
        self.handle_error(response)

        filename_header = response.headers.get("Content-Disposition")
        original_filename = (
            filename_header.split("filename=")[-1].strip('"')
            if filename_header
            else f"downloaded_asset_{int(time.time())}.unknown"
        )
        use_filename = filename if filename else original_filename

        file_path = os.path.join(self.output_dir, use_filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
