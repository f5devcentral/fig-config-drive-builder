#!/usr/bin/env python3

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
This module contains the Flask application to build ISO9660 ConfigDrives
from posted user_data YAML
"""

import os
import json
import tempfile
import config_drive_builder

from flask import Flask, request, Response, redirect, url_for, send_file, render_template

app = Flask(__name__)

APP_URI = '/fig-config-drive-builder'


@app.route('/')
def index():
    """  Redirects index to application URI """
    return redirect(url_for('configdrivebuilder'))


@app.route(APP_URI, methods=['GET', 'POST'])
def configdrivebuilder():
    """ Implements Main Interface """
    if request.method == 'GET':
        substituions = {
            "APP_URI": APP_URI
        }
        return render_template("index.html", **substituions)
    elif request.method == 'POST':
        userdata = None
        if 'userdata' in request.files:
            userdata = request.files['userdata'].read().decode('utf-8')
        else:
            userdata = request.data.decode('utf-8')
        print('received userdata: \n%s' % userdata)
        (fd, config_drive_temp_file) = tempfile.mkstemp()
        if config_drive_builder.create_configdrive(userdata, config_drive_temp_file):
            return_data = send_file(config_drive_temp_file, as_attachment=True, attachment_filename='configdrive.iso')
            os.remove(config_drive_temp_file)
            return return_data
        else:
            resp = Response('{"msg": "Invalid userdata POST"}', status=400, mimetype='application/json')
            return resp



