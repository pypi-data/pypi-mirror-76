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

from aliyunsdkcore.request import RpcRequest
from aliyunsdkivpd.endpoint import endpoint_data

class PreviewModelForPackageDesignRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'ivpd', '2019-06-25', 'PreviewModelForPackageDesign','ivpd')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_MaterialName(self):
		return self.get_body_params().get('MaterialName')

	def set_MaterialName(self,MaterialName):
		self.add_body_params('MaterialName', MaterialName)

	def get_ElementLists(self):
		return self.get_body_params().get('ElementLists')

	def set_ElementLists(self, ElementLists):
		for depth1 in range(len(ElementLists)):
			if ElementLists[depth1].get('ImageUrl') is not None:
				self.add_body_params('ElementList.' + str(depth1 + 1) + '.ImageUrl', ElementLists[depth1].get('ImageUrl'))
			if ElementLists[depth1].get('SideName') is not None:
				self.add_body_params('ElementList.' + str(depth1 + 1) + '.SideName', ElementLists[depth1].get('SideName'))

	def get_DataId(self):
		return self.get_body_params().get('DataId')

	def set_DataId(self,DataId):
		self.add_body_params('DataId', DataId)

	def get_MaterialType(self):
		return self.get_body_params().get('MaterialType')

	def set_MaterialType(self,MaterialType):
		self.add_body_params('MaterialType', MaterialType)

	def get_ModelType(self):
		return self.get_body_params().get('ModelType')

	def set_ModelType(self,ModelType):
		self.add_body_params('ModelType', ModelType)

	def get_Category(self):
		return self.get_body_params().get('Category')

	def set_Category(self,Category):
		self.add_body_params('Category', Category)