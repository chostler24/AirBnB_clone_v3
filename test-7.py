#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ DELETE /api/v1/states/<state_id>
    """
    r = requests.delete("http://0.0.0.0:5050/api/v1/states/{}".format("doesn_t_exist"))
    print(r.status_code)
