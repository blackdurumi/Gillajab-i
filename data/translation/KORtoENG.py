# code reference: https://developers.naver.com/docs/papago/papago-nmt-example-code.md#python

import os
import sys
import json
import urllib.request
client_id = "PEDMV9jlEiGwITMbVl9S" # 개발자센터에서 발급받은 Client ID 값
client_secret = "0y7PXg98mI" # 개발자센터에서 발급받은 Client Secret 값

def translate(korstring):
    string = korstring

    encText = urllib.parse.quote(string)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode==200:
        response_body = json.load(response)
        print(response_body['message']['result']['translatedText'])
    else:
        print("Error Code:" + rescode)