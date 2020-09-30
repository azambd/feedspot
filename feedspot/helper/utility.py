import re
import json
import datetime
from scrapy.utils.project import get_project_settings

notAvailable = 'NOT AVAILABALE'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'}


def getGlobalSettings(varName):
    settings = get_project_settings()
    return settings.get(varName)


def getCurrentTime():
    return datetime.datetime.now().isoformat()


def json_from_s(s):
    match = re.findall(r"{.+[:,].+}|\[.+[,:].+\]", s)
    return json.loads(match[0]) if match else None


def getJSObject(response):
    return json_from_s(response.body.decode("utf-8"))
    # JSObject = re.findall('<script>window.__WML_REDUX_INITIAL_STATE__ =(.+?);</script>', response.body.decode("utf-8"), re.S)

    # if JSObject and len(JSObject) > 0:
    #     jsonString = JSObject[0].replace(';</script>', '')
    #     jsonObject =  json.loads(jsonString)
    #     if jsonObject:
    #         return jsonObject

    # return None


def getVarName(value):
    try:
        return int(value)
    except ValueError:
        pass
    return value


def getJSONObjectVariable(Object, varNames, noVal=notAvailable):
    value = noVal
    for varName in varNames.split('.'):
        varName = getVarName(varName)
        try:
            value = Object[varName]
            Object = Object[varName]
        except Exception:
            return noVal
    return value


def jsonDateConverter(object):
    if isinstance(object, datetime.datetime):
        return object.__str__()


def jsonDump(object):
    return json.dumps(object,
                      default=jsonDateConverter,
                      indent=4,
                      sort_keys=True)
