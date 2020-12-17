#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
# Santander UK Security Engineering team.
##################################################
# MIT License Copyright (c) 2020 Grupo Santander
##################################################
# Author: Javier Dominguez Ruiz (@javixeneize)
# Version: 1.0
##################################################

import requests
import urllib3
import validators
import tldextract
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
VERBS = ['get', 'head', 'post', 'put', 'delete', 'options', 'patch']
SM_ORIGIN = 'https://scarymonster.com'
SM_ORIGIN_NO_PROTOCOL = 'scarymonster.com'
SM_ORIGIN_DOMAIN = 'scarymonster'
CORS_TESTS = ['fake_origin', 'sub-domain', 'pre-domain', 'post-domain']


def corsair_scan(data: list, verify: bool = True) -> dict:
    full_report: list = []
    final_report: dict = {}
    for url in data:
        single_report: dict = corsair_scan_single_url(url, verify)
        full_report.append(single_report.copy())
    final_report['summary'] = filter_report(full_report)
    final_report['report'] = full_report
    return final_report


def corsair_scan_single_url(url_data: dict, verify: bool = True) -> dict:
    report: dict = {'url': url_data.get('url'), 'verb': url_data.get('verb')}
    if validate_data(url_data.get('url'), url_data.get('verb')):
        report['fake_origin'] = validate_response(url_data, SM_ORIGIN, verify)
        if url_data.get('headers').get('Origin'):
            parsed_url = urlparse(url_data.get('headers').get('Origin'))
            parsed_domain = tldextract.extract(parsed_url.netloc)
            predomain: str = parsed_url.scheme + '://' + parsed_domain.subdomain + '.' + SM_ORIGIN_DOMAIN + \
                parsed_domain.domain + '.' + parsed_domain.suffix
            subdomain: str = parsed_url.scheme + '://' + SM_ORIGIN_DOMAIN + '.' + parsed_url.netloc
            postdomain: str = url_data.get('headers').get('Origin') + '.' + SM_ORIGIN_NO_PROTOCOL
            report['post-domain'] = validate_response(url_data, postdomain, verify)
            report['sub-domain'] = validate_response(url_data, subdomain, verify)
            report['pre-domain'] = validate_response(url_data, predomain, verify)
    return report


def validate_response(url_data: dict, origin: str, verify: bool) -> dict:
    url_report: dict = {}
    error: bool = False
    misconfigured: bool = False
    url: str = url_data.get('url')
    verb: str = url_data.get('verb')
    headers: dict = url_data.get('headers').copy()
    params: str = url_data.get('params')
    headers['Origin'] = origin
    resp = getattr(requests, verb.lower())(url=url, headers=headers, data=params, verify=verify, allow_redirects=False)
    url_report['Origin'] = origin
    url_report['Access-Control-Allow-Origin'] = resp.headers.get('Access-Control-Allow-Origin')
    url_report['credentials'] = 'access-control-allow-credentials' in resp.headers
    url_report['status_code'] = resp.status_code
    if resp.status_code == 401:
        error = True
    if url_report.get('Access-Control-Allow-Origin') in ['null', '*', url_report.get('Origin')]:
        misconfigured = True
    url_report['error'] = error
    url_report['misconfigured'] = misconfigured
    return url_report


def filter_report(report_list: list) -> dict:
    misconfigured_list: list = []
    error_list: list = []
    final_report: dict = {}
    for report in report_list:
        misconfigured_tests: list = []
        filtered_report: dict = {}
        filtered_report['url'] = report.get('url')
        filtered_report['verb'] = report.get('verb')
        filtered_report['status_code'] = report.get('fake_origin').get('status_code')
        error: bool = False
        for test in CORS_TESTS:
            if report.get(test):
                if report.get(test).get('error'):
                    error = True
                if report.get(test).get('misconfigured'):
                    misconfigured_tests.append(test)
                    filtered_report['credentials'] = report.get(test).get('credentials')
        if len(misconfigured_tests) > 0:
            filtered_report['misconfigured_test'] = misconfigured_tests
            misconfigured_list.append(filtered_report.copy())
        if error:
            error_list.append(filtered_report.copy())
        final_report['misconfigured'] = misconfigured_list
        final_report['error'] = error_list

    return (final_report)


def validate_data(url, verb):
    return validators.url(url) and verb.lower() in VERBS
