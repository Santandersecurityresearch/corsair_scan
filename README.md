
[![GitHub release](https://img.shields.io/github/release/Santandersecurityresearch/corsair_scan.svg)](https://GitHub.com/Santandersecurityresearch/corsair_scan/releases/)
[![Github all releases](https://img.shields.io/github/downloads/Santandersecurityresearch/corsair_scan/total.svg)](https://GitHub.com/Santandersecurityresearch/corsair_scan/releases/)
[![HitCount](http://hits.dwyl.io/Santandersecurityresearch/corsair_sca.svg)](http://hits.dwyl.io/Santandersecurityresearch/corsair_scan)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Santandersecurityresearch/corsair_scan.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Santandersecurityresearch/corsair_scan/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Santandersecurityresearch/corsair_scan.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Santandersecurityresearch/corsair_scan/context:python)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)


![corsair_scan](/images/corsair_scan.png)

# Welcome to Corsair_scan

Corsair_scan is a security tool to test Cross-Origin Resource Sharing (CORS) misconfigurations. CORS is a mechanism that allows restricted resources on a web page to be requested from another domain outside the domain from which the first resource was served. If this is not properly configured, unauthorised domains can access to those resources.

# What is CORS?

CORS is an HTTP-header based mechanism that allows a server to indicate any other origins (domain, scheme, or port) than its own from which a browser should permit loading of resources. It works by adding new HTTP headers that let servers describe which origins are permitted to read that information from a web browser.

CORS also relies on a mechanism by which browsers make a “preflight” request to the server hosting the cross-origin resource, in order to check that the server will permit the actual request. In that preflight, the browser sends headers that indicate the HTTP method and headers that will be used in the actual request.

The most common and problematic security issue when implementing CORS is the failure to validate/whitelist requestors. Too often, we see the value for Access-Control-Allow-Origin set to ‘*’. 

Unfortunately, this is the default and as such allows any domain on the web to access that site’s resources.

As per the OWASP Application Security Verification Standard (ASVS), requirement [14.5.3](https://github.com/OWASP/ASVS/blob/6454d64fb1d23c1609050df0a017e7ae2fd6beb1/4.0/en/0x22-V14-Config.md) states

`Verify that the Cross-Origin Resource Sharing (CORS) Access-Control-Allow-Origin header uses a strict allow list of trusted domains and subdomains to match against and does not support the "null" origin.`

# How Does corsair_scan work?

Corsair_scan works by resending a request (or list of requests) received as a parameter and then injecting a value in the Origin header. Depending on the content of the Access-Control-Allow-Origin header in the response to this request, we can assert if CORS configuration is correct or not. There are three scenarios that indicate that CORS is misconfigured:

- The fake origin sent in the request is reflected in Access-Control-Allow-Origin
- The value of Access-Control-Allow-Origin is *
- The value of Access-Control-Allow-Origin is null

If CORS is found to be misconfigured, we check to see if the response contains the header Access-Control-Allow-Credentials, which means that the server allows credentials to be included on cross-origin requests.

Often, CORS configurations make use of wildcards, for example accepting anything under * example.com *. This means that the origin domain.com.evil.com will be accepted as it matches the given regex. To try and combat this, corsair_scan tests four scenarios:

- Fake domain injection: We set the origin header to https://scarymonster.com, even if the original request doesn't have an origin header
- If the original request has an origin header (for clarity, lets assume it is https://example.com):
  - Pre-domain injection: We concatenate our fake domain to the original domain on the left. In our example, the origin will be set to https://scarymonsterexample.com
  - Post-domain injection: The opposite of pre-domain, just concatenation on the right. The origin will be https://example.com.scarymonster.com
  - Sub-domain injection: Sometimes the CORS configuration whitelists all the subdomains under a given domain. Although it is not a problem per-se, if one of the domains is vulnerable to XSS, then, it can be a serious problem. The origin in this scenario will be https://scarymonster.example.com



# How Do I Install It?

This project was developed with Python 3.9, but should work with any Python 3.x version. 

corsair_scan has been designed to be used as a Python module , so the easiest way to install it is using pip.

`pip3 install corsair_scan --user`


# How Do I Use It?

At the moment, corsair_scan is intended to be used as a Python package. However, we plan to release this as a command line tool (CLI) in future releases.

The method that performs the CORS scan is corsair_scan. Here is its definition:

#### corsair_scan

Receives a list of requests and a parameter to enable/disable certificate check in the request

**Input**:

- data [List]: A list of requests. Each request is a dictionary that contains the relevant data for the request:

  - url_data [Dict]: This is a dictionary that contains all the relevant data for the request:
    - url [String]: This is the url where the request is sent
    - verb [String]: The verb for the request (get, post, patch, delete, options...)
    - params [String]: The body sent in the request (if any)
    - headers [Dict]: This is a dict with all the headers included in the request

- verify [Boolean] [Default: True] : Sends this value to corsair_scan_single_url for each request

  

**Output**:

- final_report [List]: Contains the full report for the test performed. If filter is set to true, it also adds a summary of the test to the report.
  - report [List]: List of detailed individual reports with the test performed
  - summary [Dict] : Summary of the issues detected in the scan



# Example

```
import corsair_scan
url_data = {}
data = []
verb =  'GET'
url = 'https://example.com/'
params = 'user=user1&password=1234'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'en-GB,en;q=0.5', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
           'Origin': 'https://example.com',
           'Host': 'example.com'}

url_data['verb'] = verb
url_data['url'] = url
url_data['params'] = params
url_data['headers'] = headers
data.append(url_data)

print (corsair_scan.corsair_scan(data, verify=True))
```



Response:

```
{'report': [{'fake_origin': {'Access-Control-Allow-Origin': 'https://scarymonster.com',
                             'Origin': 'https://scarymonster.com',
                             'credentials': True,
                             'error': False,
                             'misconfigured': True,
                             'status_code': 200},
             'post-domain': {'Access-Control-Allow-Origin': 'https://example.com.scarymonster.com',
                             'Origin': 'https://example.com.scarymonster.com',
                             'credentials': True,
                             'error': False,
                             'misconfigured': True,
                             'status_code': 200},
             'pre-domain': {'Access-Control-Allow-Origin': 'https://scarymonsterexample.com',
                            'Origin': ' https://scarymonsterexample.com',
                            'credentials': True,
                            'error': False,
                            'misconfigured': True,
                            'status_code': 200},
             'sub-domain': {'Access-Control-Allow-Origin': 'https://scarymonster.example.com',
                            'Origin': 'https://scarymonster.example.com',
                            'credentials': True,
                            'error': False,
                            'misconfigured': True,
                            'status_code': 200},
             'url': 'https://example.com/',
             'verb': 'GET'}],
 'summary': {'error': [], 'misconfigured': [{'credentials': True,
                    'misconfigured_test': ['fake_origin',
                                           'sub-domain',
                                           'pre-domain',
                                           'post-domain'],
                    'status_code': 200,
                    'url': 'https://domain.com',
                    'verb': 'GET'}]}}
```





## Roadmap

* Release corsair_scan as a CLI tool
* Read url data from a text file
* Improve reports format

# Who Is Behind It?

Corsair_scan was developed by the Santander UK Security Engineering team who are:

- [David Albone](https://github.com/dpauk)
- [Javier Domínguez Ruiz](https://github.com/javixeneize)
- [Fernando Cabrerizo](https://github.com/pealtrufo)
- [Jonathan Strong](https://github.com/mrjonstrong)
- [James Howieson](https://github.com/bal3r)

