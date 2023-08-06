# SolarEdge Home Automation
API wrapper for SolarEdge Home Automation service.

This is an undocumented api.

## Create a new connection by supplying your Solaredge HA token
```
s = solaredgeHa.SolaredgeHa(siteId, token)
```

where ```siteId``` is the SolarEdge site id and ```token``` is the value of the
```SPRING_SECURITY_REMEMBER_ME_COOKIE``` cookie when logged in to the Smart Home section of the
SolarEdge site.

## API Requests
2 API requests are supported. The methods return the parsed JSON response as a dict.

```
def get_devices(self):

def activate_device(self, reporterId, level, duration=None):

```

