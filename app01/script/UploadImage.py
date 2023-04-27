import requests
import json
import time
import random
import os
def upload(path):
    headers = {'Authorization': 'oRGeqRIQfgb76RqTFVqyfilV0hngQUgD'}
    files = {'smfile': open(path,'rb')}
    url = 'https://smms.app/api/v2/upload'
    res = requests.post(url,files=files,headers=headers).json()
    if res['success']=='True':
        print(res['url'])
    else:
        print(res['images'])

if __name__ == "__main__":
    dir  = "../media"

    sample_tree =os.walk(dir)
    for dirname,subdir,files in sample_tree:

        print("档案串列",files)
        for x in files:
            #print(os.path.abspath(dir+"/"+x))
            upload(os.path.abspath(dir+"/"+x))

