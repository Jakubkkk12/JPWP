from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class SSHInformation:
    """
    Represents SSH information including IP addresses and port.

    Attributes:
        ip_addresses (dict[str, str]): A dictionary containing IP addresses as keys and corresponding labels as values.
        port (int): The SSH port number. Default is 22.
    """
    ip_addresses: dict[str, str]
    port: int = 22

    def is_ip_address_in_ip_address(self, ip_address_key: str) -> bool:
        if ip_address_key in self.ip_addresses.keys():
            return True
        return False

    def add_ip_address(self, ip_address: str, ip_address_key: str) -> None:
        if self.is_ip_address_in_ip_address(ip_address_key):
            raise Exception('IP address already exists')
        self.ip_addresses[ip_address_key] = ip_address
        return None

    def remove_ip_address(self, ip_address_key: str) -> None:
        if self.is_ip_address_in_ip_address(ip_address_key):
            self.ip_addresses.pop(ip_address_key)

    def __str__(self) -> str:
        """
               Returns a string representation of the SSH information.

               Returns:
                   str: A formatted string containing IP addresses and port information.
        """
        return (f"SSH Information: \n"
                f"Available IP addresses: {self.ip_addresses}\n"
                f"SSH port: {self.port}\n")
