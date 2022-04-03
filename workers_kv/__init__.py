import json

import requests


class Namespace:
    def __init__(self, account_id: str, namespace_id: str, api_key: str):
        """
        Namespace class for the KV store
        """
        self.account_id = account_id
        self.namespace_id = namespace_id
        self.request_headers = {"Content-Type": "application/json",
                                "Authorization": f"Bearer {api_key}"}
        self.request_base_url = (
            f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/storage/kv/namespaces/{self.namespace_id}"
        )

    def list_keys(self):
        """
        List all keys in the namespace
        """
        url = f"{self.request_base_url}/keys"
        response = requests.get(url, headers=self.request_headers)
        if "success" not in response.json():
            raise Exception(response.json()["error"])
        elif response.json()["success"] is not True:
            raise Exception(response.json()["errors"])

        res_body = response.json()["result"]
        key_list = []
        for data in res_body:
            key_list.append(data["name"])
        return key_list

    def read(self, key: str):
        """
        Read a key-value pair from the namespace
        If value is a json object, returns dict or list.
        """
        url = f"{self.request_base_url}/values/{key}"
        response = requests.get(url, headers=self.request_headers)
        try:
            res_body = response.json()
        except json.JSONDecodeError:
            # 正常時
            return response.content.decode()
        # エラー発生時
        if "errors" in res_body:
            raise Exception(res_body["errors"][0]["message"])
        else:
            return res_body

    def write(self, key_value_pairs: dict):
        """
        Insert a key-value pair(s) into the namespace
        """
        if len(key_value_pairs) == 1:
            self._write_one(key_value_pairs)
        else:
            self._write_multiple(key_value_pairs)
        return None

    def delete_one(self, key: str):
        """
        Delete a key-value pair from the namespace
        """
        url = f"{self.request_base_url}/values/{key}"
        response = requests.delete(url, headers=self.request_headers)
        if response.json().get("success") is not True:
            raise Exception(response.json()["errors"])
        return None

    def delete_multiple(self, keys: list):
        """
        Delete multiple key-value pairs from the namespace
        """
        if len(keys) > 10000:
            raise Exception("Too many keys to delete")
        url = f"{self.request_base_url}/bulk"
        response = requests.delete(url, headers=self.request_headers, json=keys)
        if response.json().get("success") is not True:
            raise Exception(response.json()["errors"])
        return None

    def _write_one(self, key_value_pair: dict):
        key = list(key_value_pair.keys())[0]
        url = f"{self.request_base_url}/values/{key}"
        response = requests.put(url,
                                headers=self.request_headers,
                                data=key_value_pair[key]
                                )
        if response.json().get("success") is not True:
            raise Exception(response.json()["errors"])
        return None

    def _write_multiple(self, key_value_pairs: dict):
        if len(key_value_pairs) > 10000:
            raise Exception("Too many key-value pairs. "
                            "See https://api.cloudflare.com/#workers-kv-namespace-write-multiple-key-value-pairs "
                            "for a detail.")
        url = f"{self.request_base_url}/bulk"
        data = []
        for key in key_value_pairs:
            data.append({"key": key, "value": key_value_pairs[key]})
        response = requests.put(url,
                                headers=self.request_headers,
                                json=data
                                )
        if response.json().get("success") is not True:
            raise Exception(response.json()["errors"])
        return None
