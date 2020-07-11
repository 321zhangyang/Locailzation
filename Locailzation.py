import os
import re
import requests
import json


def translate(word):
    # 注 频繁调用会出现封ip情况,自己根据实际情况来
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    print(response)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        result = json.loads(response.text)
        return result['translateResult'][0][0]['tgt']
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None


def getFileCodeArray(pathname):
    f = open(pathname, 'r')
    code = f.read()
    chinese = u'(@"[^"]*[\u4e00-\u9fff]+[^"\n]*?")'
    pattern = re.compile(chinese)
    result = pattern.findall(code)
    if len(result) != 0:
        for string in result:
            localString = string.split('@', 1)
            total.append(localString[1])


def getFilePath(catalogue):
    for filenames in os.walk(catalogue):
        for filename in filenames:
            for subfilename in filename:
                if subfilename.count('.m') > 0:
                    filepath = os.path.join(filenames[0], subfilename)
                    getFileCodeArray(filepath)


def writeStringToFile(totalChineses):
    define = open('Define.h', 'a')
    define.seek(0)
    define.truncate()
    for chinese in totalChineses:
        translationStr = translate(chinese)
        define.write('#define FFRemoteControlTempText @' + chinese + '   //' + chinese + '    //翻译结果为:' + translationStr)
        define.write('\r\n')
    define.close()


sourcePath = '/Users/apple/Desktop/项目/QCEducation/QCEducation'
path = sourcePath + ''
total = []
# 获取所有文字
getFilePath(path)
# 去重
total = list(set(total))
print(total)
# 写入define文件
writeStringToFile(total)
