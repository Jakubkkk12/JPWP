import json
import Crypto
from resources.devices.NetworkDevice import NetworkDevice
from resources.devices.Router import Router
from resources.ssh.SSHInformation import SSHInformation
from Crypto.Cipher import AES


def get_aes_cipher(aes_key: str, aes_iv: bytes = None) -> Crypto.Cipher:
    aes_key: bytes = aes_key.encode('utf8')
    try:
        if aes_iv is None:
            cipher = AES.new(aes_key, AES.MODE_OFB)
        else:
            cipher = AES.new(aes_key, AES.MODE_OFB, aes_iv)
    except ValueError:
        raise Exception('Wrong key format')
    return cipher


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


def add_new_user(username: str, hash_password: str) -> None:
    with open('../../app_conf_files/username.txt', 'at') as file:
        file.write(f'{username} {hash_password}')
    return None
