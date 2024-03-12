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

    def __str__(self):
        """
               Returns a string representation of the SSH information.

               Returns:
                   str: A formatted string containing IP addresses and port information.
        """
        return (f"SSH Information: \n"
                f"Available IP addresses: {self.ip_addresses}\n"
                f"SSH port: {self.port}\n")
