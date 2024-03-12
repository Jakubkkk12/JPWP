from dataclasses import dataclass
import json
from resources.ssh.SSHInformation import SSHInformation
from resources.interfaces.RouterInterface import RouterInterface
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.rip.RIPInformation import RIPInformation
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.devices.NetworkDevice import NetworkDevice


@dataclass(slots=True, kw_only=True)
class Router(NetworkDevice):
    """
    Represents a router device with additional configuration.

    Attributes:
        name (str): The name of the router.
        ssh_information (SSHInformation): SSH connection information for the router.
        type (str): The type of the router.
        enable_password (str, optional): The enable password for accessing privileged mode. Defaults to None.
        interfaces (dict[str, RouterInterface], optional): Dictionary of router interfaces, where keys are interface names and values are RouterInterface objects. Defaults to None.
        static_routes (dict[str, StaticRoute], optional): Dictionary of static routes, where keys are route names and values are StaticRoute objects. Defaults to None.
        ospf (OSPFInformation, optional): OSPF (Open Shortest Path First) configuration information for the router. Defaults to None.
        rip (RIPInformation, optional): RIP (Routing Information Protocol) configuration information for the router. Defaults to None.
        bgp (BGPInformation, optional): BGP (Border Gateway Protocol) configuration information for the router. Defaults to None.
    """
    type: str
    enable_password: str = None
    interfaces: dict[str, RouterInterface] = None
    static_routes: dict[str, StaticRoute] = None
    ospf: OSPFInformation = None
    rip: RIPInformation = None
    bgp: BGPInformation = None

    def to_json(self) -> str:
        """
        Convert the Router instance to a JSON string.

        Returns:
            str: JSON string representing the Router instance.
        """
        attributes_to_json: dict = {'name': self.name,
                                    'type': self.type,
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
        self.type = attributes_form_json['type']
        self.ssh_information = SSHInformation(ip_addresses=attributes_form_json['ssh_information']['ip_addresses'],
                                              port=attributes_form_json['ssh_information']['port'])
        return None
