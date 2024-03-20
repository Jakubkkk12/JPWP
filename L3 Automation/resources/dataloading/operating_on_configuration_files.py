import json
from resources.devices.NetworkDevice import NetworkDevice
from resources.devices.Router import Router
from resources.ssh.SSHInformation import SSHInformation


def get_device(class_name: str, device: dict, ssh_ip_addresses: dict[str, str]) -> NetworkDevice | Router:
    if class_name == "Router":
        return Router(name=device['name'],
                      type=device['type'],
                      ssh_information=SSHInformation(ip_addresses=ssh_ip_addresses,
                                                     port=device['ssh_information']['port'])
                      )
    if class_name == "NetworkDevice":
        return NetworkDevice(name=device['name'],
                             ssh_information=SSHInformation(ip_addresses=ssh_ip_addresses,
                                                            port=device['ssh_information']['port'])
                             )
    raise Exception("Wrong class name")


def save_project(file_path: str, devices: dict[str, NetworkDevice]) -> None:
    # Zapewne jakieś errory bedę sie zobaczy
    with open(file_path, mode='wt') as file:
        file.write('[\n')
        list_of_devices = list(devices.values())
        for device in list_of_devices[:-1]:
            file.write(device.to_json())
            file.write(',\n')
        file.write(list_of_devices[-1].to_json())
        file.write('\n]')

    return None


def open_project(file_path: str) -> dict[str, NetworkDevice] | None:
    # Zapewne jakieś errory bedę sie zobaczy
    if file_path.endswith('.jkal'):
        with open(file_path, mode='rt') as file:
            list_of_devices_json = json.loads(file.read())
            devices: dict[str, NetworkDevice] = {}
            for device in list_of_devices_json:
                ssh_ip_addresses: dict[str, str] = {}
                for key, ip_address in device['ssh_information']['ip_addresses'].items():
                    ssh_ip_addresses[f'{key}'] = ip_address

                devices[device['name']] = get_device(class_name=device['class'],
                                                     device=device,
                                                     ssh_ip_addresses=ssh_ip_addresses)
        return devices
    return None
