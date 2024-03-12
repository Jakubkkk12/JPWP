from dataclasses import dataclass
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
