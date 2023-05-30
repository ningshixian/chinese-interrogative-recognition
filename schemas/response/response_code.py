#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/22 13:32
# @Author  : CoderCharm
# @File    : response_code.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""

统一响应状态码

"""
from typing import Union

from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder


def resp_200(*, result_list: Union[list, dict] = [], message: str = "success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 200,
            'msg': message,
            'result_list': result_list,
        })
    )


def resp_500(*, result_list: Union[list, dict] = [], message: str = "Internal Server Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({
            'code': 500,
            'msg': message,
            'result_list': result_list,
        })
    )


# 请求参数格式错误
def resp_4001(*, result_list: Union[list, dict] = [],
              message: Union[list, dict, str] = "Request Validation Error") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 4001,
            'msg': message,
            'result_list': result_list,
        })
    )


# 内部验证数据错误
def resp_5002(*, result_list: Union[list, dict] = [], message: Union[list, dict, str] = "Request Fail") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 5002,
            'msg': message,
            'result_list': result_list,
        })
    )
