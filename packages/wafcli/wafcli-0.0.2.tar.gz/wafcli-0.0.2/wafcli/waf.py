import fire
import os
import json
from tencentcloud.common import credential, abstract_client
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException


class WafClient(abstract_client.AbstractClient):
    _apiVersion = '2018-01-25'
    _endpoint = 'waf.tencentcloudapi.com'

    def api(self, api_name: str, params):
        try:
            body = self.call(api_name, params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                return response
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


class Waf(object):
    def __init__(self, secret_id='', secret_key='', region='', edition=''):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        self.edition = edition

    def send_request(self, api, params):
        cred = credential.Credential(self.secret_id, self.secret_key)
        client = WafClient(cred, self.region)
        return client.api(api, params)

    def print_resp(self, resp):
        print(json.dumps(resp, indent="\t"))


class Domains(Waf):

    def __init__(self, secret_id='', secret_key='', region='', edition=''):
        super().__init__(secret_id, secret_key, region, edition)

    def list(self, index=1, count=10):
        resp = self.send_request("DescribeSpartaProtectionList", {
            "Paging": {
                "Index": index,
                "Count": count
            }
        })
        self.print_resp(resp)

    def info(self, domain):
        resp = self.send_request("DescribeSpartaProtectionInfo", {
            "Domain": domain
        })
        self.print_resp(resp)


class CustomRules(Waf):

    def __init__(self, secret_id='', secret_key='', region='', edition=''):
        super().__init__(secret_id, secret_key, region, edition)

    def list(self, domain, index=0, count=10, action=None, search=None):
        """
        列举出某个域名下的所有自定义规则
        :param domain:
        :return:
        """
        params = {
            "Paging": {
                "Offset": index,
                "Limit": count
            },
            "Domain": domain
        }
        if action is not None:
            params["ActionType"] = action
        if search is not None:
            params["Search"] = search
        resp = self.send_request("DescribeCustomRules", params)
        self.print_resp(resp)

    def copy(self, from_domain: str, rule_name: str, to_domains: str):
        """
        复制规则
        :param from_domain:
        :param rule_name:
        :param to_domains:
        :return:
        """
        params = {
            "Edition": self.edition,
            "From": from_domain,
            "RuleName": rule_name,
            "Domains": to_domains
        }
        resp = self.send_request("CopyCustomRule", params)
        self.print_resp(resp)


class IP(Waf):
    def add(self, domain, ips):
        resp = self.send_request("UpsertIpAccessControl", {
            "Domain": domain,
            "Items": ips,
            "Edition": self.edition
        })
        self.print_resp(resp)

    def list(self):
        pass


class Pipeline(object):
    def __init__(self, secret_id='', secret_key='', region='', edition=''):
        if secret_id == "" or secret_key == "":
            home = os.path.expanduser("~")
            config_fp = os.path.join(home, ".waf", "waf.json")
            if not os.path.exists(config_fp):
                raise Exception("配置文件不能存在：{}".format(config_fp))
            with open(config_fp) as fp:
                obj = json.load(fp)
                secret_id = obj["secret_id"]
                secret_key = obj["secret_key"]
                region = obj["region"]
                edition = obj["edition"]
        self.domain = Domains(secret_id, secret_key, region, edition)
        self.custom_rule = CustomRules(secret_id, secret_key, region, edition)
        self.ip = IP(secret_id, secret_key, region, edition)


def exec():
    fire.Fire(Pipeline)


if __name__ == '__main__':
    fire.Fire(Pipeline)