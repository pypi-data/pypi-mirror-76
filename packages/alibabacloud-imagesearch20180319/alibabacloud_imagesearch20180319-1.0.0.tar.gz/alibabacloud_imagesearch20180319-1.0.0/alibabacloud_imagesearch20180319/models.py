# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel


class SearchItemQuery(TeaModel):
    def __init__(self, instance_name=None):
        self.instance_name = instance_name

    def validate(self):
        self.validate_required(self.instance_name, 'instance_name')

    def to_map(self):
        result = {}
        result['instanceName'] = self.instance_name
        return result

    def from_map(self, map={}):
        self.instance_name = map.get('instanceName')
        return self


class SearchItemRequest(TeaModel):
    def __init__(self, headers=None, query=None):
        self.headers = headers
        self.query = query

    def validate(self):
        self.validate_required(self.query, 'query')
        if self.query:
            self.query.validate()

    def to_map(self):
        result = {}
        result['headers'] = self.headers
        if self.query is not None:
            result['query'] = self.query.to_map()
        else:
            result['query'] = None
        return result

    def from_map(self, map={}):
        self.headers = map.get('headers')
        if map.get('query') is not None:
            temp_model = SearchItemQuery()
            self.query = temp_model.from_map(map['query'])
        else:
            self.query = None
        return self


class SearchItemResponseBody(TeaModel):
    def __init__(self, request_id=None, success=None, message=None, code=None, auctions=None, head=None,
                 pic_info=None):
        self.request_id = request_id
        self.success = success
        self.message = message
        self.code = code
        self.auctions = auctions
        self.head = head
        self.pic_info = pic_info

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.success, 'success')
        self.validate_required(self.message, 'message')
        self.validate_required(self.code, 'code')
        self.validate_required(self.auctions, 'auctions')
        if self.auctions:
            self.auctions.validate()
        self.validate_required(self.head, 'head')
        if self.head:
            self.head.validate()
        self.validate_required(self.pic_info, 'pic_info')
        if self.pic_info:
            self.pic_info.validate()

    def to_map(self):
        result = {}
        result['RequestId'] = self.request_id
        result['Success'] = self.success
        result['Message'] = self.message
        result['Code'] = self.code
        if self.auctions is not None:
            result['Auctions'] = self.auctions.to_map()
        else:
            result['Auctions'] = None
        if self.head is not None:
            result['Head'] = self.head.to_map()
        else:
            result['Head'] = None
        if self.pic_info is not None:
            result['PicInfo'] = self.pic_info.to_map()
        else:
            result['PicInfo'] = None
        return result

    def from_map(self, map={}):
        self.request_id = map.get('RequestId')
        self.success = map.get('Success')
        self.message = map.get('Message')
        self.code = map.get('Code')
        if map.get('Auctions') is not None:
            temp_model = SearchItemResponseBodyAuctions()
            self.auctions = temp_model.from_map(map['Auctions'])
        else:
            self.auctions = None
        if map.get('Head') is not None:
            temp_model = SearchItemResponseBodyHead()
            self.head = temp_model.from_map(map['Head'])
        else:
            self.head = None
        if map.get('PicInfo') is not None:
            temp_model = SearchItemResponseBodyPicInfo()
            self.pic_info = temp_model.from_map(map['PicInfo'])
        else:
            self.pic_info = None
        return self


class SearchItemResponseBodyAuctionsAuction(TeaModel):
    def __init__(self, cust_content=None, item_id=None, sort_expr_values=None, cat_id=None, pic_name=None):
        self.cust_content = cust_content
        self.item_id = item_id
        self.sort_expr_values = sort_expr_values
        self.cat_id = cat_id
        self.pic_name = pic_name

    def validate(self):
        self.validate_required(self.cust_content, 'cust_content')
        self.validate_required(self.item_id, 'item_id')
        self.validate_required(self.sort_expr_values, 'sort_expr_values')
        self.validate_required(self.cat_id, 'cat_id')
        self.validate_required(self.pic_name, 'pic_name')

    def to_map(self):
        result = {}
        result['CustContent'] = self.cust_content
        result['ItemId'] = self.item_id
        result['SortExprValues'] = self.sort_expr_values
        result['CatId'] = self.cat_id
        result['PicName'] = self.pic_name
        return result

    def from_map(self, map={}):
        self.cust_content = map.get('CustContent')
        self.item_id = map.get('ItemId')
        self.sort_expr_values = map.get('SortExprValues')
        self.cat_id = map.get('CatId')
        self.pic_name = map.get('PicName')
        return self


