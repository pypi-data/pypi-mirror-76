import json, re
from enum import Enum
from sanic import response
from .log_helper import LogHelper

Log = LogHelper()


# 0非必填 1必填
class Param:
    def __init__(self, request):
        content_type = request.content_type if request.content_type else ""
        self._param = request.args if request.method == "GET" or "multipart/form-data" in content_type else request.json
        self.req = request

    def checkParam(self, key, code, checkFormatReg=None):
        if self._param is None:
            raise RuntimeError({"rtnCode": "1000", "rtnMsg": key + "参数不存在"})
        else:
            param = self._param.get(key)
            if not isinstance(param, str):
                param = json.dumps(param, ensure_ascii=False) if param is not None else None
            if param is None:
                if code == 1:
                    raise RuntimeError(
                        {"rtnCode": "1000", "rtnMsg": key + "参数不存在"})
                else:
                    return ""
            else:
                if code == 1:
                    if len(param) == 0:
                        raise RuntimeError(
                            {"rtnCode": "1000", "rtnMsg": key + "参数不存在"})
                    else:
                        if checkFormatReg is None:
                            return param
                        else:
                            result = re.match((checkFormatReg), param)
                            # print(result, param)
                            if result:
                                return param
                            else:
                                raise RuntimeError(
                                    {"rtnCode": "1000", "rtnMsg": key + "参数格式错误"})
                else:
                    return param

    def Response(self, rtn_code, rtnDesc="", Body=None):
        rtnObj = rtn_code.value[0]
        rtnObj["rtnDesc"] = rtnDesc
        if Body is not None:
            rtnBody = {
                "head": rtnObj,
                "body": Body
            }
        else:
            rtnBody = {
                "head": rtnObj
            }
        if "0000" == rtnObj.get("rtnCode"):
            Log.info(f"{self.req.url} 0000 {rtnBody}")
        elif "1000" == rtnObj.get("rtnCode"):
            Log.warning(f"{self.req.url} 1000 {rtnBody}")
        else:
            Log.error(f"{self.req.url} {rtnObj.get('rtnCode')} {rtnBody}")
        return response.json(status=200, body=rtnBody, dumps=json.dumps, default=str)

    def HandleParam(self, ParamStr, *OtherKey):
        RealParam = {k: self.checkParam(k, v) for (k, v) in ParamStr.items()}
        if OtherKey:
            if OtherKey[0]:
                OtherParam = {k: v for (k, v) in self._param.items() if k in OtherKey[0]}
            else:
                OtherParam = {k: v for (k, v) in self._param.items() if k not in ParamStr.keys()}
        else:
            OtherParam = {k: v for (k, v) in self._param.items() if k not in ParamStr.keys()}
        return RealParam, OtherParam


class rtnCode(Enum):
    Success = {"rtnCode": "0000", "rtnMsg": "操作成功", "rtnDesc": ""},
    Failure = {"rtnCode": "1000", "rtnMsg": "操作失败", "rtnDesc": ""},
    ParamError = {"rtnCode": "1001", "rtnMsg": "缺少参数/参数格式错误"},
    BizParamError = {"rtnCode": "1002", "rtnMsg": "业务参数异常"},
    # Auth
    AuthError = {"rtnCode": "2000", "rtnMsg": "接口授权信息异常"},
    PermissionError = {"rtnCode": "2001", "rtnMsg": "权限不足"},
    TokenError = {"rtnCode": "2002", "rtnMsg": "token异常"},
    SignatureError = {"rtnCode": "2003", "rtnMsg": "signature异常"},
    # 补充异常
    DBError = {"rtnCode": "3001", "rtnMsg": "数据库异常"},
    OutsideApiError = {"rtnCode": "4001", "rtnMsg": "外部接口访问异常"},
    # Other
    OtherError = {"rtnCode": "9999", "rtnMsg": "其他异常"},
    TipError = {"rtnCode": "xxxx", "rtnMsg": "异常提示"},
