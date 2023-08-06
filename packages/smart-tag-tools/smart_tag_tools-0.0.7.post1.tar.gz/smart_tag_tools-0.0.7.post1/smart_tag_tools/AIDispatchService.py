#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
import time

"""
    {
        "accesstoken": "classification",
        "type": "nlp/classification",
        "version": "1.0",
        "params": {},
        "files": [
            {
                "type": "text",
                "id": "uuid_1",
                "txt": "海军陆战队训练"
            },
            {
                "type": "text",
                "id": "uuid_2",
                "txt": "来自全国各地的医生团体"
            }
        ],
        "callback": ["http://172.16.139.24:2000/sobey/AI/Result"],
        "userdata": {}
    }
    """


def callback(func_2=None, *args_, **kwargs_):
    """
    三层嵌套, 第一层callback是工厂, 获取func_2和它的参数
    decorator和inner就是正常的装饰器, 捕获func_1及其参数.
    :param func_2:      The callback function.
    :param args_:       Parameters of func_2.
    :param kwargs_:     Parameters of func_2.
    :return:
    """

    def decorator(func_1):
        def inner(*args, **kwargs):
            res = func_1(*args, **kwargs)
            result = None
            if func_2:
                kwargs_.update({'callback_url': res['taskurl']})
                result = func_2(*args_, **kwargs_)
            return result

        return inner

    return decorator


def get_result(callback_url: str):
    while True:
        time.sleep(2)
        try:
            res = requests.get(callback_url, timeout=5).json()
            if res.get('code') == 0:
                # 任务已完成，判断每个file是不是执行成功。失败的话，直接抛异常
                if res['data']['taskStatus'] == 0:
                    for file_task in res['data']['results']:
                        if file_task['statusCode'] != 0:
                            raise Exception('单个file执行失败:{}'.format(file_task['statusInfo']))
                    return res['data']['results']
            else:
                raise Exception('查询任务失败:{}'.format(res.get("message")))
        except Exception as error:
            raise error


# noinspection PyDefaultArgument
@callback(get_result)
def analysis(url, typ, access_token, version, files, params={}, user_data={}):
    data = {
        "accesstoken": access_token,
        "type": typ,
        "version": version,
        "params": params,
        "files": files,
        "callback": ["http://172.16.139.24:2000/sobey/AI/Result"],
        "userdata": user_data
    }
    try:
        res = requests.post(url, json=data, timeout=5).json()
        if res['code'] == 0:
            return res['data']
        else:
            raise Exception('添加任务失败:{}'.format(res.get('msg')))
    except Exception as error:
        raise error

# d = {
#     'url': 'https://ai-dispatch.sobeylingyun.com/api/task',
#     'version': '1.0',
#     'typ': 'nlp/keywords',
#     'access_token': 'key',
#     'files': [
#         {
#             "type": "text",
#             "id": "uuid_1",
#             "txt": "海军陆战队训练"
#         },
#         {
#             "type": "text",
#             "id": "uuid_2",
#             "txt": "来自全国各地的医生团体"
#         }
#     ]
# }
# print(analysis(**d))