class SearchItemResponseBodyAuctions(TeaModel):
    def __init__(self, auction=None):
        self.auction = auction

    def validate(self):
        self.validate_required(self.auction, 'auction')
        if self.auction:
            for k in self.auction:
                if k:
                    k.validate()

    def to_map(self):
        result = {}
        result['Auction'] = []
        if self.auction is not None:
            for k in self.auction:
                result['Auction'].append(k.to_map() if k else None)
        else:
            result['Auction'] = None
        return result

    def from_map(self, map={}):
        self.auction = []
        if map.get('Auction') is not None:
            for k in map.get('Auction'):
                temp_model = SearchItemResponseBodyAuctionsAuction()
                temp_model = temp_model.from_map(k)
                self.auction.append(temp_model)
        else:
            self.auction = None
        return self


class SearchItemResponseBodyHead(TeaModel):
    def __init__(self, search_time=None, docs_found=None, docs_return=None):
        self.search_time = search_time
        self.docs_found = docs_found
        self.docs_return = docs_return

    def validate(self):
        self.validate_required(self.search_time, 'search_time')
        self.validate_required(self.docs_found, 'docs_found')
        self.validate_required(self.docs_return, 'docs_return')

    def to_map(self):
        result = {}
        result['SearchTime'] = self.search_time
        result['DocsFound'] = self.docs_found
        result['DocsReturn'] = self.docs_return
        return result

    def from_map(self, map={}):
        self.search_time = map.get('SearchTime')
        self.docs_found = map.get('DocsFound')
        self.docs_return = map.get('DocsReturn')
        return self


class SearchItemResponseBodyPicInfoAllCategoryCategory(TeaModel):
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id

    def validate(self):
        self.validate_required(self.name, 'name')
        self.validate_required(self.id, 'id')

    def to_map(self):
        result = {}
        result['Name'] = self.name
        result['Id'] = self.id
        return result

    def from_map(self, map={}):
        self.name = map.get('Name')
        self.id = map.get('Id')
        return self


class SearchItemResponseBodyPicInfoAllCategory(TeaModel):
    def __init__(self, category=None):
        self.category = category

    def validate(self):
        self.validate_required(self.category, 'category')
        if self.category:
            for k in self.category:
                if k:
                    k.validate()

    def to_map(self):
        result = {}
        result['Category'] = []
        if self.category is not None:
            for k in self.category:
                result['Category'].append(k.to_map() if k else None)
        else:
            result['Category'] = None
        return result

    def from_map(self, map={}):
        self.category = []
        if map.get('Category') is not None:
            for k in map.get('Category'):
                temp_model = SearchItemResponseBodyPicInfoAllCategoryCategory()
                temp_model = temp_model.from_map(k)
                self.category.append(temp_model)
        else:
            self.category = None
        return self


class SearchItemResponseBodyPicInfo(TeaModel):
    def __init__(self, category=None, region=None, all_category=None):
        self.category = category
        self.region = region
        self.all_category = all_category

    def validate(self):
        self.validate_required(self.category, 'category')
        self.validate_required(self.region, 'region')
        self.validate_required(self.all_category, 'all_category')
        if self.all_category:
            self.all_category.validate()

    def to_map(self):
        result = {}
        result['Category'] = self.category
        result['Region'] = self.region
        if self.all_category is not None:
            result['AllCategory'] = self.all_category.to_map()
        else:
            result['AllCategory'] = None
        return result

    def from_map(self, map={}):
        self.category = map.get('Category')
        self.region = map.get('Region')
        if map.get('AllCategory') is not None:
            temp_model = SearchItemResponseBodyPicInfoAllCategory()
            self.all_category = temp_model.from_map(map['AllCategory'])
        else:
            self.all_category = None
        return self
class SearchItemResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = {}
        result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        else:
            result['body'] = None
        return result

    def from_map(self, map={}):
        self.headers = map.get('headers')
        if map.get('body') is not None:
            temp_model = SearchItemResponseBody()
            self.body = temp_model.from_map(map['body'])
        else:
            self.body = None
        return self


