# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest

class DemoRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'SDK', '2018-01-01', 'Demo')
		self.set_uri_pattern('/helloworld')
		self.set_method('POST')

	def get_Price(self):
		return self.get_query_params().get('Price')

	def set_Price(self,Price):
		self.add_query_param('Price',Price)

	def get_Name(self):
		return self.get_body_params().get('Name')

	def set_Name(self,Name):
		self.add_body_params('Name', Name)

	def get_ContentLists(self):
		return self.get_body_params().get('ContentLists')

	def set_ContentLists(self, ContentLists):
		for depth1 in range(len(ContentLists)):
			if ContentLists[depth1].get('Tag') is not None:
				self.add_body_params('ContentList.' + str(depth1 + 1) + '.Tag', ContentLists[depth1].get('Tag'))
			if ContentLists[depth1].get('Letters') is not None:
				for depth2 in range(len(ContentLists[depth1].get('Letters'))):
					if ContentLists[depth1].get('Letters')[depth2] is not None:
						self.add_body_params('ContentList.' + str(depth1 + 1) + '.Letters.' + str(depth2 + 1) , ContentLists[depth1].get('Letters')[depth2])