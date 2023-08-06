# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from alibabacloud_tea_roa.client import Client as ROAClient
from alibabacloud_imagesearch20180319 import models as image_search_20180319_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient


class Client(ROAClient):
    def __init__(self, config):
        super(Client, self).__init__(config)
        self._endpoint_rule = ""
        self.check_config(config)
        self._endpoint_host = self.get_endpoint("imagesearch", self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint_host)

    def search_item_with_options(self, request, runtime):
        UtilClient.validate_model(request)
        return image_search_20180319_models.SearchItemResponse().from_map(self.do_request_with_action("SearchItem", "2018-03-19", "HTTPS", "POST", "AK", "/item/search", UtilClient.stringify_map_value(request.query.to_map()), request.headers, None, runtime))


    def search_item(self, request):
        runtime = util_models.RuntimeOptions(

        )
        return self.search_item_with_options(request, runtime)

    def delete_item_with_options(self, request, runtime):
        UtilClient.validate_model(request)
        return image_search_20180319_models.DeleteItemResponse().from_map(self.do_request_with_action("DeleteItem", "2018-03-19", "HTTPS", "POST", "AK", "/item/delete", UtilClient.stringify_map_value(request.query.to_map()), request.headers, None, runtime))


    def delete_item(self, request):
        runtime = util_models.RuntimeOptions(

        )
        return self.delete_item_with_options(request, runtime)

    def add_item_with_options(self, request, runtime):
        UtilClient.validate_model(request)
        return image_search_20180319_models.AddItemResponse().from_map(self.do_request_with_action("AddItem", "2018-03-19", "HTTPS", "POST", "AK", "/item/add", UtilClient.stringify_map_value(request.query.to_map()), request.headers, None, runtime))


    def add_item(self, request):
        runtime = util_models.RuntimeOptions(

        )
        return self.add_item_with_options(request, runtime)

    def get_endpoint(self, product_id, region_id, endpoint_rule, network, suffix, endpoint_map, endpoint):
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get('regionId')):
            return endpoint_map.get('regionId')
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)
