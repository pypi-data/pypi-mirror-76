'''
Created by auto_sdk on 2019.08.07
'''
from libs.customize.top.api.base import RestApi
class ShopSellerGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None

	def getapiname(self):
		return 'taobao.shop.seller.get'
