import json
import warnings

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

        Returns:
            keys (list): list of keys in the namespace
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
        If nothing matches, returns None.

        Args:
            key (str): key to be read

        Returns:
            value (str or dict or list): value of the key
        """
        url = f"{self.request_base_url}/values/{key}"
        response = requests.get(url, headers=self.request_headers)
        if response.status_code == 404:
            return None
        try:
            res_body = response.json()
        except json.JSONDecodeError:
            # 正常時
            return response.content.decode()
        if not isinstance(res_body, dict):
            return res_body
        # エラー発生時
        if "errors" in res_body:
            raise Exception(res_body["errors"][0]["message"])
        else:
            return res_body

    def write(self, key_value_pairs: dict):
        """
        Insert a key-value pair(s) into the namespace

        Args:
            key_value_pairs (dict): key-value pair(s) to be inserted

        Returns:
            None
        """
        if len(key_value_pairs) == 1:
            self._write_one(key_value_pairs)
        else:
            self._write_many(key_value_pairs)
        return None

    def delete_one(self, key: str):
        """
        Delete a key-value pair from the namespace

        Args:
            key (str): key to be deleted

        Returns:
            None
        """
        url = f"{self.request_base_url}/values/{key}"
        response = requests.delete(url, headers=self.request_headers)
        if response.json().get("success") is not True:
            raise Exception(response.json()["errors"])
        return None

    def delete_multiple(self, keys: list):
        warnings.warn("delete_multiple() is deprecated and should be removed in version 2.0. Use delete_many() instead.",
                      DeprecationWarning)
        return self.delete_many(keys)

    def delete_many(self, keys: list):
        """
        Delete multiple key-value pairs from the namespace

        Args:
            keys (list): list of keys to be deleted

        Returns:
            None
        """
        if len(keys) > 10000:
            raise Exception("Too many keys to delete")
        keys = [str(key) for key in keys]
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

    def _write_many(self, key_value_pairs: dict):
        if len(key_value_pairs) > 10000:
            raise Exception("Too many key-value pairs. "
                            "See https://api.cloudflare.com/#workers-kv-namespace-write-multiple-key-value-pairs "
                            "for a detail.")
        url = f"{self.request_base_url}/bulk"
        data = []
        for key in key_value_pairs:
            value = json.dumps(key_value_pairs[key]) \
                if type(key_value_pairs[key]) in (list, dict) else str(key_value_pairs[key])
            data.append({"key": str(key), "value": value})
        response = requests.put(url,
                                headers=self.request_headers,
                                json=data
                                )
        if response.json().get("success") is not True:
            raise Exception(response.json()["errors"])
        return None
