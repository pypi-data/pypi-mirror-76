import requests

BASEURL = 'https://ha.monitoring.solaredge.com/api/homeautomation/v1.0'

COOKIE_NAME = "SPRING_SECURITY_REMEMBER_ME_COOKIE"


class SolaredgeHa(object):
    """
    Object containing SolarEdge's Home Automation site API-methods.
    """

    def __init__(self, site, site_token):
        """
        To communicate, you need to set a site and site token.
        Get it from your account.

        Parameters
        ----------
        site : str
        site_token : str
        """
        self.site = site
        self.token = site_token

    def get_devices(self):
        """
        Request devices

        Returns
        -------
        dict
        """

        url = urljoin(BASEURL, "sites", self.site, "devices")

        cookies = dict(SPRING_SECURITY_REMEMBER_ME_COOKIE=self.token)

        r = requests.get(url, cookies=cookies)
        r.raise_for_status()
        return r.json()

    def activate_device(self, reporterId, level, duration=None):
        """
        Activate devices

        Returns
        -------
        dict
        """

        url = urljoin(BASEURL, self.site, "devices", reporterId, "activationState")

        cookies = dict(SPRING_SECURITY_REMEMBER_ME_COOKIE=self.token)

        params = {
            "mode": "MANUAL",
            "level": level,
            "duration": duration
        }

        print("Params:")
        print(params)

        r = requests.put(url, json=params, cookies=cookies)
        r.raise_for_status()
        return r.json()


def urljoin(*parts):
    """
    Join terms together with forward slashes

    Parameters
    ----------
    parts

    Returns
    -------
    str
    """
    # first strip extra forward slashes (except http:// and the likes) and
    # create list
    part_list = []
    for part in parts:
        p = str(part)
        if p.endswith('//'):
            p = p[0:-1]
        else:
            p = p.strip('/')
        part_list.append(p)
    # join everything together
    url = '/'.join(part_list)
    return url
