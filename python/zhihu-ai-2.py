import requests
import os
import base64
import json
import time


def get_img_base(file):
    with open(file, 'rb') as fp:
        content = base64.b64encode(fp.read())
        return content


ak = 'GShVT9eIIVs2mLSF89aVntDV'
sk = 'mZx5M2UwMU4CwcicCl1Th23mdflcZ9hS'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
    ak, sk)
res = requests.post(host)
json_result = json.loads(res.text)
token = json_result['access_token']

file_path = 'row_img'
list_paths = os.listdir(file_path)
for i in range(10):
    p = f'{i}分'
    if not os.path.exists(p):
        os.mkdir(p)
p = '其他分'
if not os.path.exists(p):
    os.mkdir(p)

for list_path in list_paths:
    time.sleep(2)
    img_path = file_path + '/' + list_path
    # print(img_path)

    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    request_url = request_url + "?access_token=" + token

    params = {
        'image': get_img_base(img_path),
        'image_type': 'BASE64',
        'face_field': 'age,beauty,gender'
    }

    res = requests.post(request_url, data=params)
    json_result = json.loads(res.text)
    code = json_result['error_code']
    print(json_result)
    if code == 222202:
        continue

    try:
        gender = json_result['result']['face_list'][0]['gender']['type']
        if gender == 'male':
            continue
        beauty = json_result['result']['face_list'][0]['beauty']
        new_beauty = round(beauty / 10, 1)
        print(img_path, new_beauty)
        if new_beauty >= 8:
            os.rename(
                os.path.join(file_path, list_path),
                os.path.join('8分',
                             str(new_beauty) + '+' + list_path))
        elif new_beauty >= 7:
            os.rename(
                os.path.join(file_path, list_path),
                os.path.join('7分',
                             str(new_beauty) + '+' + list_path))
        elif new_beauty >= 6:
            os.rename(
                os.path.join(file_path, list_path),
                os.path.join('6分',
                             str(new_beauty) + '+' + list_path))
        elif new_beauty >= 5:
            os.rename(
                os.path.join(file_path, list_path),
                os.path.join('5分',
                             str(new_beauty) + '+' + list_path))
        else:
            os.rename(
                os.path.join(file_path, list_path),
                os.path.join('其他分',
                             str(new_beauty) + '+' + list_path))
    except KeyError:
        pass
    except TypeError:
        pass
