import json

data = {"device_name":"msi_notebook"}


with open('device_config.txt', 'w') as outfile:
    json.dump(data, outfile)