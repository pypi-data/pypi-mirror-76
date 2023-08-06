import json
from py3nvml.py3nvml import *


def get_device_uuids():
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
        h = nvmlDeviceGetHandleByIndex(i)
        yield nvmlDeviceGetUUID(h)


def configure(path='/etc/docker/daemon.json', key='NVIDIA-GPU'):
    try:
        with open(path) as f:
            conf = json.load(f)
    except:
        conf = {}

    resources = conf.get('node-generic-resources', [])
    resources = [r for r in resources if not r.startswith(key+'=')]
    for uuid in get_device_uuids():
        resources.append(key+'='+uuid)
    conf['node-generic-resources'] = resources

    with open(path, 'w') as f:
        json.dump(conf, f, indent=2)


if __name__ == '__main__':
    configure()
