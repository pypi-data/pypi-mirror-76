'''
Created by auto_sdk on 2018.07.25
'''
from libs.customize.top.api.base import RestApi
class TmcUserCancelRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.nick = None
		self.user_platform = None

	def getapiname(self):
		return 'taobao.tmc.user.cancel'
