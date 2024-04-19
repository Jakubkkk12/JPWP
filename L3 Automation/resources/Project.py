from dataclasses import dataclass
from resources.devices.NetworkDevice import NetworkDevice
from resources.user.User import User
from resources.login_and_dataloading.operating_on_project_files import (get_aes_cipher, get_device,
                                                                        get_list_of_devices_in_json_from)


@dataclass(slots=True, kw_only=True)
class Project:
    file_path: str = ''
    devices: dict[str, NetworkDevice]
    current_user: User = None

    def check_file_extension(self) -> None:
        if not self.file_path.endswith('.jkal'):
            raise ValueError('Wrong file extension')
        return None

    def open_project(self, aes_key: str) -> None:
        self.check_file_extension()

        with open(self.file_path, mode='rb') as file:
            aes_iv: bytes = file.read(16)
            cipher = get_aes_cipher(aes_key, aes_iv)
            decrypted_data = cipher.decrypt(file.read())

        list_of_devices_json = get_list_of_devices_in_json_from(decrypted_data)
        self.devices: dict[str, NetworkDevice] = {}
        for device in list_of_devices_json:
            ssh_ip_addresses: dict[str, str] = {}
            for key, ip_address in device['ssh_information']['ip_addresses'].items():
                ssh_ip_addresses[f'{key}'] = ip_address

            self.devices[device['name']] = get_device(class_name=device['class'],
                                                      device=device,
                                                      ssh_ip_addresses=ssh_ip_addresses)
        return None

    def save_project(self, aes_key: str) -> None:
        self.check_file_extension()

        list_of_devices = list(self.devices.values())
        project_data: str = '[\n'
        for device in list_of_devices[:-1]:
            project_data += device.to_json() + ',\n'
        project_data += list_of_devices[-1].to_json() + '\n]'

        project_data_bytes: bytes = project_data.encode()
        cipher = get_aes_cipher(aes_key)
        project_data_encrypted: bytes = cipher.encrypt(project_data_bytes)

        with open(self.file_path, mode='wb') as file:
            file.write(cipher.IV)
            file.write(project_data_encrypted)
        return None
