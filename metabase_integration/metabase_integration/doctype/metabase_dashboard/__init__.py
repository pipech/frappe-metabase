# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
import jwt
import time


@frappe.whitelist()
def get_url(dashboard):
    # get metabase info
    metabase_config = frappe.get_single('Metabase Settings')
    # get dashboard info
    dashboard = frappe.get_doc('Metabase Dashboard', dashboard)

    # config token
    payload = {
        'resource': {'dashboard': int(dashboard.dashboard_id)},
        'params': {},
    }
    # set expiration time
    exp_time = metabase_config.metabase_exp_time
    if exp_time:
        payload['exp'] = round(time.time()) + (60 * exp_time)  # 60 second * minute

    # gen token
    token = jwt.encode(
        payload,
        metabase_config.metabase_secret,
        algorithm='HS256'
    )

    # prepare config
    config = []
    if dashboard.show_border:
        config.append('bordered=true')
    else:
        config.append('bordered=false')
    if dashboard.show_title:
        config.append('titled=true')
    else:
        config.append('titled=false')
    if dashboard.theme == 'Dark':
        config.append('theme=night')

    #config.append('user='+frappe.session.user)
    config_param = '&'.join(config)

    # prepare url
    resizer = ''.join([
        metabase_config.metabase_url,
        '/app/iframeResizer.js',
    ])
    iframeUrl = ''.join([
        metabase_config.metabase_url,
        '/embed/dashboard/',
        token,
#        '&user='+frappe.session.user,
        '#',
        config_param,
    ])

    #Rewriting meatebase iframeUrl generation here
    METABASE_SITE_URL = metabase_config.metabase_url
    METABASE_SECRET_KEY = metabase_config.metabase_secret

    payload = {
    "resource": {"dashboard": int(dashboard.dashboard_id)},
    "params": {
        "user": frappe.session.user
    },
    "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"    

    return {
        'name': dashboard.dashboard_name,
        'resizer': resizer,
        'iframeUrl': iframeUrl
    }
