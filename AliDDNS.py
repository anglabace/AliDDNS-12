#!/usr/bin/python
# coding=UTF-8

import datetime, hmac, hashlib, base64, uuid, urllib, getopt, sys, json
from collections import OrderedDict


def useage():
    print "Useage: " \
          " /path/to/python aliddns.py [-aknArRih]\n" \
          "选项:\n" \
          "     -a,--accessid   : 阿里云API AceessID,在阿里云控制台中开启, 必须;\n" \
          "     -k,--accesskey  : 阿里云API AccessKey, 必须;\n" \
          "     -A,--action     : 操作[ 查询 | 更新 ], 可选值为[ DescribeDomainRecord | UpdateDomainRecord ], 必须;\n" \
          "     -n,--domainname : 你的域名, 例如'example.com', 查询时必须;\n" \
          "     -r,--rr         : 主机记录, 例如'www.baidu.com'中的baidu, 更新DNS记录时必须;\n" \
          "     -R,--recordid   : 主机记录ID, 通过查询获取, 更新DNS记录时必须;\n" \
          "     -i,--ip         : 需要解析到的IP地址,更新DNS记录时必须;;\n" \
          "     -h,--help       : 显示此帮助;\n" \
          "说明:" \
          "     首先取得你的域名对应的RecordID\n" \
          "     #aliddns.py -A DescribeDomainRecord -a 你的KEYID -k 你的KEY -n 你的域名\n" \
          "     再使用相应的RecordID和IP地址更新域名解析\n" \
          "     #aliddns.py -A UpdateDomainRecord -a 你的KEYID -k 你的KEY -r 你的主机记录 -R 对应的RecordID -i 需要解析的IP\n" \
          "     或者获取到RecordID后, 直接将脚本设置为连线后自动运行."


def access_api(pars, key):
    protocal = 'http://'
    httpmethod = 'GET'
    host = 'alidns.aliyuncs.com'
    ordered = OrderedDict()
    keys = pars.keys()
    keys.sort()
    for k in keys:
        ordered[k] = pars[k]
    print ordered
    querystring = urllib.urlencode(ordered)
    stringtosign = httpmethod + '&%2F&' + urllib.quote(querystring)
    # 使用key将参数字符串HMAC-SHA1加密并使用base64编码
    signature = base64.b64encode(hmac.new(key, stringtosign, hashlib.sha1).digest())
    ordered['Signature'] = signature
    url = protocal + host + '/?' + urllib.urlencode(ordered)
    print url
    response = urllib.urlopen(url)
    print response.read()


def main():
    try:
        options, value = getopt.getopt(sys.argv[1:], 'a:k:n:A:r:R:i:h',
                                       ["accessid=", "accesskey=", "domainname=", "action=",
                                        "rr=", "recordid=", "ip=", "help"])
    except getopt.GetoptError as err:
        useage()
        print err
        return ()
    else:
        pars = {}
        for o, v in options:
            if o in ['-a', '--accessid']:
                pars['AccessKeyId'] = v
            if o in ['-k', '--accesskey']:
                pars['AccessKey'] = v
            if o in ['-A', '--action']:
                pars['Action'] = v
            if o in ['-n', '--domainname']:
                pars['DomainName'] = v
            if o in ['-r', '--rr']:
                pars['RR'] = v
            if o in ['-R', '--recordid']:
                pars['RecordId'] = v
            if o in ['-i', '--ip']:
                pars['Value'] = v
            if o in ['-h', '--help']:
                useage()
                exit()
        timestamp = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")
        pars.update({'Format': 'JSON', 'Version': '2015-01-09', 'SignatureMethod': 'HMAC-SHA1', 'Timestamp': timestamp,
                     'SignatureVersion': '1.0', 'SignatureNonce': uuid.uuid4()})
        if 'AccessKeyId' in pars.keys() and 'AccessKey' in pars.keys():
            # 签名使用AccessKey+‘&’作为密钥, AccessKey本身不属于待签名字字串
            accesskey = pars.pop('AccessKey') + '&'
            if 'Action' in pars.keys() and pars['Action'] in ['UpdateDomainRecord', 'DescribeDomainRecords']:
                if pars['Action'] == 'DescribeDomainRecords':
                    if 'DomainName' in pars.keys():
                        access_api(pars, accesskey)
                    else:
                        print '错误: 需要DomainName字段.'
                else:
                    if 'RR' in pars.keys() and 'RecordId' in pars.keys() and 'Value' in pars.keys():
                        access_api(pars, accesskey)
                    else:
                        print '错误, 需要RR/RecordId/Value字段.'
            else:
                print '错误, 需要Actions字段.'
        else:
            print '错误, 需要AccessKey&ID字段.'


if __name__ == '__main__':
    main()

# ntpd -n -q -p 0.asia.pool.ntp.org
# /opt/bin/python /media/AiDisk_a1/AliDDNS.py -i $3
