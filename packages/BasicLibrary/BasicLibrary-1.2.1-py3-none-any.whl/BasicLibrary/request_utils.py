import requests
import json

################################
#封装的request和Response返回
_REQ="req"
_RESP="resp"
_URL="url"
_HEADER="header"
_PARAMS="params"
_METHOD="method"
_STATUS_CODE="status_code"
_BODY="body"

_METHOD_GET="GET"
_METHOD_POST="POST"
################################

session_req = requests.session()

def http_get(url, params=None, headers=None, timeout=None):
    if url is None:
        raise AssertionError('url参数是None!')
    try:
        response = session_req.get(url,headers=headers,params=params,timeout=timeout)
        # resAndRes = __get_req_and_resp_dict(params,headers,None,_METHOD_GET,response)
        Res = response.text
        resAndJosnDict = json.loads(Res)
        return resAndJosnDict
    except requests.exceptions.RequestException as e:
        raise AssertionError('发送请求失败，原因：%s'%e)

def http_post(url, params=None, headers=None, data=None,timeout=None):
    if url is None:
        raise AssertionError('url参数是None!')
    try:
        if headers is None:
            headers = {}
        headers.update({'Content-Type': 'application/json;charset=UTF-8'})
        if isinstance(data,str):
            data = json.loads(data)
        response = session_req.post(url,headers=headers,params=params,json=data,timeout=timeout)
        Res = response.text
        # resAndRes = __get_req_and_resp_dict(params,headers,data,_METHOD_POST,response)
        # resAndJosnStr = resAndRes.get('resp').get('body')
        resAndJosnDict = json.loads(Res)
        return resAndJosnDict
    except requests.exceptions.RequestException as e:
        raise AssertionError('发送请求失败，原因：%s'%e)

def __fill_req_dict(url,params,headers,body,method):
    req = {}
    req[_URL] = url
    req[_METHOD] = method
    req[_PARAMS] = params
    req[_HEADER] = headers
    body = str(body)
    req[body] = body
    return req

def __fill_resp_dict(response):
    resp = {}
    resp[_STATUS_CODE] = response.status_code
    resp[_HEADER] = response.headers
    resp[_BODY] = response.text
    return resp

def __get_req_and_resp_dict(params,headers,body,method,response):
    req_and_resp = {}
    url = response.url
    req = __fill_req_dict(url,params,headers,body,method)
    resp = __fill_resp_dict(response)
    req_and_resp[_REQ] = req
    req_and_resp[_RESP] = resp
    return req_and_resp
