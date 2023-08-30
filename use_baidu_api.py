import requests


'''
规则：
每月免费使用一千次
48块钱买十万次，有效期12个月
（1s一次调用的话，一小时3600次，烧2块钱）
（1s一次调用的话，一天要烧掉86400次，一天花完48）
先用numpy进行人脸检测，检测到人脸后再调用api接口，会省很多钱
'''
def baidu_api(image):
    try:

        url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        request_url = url + "?access_token=" + get_Token()

        params = {
            "image": image,
            "image_type": "BASE64",
            "group_id_list": "2005",
            "quality_control": "LOW",
            "liveness_control": "NORMAL"
        }

        headers = {
            'Content-Type': "application/json",
        }

        response = requests.post(url=request_url, data=params, headers=headers)
        return response.json()
    except:
        print("Ui_FirstForm.baidu_search")
        pass


def baidu_api(image,token):
    try:

        url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        request_url = url + "?access_token=" + token

        params = {
            "image": image,
            "image_type": "BASE64",
            "group_id_list": "2005",
            "quality_control": "LOW",
            "liveness_control": "LOW"
        }

        headers = {
            'Content-Type': "application/json",
        }

        response = requests.post(url=request_url, data=params, headers=headers)
        return response.json()
    except:
        print("Ui_FirstForm.baidu_search")
        pass

def get_Token():
    try:
        AK = 'x1fQaRD*******8sUqG68A'  # 填写的你API Key
        SK = 'Mbwy*****************LTSjZz'  # 填写你的Secret Key
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
            AK, SK)
        response = requests.get(host)
        return response.json()['access_token']
    except:
        pass
        print("Ui_FirstForm.get_Token")

if __name__=="__main__":
    str=get_Token()
    print(str)