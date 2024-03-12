from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class User:
    """
        Represents a user with SSH access.

        Attributes:
            username (str): The username of the user.
            ssh_password (str, optional): The SSH password of the user. Defaults to None.
    """
    username: str
    ssh_password: str = None
