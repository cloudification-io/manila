# Copyright 2014 Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import ddt
from tempest.lib import exceptions as lib_exc
from testtools import testcase as tc

from manila_tempest_tests.tests.api import base


@ddt.ddt
class SharesMetadataAPIOnlyNegativeTest(base.BaseSharesTest):

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    @ddt.data(True, False)
    def test_try_set_metadata_to_unexisting_share(self, is_v2_client):
        md = {u"key1": u"value1", u"key2": u"value2", }
        client = self.shares_v2_client if is_v2_client else self.shares_client
        self.assertRaises(lib_exc.NotFound,
                          client.set_metadata,
                          "wrong_share_id", md)

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    @ddt.data(True, False)
    def test_try_update_all_metadata_for_unexisting_share(self, is_v2_client):
        md = {u"key1": u"value1", u"key2": u"value2", }
        client = self.shares_v2_client if is_v2_client else self.shares_client
        self.assertRaises(lib_exc.NotFound,
                          client.update_all_metadata,
                          "wrong_share_id", md)


class SharesMetadataNegativeTest(base.BaseSharesMixedTest):
    @classmethod
    def resource_setup(cls):
        super(SharesMetadataNegativeTest, cls).resource_setup()
        # create share type
        cls.share_type = cls._create_share_type()
        cls.share_type_id = cls.share_type['id']

        # create share
        cls.share = cls.create_share(share_type_id=cls.share_type_id)

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    def test_try_set_metadata_with_empty_key(self):
        self.assertRaises(lib_exc.BadRequest,
                          self.shares_client.set_metadata,
                          self.share["id"], {"": "value"})

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    def test_try_upd_metadata_with_empty_key(self):
        self.assertRaises(lib_exc.BadRequest,
                          self.shares_client.update_all_metadata,
                          self.share["id"], {"": "value"})

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    def test_try_set_metadata_with_too_big_key(self):
        too_big_key = "x" * 256
        md = {too_big_key: "value"}
        self.assertRaises(lib_exc.BadRequest,
                          self.shares_client.set_metadata,
                          self.share["id"], md)

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    def test_try_upd_metadata_with_too_big_key(self):
        too_big_key = "x" * 256
        md = {too_big_key: "value"}
        self.assertRaises(lib_exc.BadRequest,
                          self.shares_client.update_all_metadata,
                          self.share["id"], md)

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    def test_try_set_metadata_with_too_big_value(self):
        too_big_value = "x" * 1024
        md = {"key": too_big_value}
        self.assertRaises(lib_exc.BadRequest,
                          self.shares_client.set_metadata,
                          self.share["id"], md)

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    def test_try_upd_metadata_with_too_big_value(self):
        too_big_value = "x" * 1024
        md = {"key": too_big_value}
        self.assertRaises(lib_exc.BadRequest,
                          self.shares_client.update_all_metadata,
                          self.share["id"], md)

    @tc.attr(base.TAG_NEGATIVE, base.TAG_API_WITH_BACKEND)
    def test_try_delete_unexisting_metadata(self):
        self.assertRaises(lib_exc.NotFound,
                          self.shares_client.delete_metadata,
                          self.share["id"], "wrong_key")
