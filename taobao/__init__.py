# -*- coding: utf-8 -*-
##############################################################################
#
#    Python Taobao Open Platform API
#    Copyright 2013 wangbuke <wangbuke@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
__version__ = '0.1.2'
__author__ = 'wangbuke@gmail.com'

import json
import base64
import datetime
from hashlib import md5
import urllib
import urllib2

class TOPException(Exception):
    def __init__(self, code, msg):
        if type(msg) == unicode:
            msg = msg.encode('utf-8')
        self.code = code
        super(TOPException, self).__init__(msg)

    def __str__(self):
        return "%s (code=%d)" % (super(TOPException, self).__str__(), self.code)

    __repr__ = __str__


class _O(dict):
    """Makes a dictionary behave like an object."""
    def __getattr__(self, name):
        try:
            return self[name.lower()]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name.lower] = value


class _Method:
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, "%s.%s" % (self.__name, name))

    def __call__(self, *args, **kwargs):
        return self.__send(self.__name, args, **kwargs)


class ServerProxy(object):
    def __init__(self, app_key = None, app_secret = None, session = None, top_url=None):
        if not(app_key and app_secret and session):
            raise AttributeError("app_key and app_secret and session can not be None")
        self.app_key = app_key
        self.app_secret = app_secret
        self.session = session
        self.top_url = top_url or "http://gw.api.taobao.com/router/rest"

    def _sign(self, params, qhs = False):
        '''
        Generate API sign code
        '''
        for k, v in params.iteritems():
            if type(v) == int: v = str(v)
            elif type(v) == float: v = '%.2f'%v
            elif type(v) in (list, set):
                v = ','.join([str(i) for i in v])
            elif type(v) == bool: v = 'true' if v else 'false'
            elif type(v) == datetime.datetime: v = v.strftime('%Y-%m-%d %H:%M:%S')
            if type(v) == unicode:
                params[k] = v.encode('utf-8')
            else:
                params[k] = v

        if qhs:
            src = self.app_secret.encode('utf-8') + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())]) + self.app_secret.encode('utf-8')
        else:
            src = self.app_secret.encode('utf-8') + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())])

        return md5(src).hexdigest().upper()

    def decode_params(top_parameters) :
        params = {}
        param_string = base64.b64decode(top_parameters)
        for p in param_string.split('&') :
            key, value = p.split('=')
            params[key] = value
        return params

    def _get_timestamp(self):
        utc8 = datetime.datetime.utcnow() + datetime.timedelta(hours = 8)
        strtime = utc8.strftime('%Y-%m-%d %H:%M:%S')
        return strtime

    def _generate_params(self, method_name, **kwargs):
        params = {}
        for k, v in kwargs.iteritems():
            if v: params[k.lower()] = v
        params['app_key'] = self.app_key
        params['v'] = '2.0'
        params['sign_method'] = 'md5',
        params['format'] = 'json'
        params['partner_id'] = 'python_taobao_%s' %  __version__
        params['timestamp'] = self._get_timestamp()
        params['method'] = method_name
        params['session'] = self.session
        params['sign'] = self._sign(params)
        return params

    def execute(self, method_name, **kwargs):
        params = self._generate_params(method_name, **kwargs)
        urlopen = urllib2.urlopen(self.top_url, urllib.urlencode(params))
        rsp = urlopen.read()
        rsp = json.loads(rsp, strict=False, object_hook =lambda x: _O(x))
        if rsp.has_key('error_response'):
            error_code = rsp['error_response']['code']
            if 'sub_msg' in rsp['error_response']:
                msg = rsp['error_response']['sub_msg']
            else:
                msg = rsp['error_response']['msg']

            raise TOPException(error_code, msg)
        else:
            rsp = rsp[method_name.replace('.','_')[7:] + '_response']
            return rsp

    def __request(self, method_name, *args, **kwargs):
        return self.execute(method_name, **kwargs)

    def __getattr__(self, name):
        return _Method(self.__request, name)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
