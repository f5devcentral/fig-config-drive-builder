# coding=utf-8
# pylint: disable=broad-except,unused-argument,line-too-long, unused-variable
# Copyright (c) 2016-2018, F5 Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
This module builds ISO9660 ConfigDrives from user_data YAML
"""

import os
import sys
import tempfile
import json
import uuid
import pycdlib


def create_configdrive(userdata, configdrive_file):
    """ create the ISO9660 configdrive containing only the user-data """
    if not userdata:
        print('missing userdata')
        return False
    if not configdrive_file:
        print('missing configdrive output filename')
        return False
    md_prefix = '/openstack/latest'
    tmpdir = '%s%s' % (tempfile.mkdtemp(), md_prefix)
    try:
        os.makedirs(tmpdir)
        iso = pycdlib.PyCdlib()
        iso.new(interchange_level=3,
                joliet=True,
                sys_ident='LINUX',
                pub_ident_str='F5 Application and Orchestration PM Team',
                app_ident_str='tmos_configdrive_builder',
                rock_ridge='1.09',
                vol_ident='config-2')
        iso.add_directory('/OPENSTACK', rr_name='openstack')
        iso.add_directory('/OPENSTACK/LATEST', rr_name='latest')
        with open('%s/user_data' % tmpdir, 'w+') as ud_file:
            ud_file.write(userdata)
        iso.add_file(
            '%s/user_data' % tmpdir,
            '%s/USER_DATA.;1' % md_prefix.upper(),
            rr_name='user_data')
        metadata = metadata = json.dumps({'uuid': str(uuid.uuid4())})
        with open('%s/meta_data.json' % tmpdir, 'w+') as md_file:
            md_file.write(metadata)
        iso.add_file(
            '%s/meta_data.json' % tmpdir,
            '%s/META_DATA.JSON;1' % md_prefix.upper(),
            rr_name='meta_data.json')
        iso.write(configdrive_file)
        iso.close()
        clean_tmpdir(tmpdir)
    except TypeError as type_error:
        print('type error occured: %s' % type_error)
        clean_tmpdir(tmpdir)
        return False
    print('wrote ISO file %s' % configdrive_file)
    return True


def clean_tmpdir(tmpdir):
    """ clean out temporary directory """
    for tmp_file in os.listdir(tmpdir):
        os.remove('%s/%s' % (tmpdir, tmp_file))
    system_temp_dir = tempfile.gettempdir()
    path, directory = os.path.split(tmpdir)
    while not path == system_temp_dir:
        os.rmdir("%s" % os.path.join(path, directory))
        path, directory = os.path.split(path)
    os.rmdir("%s" % os.path.join(path, directory))