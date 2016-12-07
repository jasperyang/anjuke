# -*- coding: utf-8 -*-
import random
import base64

from fangchan.settings import PROXIES


class RandomUserAgent(object):
	"""Randomly rotate user agents based on a list of predefined ones"""
	def __init__(self, agents):
		self.agents = agents
	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))
	def process_request(self, request, spider):
		#print "**************************" + random.choice(self.agents)
		request.headers.setdefault('User-Agent', random.choice(self.agents))
class ProxyMiddleware(object):
	def process_request(self, request, spider):
		request.meta['proxy'] = 'http://45.76.150.178:5552'
		encoded_user_pass = base64.b64encode(b'fangchan:Boyiding123')
		request.headers['Proxy-Authorization'] = b'Basic ' + encoded_user_pass
