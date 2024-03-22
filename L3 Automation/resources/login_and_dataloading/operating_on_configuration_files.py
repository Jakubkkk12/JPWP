import json
import Crypto
from resources.devices.NetworkDevice import NetworkDevice
from resources.devices.Router import Router
from resources.ssh.SSHInformation import SSHInformation
from Crypto.Cipher import AES


def check_file_extension(file_path: str) -> None:
    if not file_path.endswith('.jkal'):
        raise ValueError('Wrong file extension')
    return None


def get_aes_cipher(aes_key: str, aes_iv: bytes = None) -> Crypto.Cipher:
    aes_key: bytes = aes_key.encode('utf8')
    try:
        if aes_iv is None:
            cipher = AES.new(aes_key, AES.MODE_OFB)
        else:
            cipher = AES.new(aes_key, AES.MODE_OFB, aes_iv)
        print(cipher)
    except ValueError:
        raise Exception('Wrong key format')
    return cipher


def save_project(file_path: str, aes_key: str, devices: dict[str, NetworkDevice]) -> None:
    check_file_extension(file_path)

    list_of_devices = list(devices.values())
    configuration_data: str = '[\n'
    for device in list_of_devices[:-1]:
        configuration_data += device.to_json() + ',\n'
    configuration_data += list_of_devices[-1].to_json() + '\n]'

    configuration_data_bytes: bytes = configuration_data.encode()
    cipher = get_aes_cipher(aes_key)
    configuration_data_encrypted: bytes = cipher.encrypt(configuration_data_bytes)

    with open(file_path, mode='wb') as file:
        file.write(cipher.IV)
        file.write(configuration_data_encrypted)
    return None


def get_list_of_devices_in_json_from(decrypted_data: bytes):
    try:
        return json.loads(decrypted_data)
    except UnicodeDecodeError:
        raise UnicodeDecodeError('Unable to decode')


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


def open_project(file_path: str, aes_key: str) -> dict[str, NetworkDevice]:
    check_file_extension(file_path)

    with open(file_path, mode='rb') as file:
        aes_iv: bytes = file.read(16)
        cipher = get_aes_cipher(aes_key, aes_iv)
        decrypted_data = cipher.decrypt(file.read())

    list_of_devices_json = get_list_of_devices_in_json_from(decrypted_data)
    devices: dict[str, NetworkDevice] = {}
    for device in list_of_devices_json:
        ssh_ip_addresses: dict[str, str] = {}
        for key, ip_address in device['ssh_information']['ip_addresses'].items():
            ssh_ip_addresses[f'{key}'] = ip_address

        devices[device['name']] = get_device(class_name=device['class'],
                                             device=device,
                                             ssh_ip_addresses=ssh_ip_addresses)
    return devices


def add_new_user(username: str, hash_password: str) -> None:
    with open('../../app_conf_files/username.txt', 'at') as file:
        file.write(f'{username} {hash_password}')
    return None
