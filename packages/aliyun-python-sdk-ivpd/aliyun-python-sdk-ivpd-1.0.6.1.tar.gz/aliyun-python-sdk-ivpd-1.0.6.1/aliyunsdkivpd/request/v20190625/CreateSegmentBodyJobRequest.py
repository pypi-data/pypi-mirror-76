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

class CreateSegmentBodyJobRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'ivpd', '2019-06-25', 'CreateSegmentBodyJob','ivpd')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_DataLists(self):
		return self.get_body_params().get('DataLists')

	def set_DataLists(self, DataLists):
		for depth1 in range(len(DataLists)):
			if DataLists[depth1].get('DataId') is not None:
				self.add_body_params('DataList.' + str(depth1 + 1) + '.DataId', DataLists[depth1].get('DataId'))
			if DataLists[depth1].get('ImageUrl') is not None:
				self.add_body_params('DataList.' + str(depth1 + 1) + '.ImageUrl', DataLists[depth1].get('ImageUrl'))

	def get_JobId(self):
		return self.get_body_params().get('JobId')

	def set_JobId(self,JobId):
		self.add_body_params('JobId', JobId)

	def get_TimeToLive(self):
		return self.get_body_params().get('TimeToLive')

	def set_TimeToLive(self,TimeToLive):
		self.add_body_params('TimeToLive', TimeToLive)