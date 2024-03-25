from dataclasses import dataclass
import json
from resources.ssh.SSHInformation import SSHInformation


@dataclass(slots=True, kw_only=True)
class NetworkDevice:
    """
    Represents a network device with SSH (Secure Shell) information.

    Attributes:
        name (str): The name of the network device.
        ssh_information (SSHInformation): SSH connection information for the network device.
    """
    name: str
    ssh_information: SSHInformation

    def to_json(self) -> str:
        """
        Convert the Router instance to a JSON string.

        Returns:
            str: JSON string representing the Router instance.
        """
        attributes_to_json: dict = {'class': 'NetworkDevice',
                                    'name': self.name,
                                    'ssh_information': {'ip_addresses': self.ssh_information.ip_addresses,
                                                        'port': self.ssh_information.port}
                                    }
        return json.dumps(attributes_to_json, indent=4)

    def loads_from_json(self, filename: str) -> None:
        """
        Load Router instance attributes from a JSON file.

        Args:
            filename (str): The path to the JSON file containing the Router instance attributes.

        Returns:
            None
        """
        attributes_form_json: dict = json.loads(filename)
        self.name = attributes_form_json['name']
        self.ssh_information = SSHInformation(ip_addresses=attributes_form_json['ssh_information']['ip_addresses'],
                                              port=attributes_form_json['ssh_information']['port'])
        return None