class DeleteItemQuery(TeaModel):
    def __init__(self, instance_name=None):
        self.instance_name = instance_name

    def validate(self):
        self.validate_required(self.instance_name, 'instance_name')

    def to_map(self):
        result = {}
        result['instanceName'] = self.instance_name
        return result

    def from_map(self, map={}):
        self.instance_name = map.get('instanceName')
        return self


class DeleteItemRequest(TeaModel):
    def __init__(self, headers=None, query=None):
        self.headers = headers
        self.query = query

    def validate(self):
        self.validate_required(self.query, 'query')
        if self.query:
            self.query.validate()

    def to_map(self):
        result = {}
        result['headers'] = self.headers
        if self.query is not None:
            result['query'] = self.query.to_map()
        else:
            result['query'] = None
        return result

    def from_map(self, map={}):
        self.headers = map.get('headers')
        if map.get('query') is not None:
            temp_model = DeleteItemQuery()
            self.query = temp_model.from_map(map['query'])
        else:
            self.query = None
        return self


class DeleteItemResponseBody(TeaModel):
    def __init__(self, request_id=None, success=None, message=None, code=None):
        self.request_id = request_id
        self.success = success
        self.message = message
        self.code = code

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.success, 'success')
        self.validate_required(self.message, 'message')
        self.validate_required(self.code, 'code')

    def to_map(self):
        result = {}
        result['RequestId'] = self.request_id
        result['Success'] = self.success
        result['Message'] = self.message
        result['Code'] = self.code
        return result

    def from_map(self, map={}):
        self.request_id = map.get('RequestId')
        self.success = map.get('Success')
        self.message = map.get('Message')
        self.code = map.get('Code')
        return self


class DeleteItemResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = {}
        result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        else:
            result['body'] = None
        return result

    def from_map(self, map={}):
        self.headers = map.get('headers')
        if map.get('body') is not None:
            temp_model = DeleteItemResponseBody()
            self.body = temp_model.from_map(map['body'])
        else:
            self.body = None
        return self


class AddItemQuery(TeaModel):
    def __init__(self, instance_name=None):
        self.instance_name = instance_name

    def validate(self):
        self.validate_required(self.instance_name, 'instance_name')

    def to_map(self):
        result = {}
        result['instanceName'] = self.instance_name
        return result

    def from_map(self, map={}):
        self.instance_name = map.get('instanceName')
        return self


class AddItemRequest(TeaModel):
    def __init__(self, headers=None, query=None):
        self.headers = headers
        self.query = query

    def validate(self):
        self.validate_required(self.query, 'query')
        if self.query:
            self.query.validate()

    def to_map(self):
        result = {}
        result['headers'] = self.headers
        if self.query is not None:
            result['query'] = self.query.to_map()
        else:
            result['query'] = None
        return result

    def from_map(self, map={}):
        self.headers = map.get('headers')
        if map.get('query') is not None:
            temp_model = AddItemQuery()
            self.query = temp_model.from_map(map['query'])
        else:
            self.query = None
        return self


class AddItemResponseBody(TeaModel):
    def __init__(self, request_id=None, success=None, message=None, code=None):
        self.request_id = request_id
        self.success = success
        self.message = message
        self.code = code

    def validate(self):
        self.validate_required(self.request_id, 'request_id')
        self.validate_required(self.success, 'success')
        self.validate_required(self.message, 'message')
        self.validate_required(self.code, 'code')

    def to_map(self):
        result = {}
        result['RequestId'] = self.request_id
        result['Success'] = self.success
        result['Message'] = self.message
        result['Code'] = self.code
        return result

    def from_map(self, map={}):
        self.request_id = map.get('RequestId')
        self.success = map.get('Success')
        self.message = map.get('Message')
        self.code = map.get('Code')
        return self


class AddItemResponse(TeaModel):
    def __init__(self, headers=None, body=None):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        result = {}
        result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        else:
            result['body'] = None
        return result

    def from_map(self, map={}):
        self.headers = map.get('headers')
        if map.get('body') is not None:
            temp_model = AddItemResponseBody()
            self.body = temp_model.from_map(map['body'])
        else:
            self.body = None
        return self
