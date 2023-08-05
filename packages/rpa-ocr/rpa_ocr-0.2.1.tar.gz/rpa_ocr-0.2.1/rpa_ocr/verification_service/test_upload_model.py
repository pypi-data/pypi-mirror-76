# -*- coding:utf-8 -*-
# @author :adolf
import requests
import json


def get_result(file_path):
    print(file_path)
    files = {'file': open(file_path, 'rb')}
    r = requests.post("https://rpa-vc-upload.ai-indeed.com/upload_service/", files=files)
    res = json.loads(r.text)
    print(res)
    return res


# file_path = "model/dazongguan_verification.pth"
file_path = 'model/shandong_verification.onnx'

get_result(file_path)
