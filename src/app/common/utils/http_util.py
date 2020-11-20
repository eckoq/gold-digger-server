#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests

from werkzeug.exceptions import HTTPException
from app.common.error import ERR_OK, ERR_CALL_API_TIMEOUT, ERR_API_CONNECTION_REFUSED, ERR_API_RETURN_INVALID


class HttpRequests(object):
    # 封装Get方法，return响应码和响应内容
    """
    {
        "code": 0, // 0：只表示第三方API能正常返回，并且返回的消息格式是合法的。-1：表示调用第三方API异常，例如超时、断开、拒绝连接等。
        "error": "", // 当code不为0是，error不为空。error是系统内部的错误短语，不是API返回的错误短语。
        "api_code": 0, // API返回的错误码（如有，方便调用程序处理）
        "api_error":"",
        "api_response":{} // 第三方API返回的原始消息。（根据需要，可以是加工转换后的消息）
    }
        内部错误码
        -11000	访问第三方API超时
        -11001	第三方API服务器拒绝连接
        -11002	第三方API返回非法消息
    """

    @staticmethod
    def get(url, params=None, headers=None, timeout=120, error_key=None):
        try:
            response = requests.get(url=url, params=params, headers=headers, timeout=120)
            status_code = response.status_code
            response_json = response.json()
            # logger.info("Get请求的内容：%s" % params)
            # logger.info("获取返回的状态码:%d" % status_code)
            # TODO 这里的逻辑不够通用，各个请求的接口可能不一致
            if status_code == 0:
                return HttpResponse.third_party(ERR_OK.code, ERR_OK.message, None, None, response_json)
            else:
                api_error = response_json.error_key if error_key is not None else response_json.msg
                return HttpResponse.third_party(ERR_OK.code, ERR_OK.message, status_code, api_error, response_json)
        except requests.exceptions.ConnectTimeout:
            # logger.error("网络不通：Request ConnectTimeout")
            # print("网络不通：Request ConnectTimeout")
            return HttpResponse.normal(ERR_CALL_API_TIMEOUT.code, ERR_CALL_API_TIMEOUT.message)
        except requests.exceptions.ConnectionError:
            # logger.error("未知服务器：Connection Error")
            # print("未知服务器：Connection Error")
            return HttpResponse.normal(ERR_API_CONNECTION_REFUSED.code, ERR_API_CONNECTION_REFUSED.message)
        except HTTPException as error_msg:
            # logger.error("请求失败！")
            print(error_msg)
            return HttpResponse.normal(ERR_API_RETURN_INVALID.code, ERR_API_RETURN_INVALID.message)

    # 封装Post方法，return响应码和响应内容
    @staticmethod
    def post(url, params=None, headers=None, timeout=60, error_key=None):
        try:
            response = requests.post(url=url, params=params, headers=headers, timeout=60)
            status_code = response.status_code
            response_json = response.json()
            # logger.info("Post请求的内容：%s" % params)
            # logger.info("获取返回的状态码:%d" % status_code)
            if status_code == 0:
                return {"code": 0, "error": "", "api_code": 0, "api_error": "", "api_response": response_json}
            else:
                return {
                    "code": 0,
                    "error": "",
                    "api_code": status_code,
                    "api_error": response_json.error_key if error_key is not None else response_json.msg,
                    "api_response": response_json
                }
        except requests.exceptions.ConnectTimeout:
            # logger.error("网络不通：Request ConnectTimeout")
            # print("网络不通：Request ConnectTimeout")
            return HttpResponse.normal(ERR_CALL_API_TIMEOUT.code, ERR_CALL_API_TIMEOUT.message)
        except requests.exceptions.ConnectionError:
            # logger.error("未知服务器：Connection Error")
            # print("未知服务器：Connection Error")
            return HttpResponse.normal(ERR_API_CONNECTION_REFUSED.code, ERR_API_CONNECTION_REFUSED.message)
        except HTTPException as error_msg:
            # logger.error("请求失败！")
            print(error_msg)
            return HttpResponse.normal(ERR_API_RETURN_INVALID.code, ERR_API_RETURN_INVALID.message)


class HttpResponse(object):
    @staticmethod
    def normal(code, error="", result=None):
        """
        通用的相应格式
        """
        if result is None:
            return {"code": code, "error": error}
        else:
            return {"code": code, "error": error, "result": result}

    @staticmethod
    def third_party(code, error="", api_code=None, api_error=None, api_response=None):
        """
        第三方API响应格式
        Args:
            code: 0代表正常返回，消息合法。-1代表异常，超时、断开、拒绝
            error: code -1 error 不空
            api_code: api返回的错误码
            api_error: api返回的错误消息
            api_response: api返回的原始消息
        """
        if api_code is None:
            # 云梯API请求正常时不带返回码和信息，故只返回api原始信息，其他接口待观察
            return {"code": code, "error": error, "api_response": api_response}
        else:
            return {
                "code": code,
                "error": error,
                "api_code": api_code,
                "api_error": api_error,
                "api_response": api_response
            }
