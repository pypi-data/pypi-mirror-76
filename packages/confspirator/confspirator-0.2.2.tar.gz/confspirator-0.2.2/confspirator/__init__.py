# Copyright (C) 2019 Catalyst Cloud Ltd
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

from confspirator import example
from confspirator import loader
from confspirator.tests import utils


create_example_config = example.create_example_config

load = loader.load_config_dict
load_dict = loader.load_config_dict
load_file = loader.load_config_file

modify_conf = utils.modify_conf
