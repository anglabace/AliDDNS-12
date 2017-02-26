#!/usr/bin/python
import datetime, hmac, hashlib, base64, uuid, urllib
from collections import OrderedDict


IP = '192.168.1.1'
ISFORMAT = "%Y-%m-%dT%H:%M:%SZ"
PROTOCAL = 'http://'
AccessKeyId = 'xxxxxxxxxxxxx'
RecordId = '12345678'
HTTPMethod = 'GET'
Host = 'alidns.aliyuncs.com'
Timestamp = datetime.datetime.strftime(datetime.datetime.utcnow(), ISFORMAT)
Hkey = 'YIvZPbkJ4YHnZNuqEmJSspjWQFP5lR' + '&'
ordered = OrderedDict()
parameters = {"AccessKeyId": AccessKeyId, 'Action': 'UpdateDomainRecord', 'RR': 'home', 'Type': 'A',
              'Value': IP, 'Format': 'JSON', 'Version': '2015-01-09', 'SignatureMethod': 'HMAC-SHA1',
              'Timestamp': Timestamp, 'SignatureVersion': '1.0', 'SignatureNonce': uuid.uuid4(),
              'RecordId': RecordId}
keys = parameters.keys()
keys.sort()
for k in keys:
    ordered[k] = parameters[k]
QueryString = urllib.urlencode(ordered)
StringToSign = HTTPMethod + '&%2F&' + urllib.quote(QueryString)
# print StringToSign
Signature = base64.b64encode(hmac.new(Hkey, StringToSign, hashlib.sha1).digest())
# print Signature
ordered['Signature'] = Signature

URL = PROTOCAL + Host + '/?' + urllib.urlencode(ordered)
print URL
response = urllib.urlopen(URL)
print response.read()
# ntpd -n -q -p 0.asia.pool.ntp.org
# /opt/bin/python /media/AiDisk_a1/AliDDNS.py -i $3