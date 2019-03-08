import requests
from lxml import etree
import json
import time
import re
import os


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'cookie': '_zap=ca6bcaa0-a5f4-4f8c-997e-c5a7f0c63144; d_c0="ANDgu05DCw-PTp7PXKA61Q9-5C5UFbBZqvI=|1551233879"; q_c1=4ebe94900b1440058d6bb0e0d6349b4e|1551233883000|1551233883000; _xsrf=c506084c-3f58-47c0-adcc-793014a67d29; capsion_ticket="2|1:0|10:1551368018|14:capsion_ticket|44:YzQxNzAwZjhlZjgxNGM2Nzk2ZmE5OGQ5NTdkOWJkODI=|0be4f94a4e1d049452dbb344a67d0beed79849f1e18ba36a0e528d9aaf245bb1"; z_c0="2|1:0|10:1551368020|4:z_c0|92:Mi4xSFp5c0FBQUFBQUFBME9DN1RrTUxEeVlBQUFCZ0FsVk5WRTFsWFFDMGlobzYtSmxaVmdQeGlPV0JMaHVpNTR0aFhB|a1aef353ef25e0abdd757884ebd78d2e14661a52fa5ac0ca0f7481cf7e73e1e5"; tgw_l7_route=060f637cd101836814f6c53316f73463'
}


def get_img(url):
    res = requests.get(url,headers=headers)
    i = 1
    json_data = json.loads(res.text)
    datas = json_data['data']

    for data in datas:
        id = data['author']['name']
        content = data['content']
        imgs = re.findall('img src="(.*?)"',content,re.S)

        if len(imgs) == 0:
            pass
        else:
            for img in imgs:
                if 'jpg' in img:
                    res_1 = requests.get(img, headers=headers)
                    if not os.path.exists('row_img'):
                        os.mkdir('row_img')
                    fp = open('row_img/' + id + '+' + str(i) + '.jpg','wb')
                    fp.write(res_1.content)
                    i = i + 1
                    print(id,img)

if __name__ == '__main__':
    urls = ['https://www.zhihu.com/api/v4/questions/29024583/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default'.format(str(i)) for i in range(0,25000,5)]
    for url in urls:
        get_img(url)
        time.sleep(2)
