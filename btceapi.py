# -*- coding: utf-8 -*-
## Author:      t0pep0
## e-mail:      t0pep0.gentoo@gmail.com
## Jabber:      t0pep0@jabber.ru
## BTC   :      1ipEA2fcVyjiUnBqUx7PVy5efktz2hucb
## donate free =)
import httplib
import urllib
import json
import hashlib
import hmac
import time

class api:
 __api_key	= '';
 __api_secret	= '';
 __nonce_v	= 1;
 __wait_for_nonce = False

 def __init__(self,api_key,api_secret,wait_for_nonce=False):
  self.__api_key = api_key
  self.__api_secret = api_secret
  self.__wait_for_nonce = wait_for_nonce

 def __nonce(self):
   if self.__wait_for_nonce: time.sleep(1)
   self.__nonce_v = str(time.time()).split('.')[0]

 def __signature(self, params):
  return hmac.new(self.__api_secret, params, digestmod=hashlib.sha512).hexdigest()

 def __api_call(self,method,params):
  self.__nonce()
  params['method'] = method
  params['nonce'] = str(self.__nonce_v)
  params = urllib.urlencode(params)
  headers = {"Content-type" : "application/x-www-form-urlencoded",
                      "Key" : self.__api_key,
		     "Sign" : self.__signature(params)}
  conn = httplib.HTTPSConnection("btc-e.com")
  conn.request("POST", "/tapi", params, headers)
  response = conn.getresponse()
  data = json.load(response)
  conn.close()
  return data
  
 def get_param(self, couple, param):
  conn = httplib.HTTPSConnection("btc-e.com")
  conn.request("GET", "/api/2/"+couple+"/"+param)
  response = conn.getresponse()
  data = json.load(response)
  conn.close()
  return data
 
 def getInfo(self):
  return self.__api_call('getInfo', {})

 def TransHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
  params = {
   "from"	: tfrom,
   "count"	: tcount,
   "from_id"	: tfrom_id,
   "end_id"	: tend_id,
   "order"	: torder,
   "since"	: tsince,
   "end"	: tend}
  return self.__api_call('TransHistory', params)
 
 def TradeHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
  params = {
   "from"	: tfrom,
   "count"	: tcount,
   "from_id"	: tfrom_id,
   "end_id"	: tend_id,
   "order"	: torder,
   "since"	: tsince,
   "end"	: tend,
   "pair"	: tpair}
  return self.__api_call('TradeHistory', params)

 def ActiveOrders(self, tpair):
  params = { "pair" : tpair }
  return self.__api_call('ActiveOrders', params)

 def Trade(self, tpair, ttype, trate, tamount):
  params = {
   "pair"	: tpair,
   "type"	: ttype,
   "rate"	: trate,
   "amount"	: tamount}
  return self.__api_call('Trade', params)
  
 def CancelOrder(self, torder_id):
  params = { "order_id" : torder_id }
  return self.__api_call('CancelOrder', params)
