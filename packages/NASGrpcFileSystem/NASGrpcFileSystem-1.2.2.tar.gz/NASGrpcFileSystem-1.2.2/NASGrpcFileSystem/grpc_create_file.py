# coding: utf-8

import base64
import json
import logging
import os
import sys
import traceback
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse
import grpc
from typing import Iterable
from future.utils import raise_
from werkzeug.wrappers import Response
from NASGrpcFileSystem.code_dict import code_dict
from .proto import files_pb2
from .proto.files_pb2_grpc import FileWorkerStub
if sys.version.startswith("2."):
    FileNotFoundError = IOError

RETRY = 0


def create_file(caller_code, remote_path, x_type, req_url, file=None, filename=None,
                file_path=None, mount_path=None, replace=True,
                recovery_path=None, timeout=3, logger=logging):
    """
    在服务器创建文件
    :param caller_code: 调用方编码
    :param remote_path: 远程存储目录
    :param x_type: 业务类型
    :param req_url: 请求服务的 ip:port
    :param file: 文件流，若不选择文件路径则必传文件流，也可以是base64编码的文件
    :param filename: 文件名称， 当上传对象为文件流时必传
    :param file_path: 本地文件路径，可以选择文件路径或者文件流
    :param mount_path: 服务器mount地址
    :param replace: 当文件已在服务器存在时是否强制替换，默认替换
    :param recovery_path: 容灾路径，当文件上传非正常失败时（调用接口非正常错误码），将文件存储的本地地址，此时返回的mount_path为空
    :param timeout: 超时时间，默认3秒
    :param logger: 日志对象
    :return:
    """
    file_like_obj, code, err, ret_mount_path = None, None, None, " "
    try:
        logger = logger if logger else logging
        if not remote_path or not x_type or not req_url or not caller_code:
            code = 128502
            return code, code_dict.get(str(code)), ""
        if req_url.startswith("http"):
            req_url = urlparse(req_url).netloc
        if file:
            if not filename:
                code = 128502
                return code, code_dict.get(str(code)), ""
            if isinstance(file, bytes):
                file = base64.b64decode(file)
            if isinstance(file, Iterable) and not isinstance(file, bytes):
                f_file = b''
                for f in file:
                    f_file += f
                file = f_file
        elif file_path:
            if not os.path.isfile(file_path):
                code = 128506
                return code, code_dict.get(str(code)), ""
            try:
                filename = os.path.basename(file_path)
                # file = open(file_path, 'rb').read()
                file = Response(_gen_file(file_path)).data
            except FileNotFoundError:
                code = 128505
                return code, code_dict.get(str(code)), ""
        else:
            code = 128502
            return code, code_dict.get(str(code)), ""
        with grpc.insecure_channel(req_url) as channel:
            stub = FileWorkerStub(channel)
            code, err, ret_mount_path = _call_interface(caller_code, stub, file, filename, remote_path, mount_path, x_type, replace, timeout, logger)
            if code == 128501:
                return code, err, ret_mount_path
    except Exception as exc:
        logger.error(traceback.format_exc())
        raise_(Exception, exc)
    finally:
        if (code in [128509, 128512, 1] or not code_dict.get(str(code), None)) and recovery_path:
            code, err, ret_mount_path = _recovery_handle(recovery_path, file_path, replace, filename, file, logger)
    return code, err, ret_mount_path


def _call_interface(caller_code, stub, file, filename, remote_path, mount_path, x_type, replace, timeout, logger):
    try:
        response = stub.createFile(files_pb2.create_request(file_data=file,
                                                            file_name=filename.encode('utf-8'),
                                                            x_file_path=remote_path.encode('utf-8'),
                                                            x_mount_path=(mount_path if mount_path else "").encode(
                                                                'utf-8'),
                                                            x_type=x_type.encode('utf-8'),
                                                            is_replace=replace,
                                                            f_code=caller_code,
                                                            ), timeout=timeout)
    except grpc.RpcError as e:
        status_code = e.code()
        if grpc.StatusCode.DEADLINE_EXCEEDED == status_code:
            code, err, ret_mount_path = 128512, code_dict.get("128512"), ""
        elif grpc.StatusCode.UNAVAILABLE == status_code:
            # 服务短时不可用，重试一次
            global RETRY
            RETRY += 1
            if RETRY <= 1:
                logger.error("Grpc error，%s, details=%s, ----> retry", status_code, e.details())
                return _call_interface(caller_code, stub, file, filename, remote_path, mount_path, x_type, replace, timeout, logger)
            else:
                logger.error("Grpc error，%s, details=%s, failed", status_code, e.details())
        elif grpc.StatusCode.INVALIDARGUMENT == status_code:
            # 参数异常
            code = 128501
            err = code_dict.get(str(code))
            ret_mount_path = ""
        else:
            logger.error("Grpc error，%s, details=%s", status_code, e.details())
            code = 1
            err = "请求失败"
            ret_mount_path = ""
    else:
        code = response.code
        err = response.err
        biz = json.loads(str(response.biz))
        ret_mount_path = biz.get('mountPath')
    return code, err, ret_mount_path


def _recovery_handle(recovery_path, file_path, replace, filename, file, logger):
    try:
        if not os.path.exists(recovery_path):
            return 128504, code_dict.get("128504"), ""
        if file_path:
            file_gen = None
            filename = os.path.basename(file_path)
            new_file = os.path.join(recovery_path, filename)
            if os.path.exists(new_file) and not replace:
                return 128507, code_dict.get("128507"), ""
            try:
                file_gen = _gen_file(file_path)
            except FileNotFoundError:
                return 128505, code_dict.get("128505"), ""
            except IOError:
                return 128513, code_dict.get("128513"), ""
            except Exception as exc:
                logger.error(traceback.format_exc())
                raise_(Exception, exc)
            if file_gen:
                with open(new_file, 'wb') as f:
                    for fc in file_gen:
                        f.write(fc)
        else:
            new_file = os.path.join(recovery_path, filename)
            if os.path.exists(new_file) and not replace:
                return 128507, code_dict.get("128507"), ""
            with open(new_file, 'wb') as f:
                f.write(file)
        code = 0
        err = code_dict.get("0")
        ret_mount_path = ""
        return code, err, ret_mount_path
    except IOError:
        return 128510, code_dict.get("128510"), ""
    except Exception as exc:
        logger.error(traceback.format_exc())
        raise_(Exception, exc)


def _gen_file(file_path, size=1024*1024):
    """
    将文件读取为文件流
    :param file_path:
    :param size:
    :return:
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read(size)
            while data:
                yield data
                data = f.read(size)
    except FileNotFoundError:
        raise_(FileNotFoundError, "文件不存在")
    except IOError:
        raise_(IOError, "文件读取失败")
    except Exception as exc:
        raise_(Exception, exc)
