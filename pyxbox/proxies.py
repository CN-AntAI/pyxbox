import string
import zipfile
import base64
import time
import hashlib


class AbuyunProxy(object):

    def __init__(self, proxyUser, proxyPass, proxyHost="http-dyn.abuyun.com", proxyPort="9020"):
        self.proxyHost = proxyHost
        self.proxyPort = proxyPort
        self.proxyUser = proxyUser
        self.proxyPass = proxyPass

    def reqProxy(self):
        '''
        :return proxies:
        '''
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    def scrapyProxy(self):
        '''
        :return proxyServer:
        :return proxyAuth:
        '''
        proxyServer = "http://http-pro.abuyun.com:9010"
        proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((self.proxyUser + ":" + self.proxyPass), "ascii")).decode(
            "utf8")
        return proxyServer, proxyAuth

    def chromeProxy(self, scheme='http', plugin_path=None):
        '''
        :param scheme:
        :param plugin_path:
        :return plugin_path:
        '''
        if plugin_path is None:
            plugin_path = r'D:/{}_{}@http-dyn.abuyun.com_9020.zip'.format(self.proxyUser, self.proxyPass)
        manifest_json = """
                        {
                            "version": "1.0.0",
                            "manifest_version": 2,
                            "name": "Abuyun Proxy",
                            "permissions": [
                                "proxy",
                                "tabs",
                                "unlimitedStorage",
                                "storage",
                                "<all_urls>",
                                "webRequest",
                                "webRequestBlocking"
                            ],
                            "background": {
                                "scripts": ["background.js"]
                            },
                            "minimum_chrome_version":"22.0.0"
                        }
                        """
        background_js = string.Template(
            """
                        var config = {
                            mode: "fixed_servers",
                            rules: {
                                singleProxy: {
                                    scheme: "${scheme}",
                                    host: "${host}",
                                    port: parseInt(${port})
                                },
                                bypassList: ["foobar.com"]
                            }
                          };
            
                        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            
                        function callbackFn(details) {
                            return {
                                authCredentials: {
                                    username: "${username}",
                                    password: "${password}"
                                }
                            };
                        }
                        chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                        );
                        """
        ).substitute(
            host=self.proxyHost,
            port=self.proxyPort,
            username=self.proxyUser,
            password=self.proxyPass,
            scheme=scheme,
        )

        with zipfile.ZipFile(plugin_path, 'w', ) as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

    def phantomjsProxy(self):
        '''
        :return service_args
        '''
        service_args = [
            "--proxy-type=http",
            "--proxy=%(host)s:%(port)s" % {
                "host": self.proxyHost,
                "port": self.proxyPort,
            },
            "--proxy-auth=%(user)s:%(pass)s" % {
                "user": self.proxyUser,
                "pass": self.proxyPass,
            },
        ]

        return service_args


class DuobeiProxy(object):
    def __init__(self, proxyUser, proxyPass, proxyHost="http-proxy-sg1.dobel.cn", proxyPort="9180"):
        self.proxyHost = proxyHost
        self.proxyPort = proxyPort
        self.proxyUser = proxyUser
        self.proxyPass = proxyPass

    def reqProxy(self):
        '''
        :return proxies:
        '''
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    def scrapyProxy(self):
        '''
        :return proxyServer:
        :return proxyAuth:
        '''
        proxyServer = "http://http-proxy-sg1.dobel.cn:9180"
        proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((self.proxyUser + ":" + self.proxyPass), "ascii")).decode(
            "utf8")
        return proxyServer, proxyAuth

    def phantomjsProxy(self):
        '''
        :return service_args
        '''
        service_args = [
            "--proxy-type=http",
            "--proxy=%(host)s:%(port)s" % {
                "host": self.proxyHost,
                "port": self.proxyPort,
            },
            "--proxy-auth=%(user)s:%(pass)s" % {
                "user": self.proxyUser,
                "pass": self.proxyPass,
            },
        ]
        return service_args

    def chromeProxy(self, scheme='http', plugin=None, ):
        '''
        :param scheme:
        :param plugin_path:
        :return plugin_path:
        '''
        if plugin is None:
            plugin_path = r'D:/{}_{}@http-proxy-sg1.dobel.cn.zip'.format(self.proxyUser, self.proxyPass)
        manifest_json = """
                        {
                            "version": "1.0.0",
                            "manifest_version": 2,
                            "name": "Duobei Proxy",
                            "permissions": [
                                "proxy",
                                "tabs",
                                "unlimitedStorage",
                                "storage",
                                "<all_urls>",
                                "webRequest",
                                "webRequestBlocking"
                            ],
                            "background": {
                                "scripts": ["background.js"]
                            },
                            "minimum_chrome_version":"22.0.0"
                        }
                        """
        background_js = string.Template(
            """
                        var config = {
                            mode: "fixed_servers",
                            rules: {
                                singleProxy: {
                                    scheme: "${scheme}",
                                    host: "${host}",
                                    port: parseInt(${port})
                                },
                                bypassList: ["foobar.com"]
                            }
                          };
            
                        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            
                        function callbackFn(details) {
                            return {
                                authCredentials: {
                                    username: "${username}",
                                    password: "${password}"
                                }
                            };
                        }
                        chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                        );
                        """
        ).substitute(
            host=self.proxyHost,
            port=self.proxyPort,
            username=self.proxyUser,
            password=self.proxyPass,
            scheme=scheme,
        )

        with zipfile.ZipFile(plugin_path, 'w', ) as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path


class MayiProxy(object):

    def generate_sign(self, app_key, secret, mayi_url, mayi_port):
        '''
        response = requests.get(url, proxies=proxies, headers=headers, allow_redirects=False, verify=False,
                            timeout=5).text
        :param app_key:
        :param secret:
        :param mayi_url:
        :param mayi_port:
        :return headers, proxies:
        '''
        mayi_proxy = 'http://{}:{}'.format(mayi_url, mayi_port)
        paramMap = {
            "app_key": app_key,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        keys = sorted(paramMap)
        codes = "%s%s%s" % (secret, str().join('%s%s' % (key, paramMap[key]) for key in keys), secret)
        sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()
        paramMap["sign"] = sign
        keys = paramMap.keys()
        authHeader = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, paramMap[key]) for key in keys)
        headers = {
            "Mayi-Authorization": authHeader,
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1"
        }
        proxies = {"http": mayi_proxy, "https": mayi_proxy}
        return headers, proxies
