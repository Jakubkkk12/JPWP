import netmiko
from netmiko import ConnectHandler
from resources.devices.Router import Router
from contextlib import contextmanager
from resources.user.User import User


class Connection:
    def __init__(self, router: Router, user: User) -> None:
        for key, ssh_ip in router.ssh_information.ip_addresses.items():
            try:
                conn_handler: ConnectHandler = ConnectHandler(host=ssh_ip,
                                                              port=router.ssh_information.port,
                                                              username=user.username,
                                                              password=user.ssh_password,
                                                              secret=router.enable_password,
                                                              device_type=router.type)
                conn_handler.enable()
            except Exception:
                continue
            self.connection = conn_handler
            return None
        raise Exception("Cannot connect to router")

    def __enter__(self) -> ConnectHandler:
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.connection.disconnect()
        return None


def execute_conf_commands(router: Router, user: User, commands: str | list[str],
                          connection: netmiko.BaseConnection | None = None) -> str:
    is_connection = False if connection is None else True
    if is_connection:
        output: list = connection.send_config_set(commands).splitlines()[2:-2]
    else:
        with open_connection(router=router, user=user) as connection:
            output: list = connection.send_config_set(commands).splitlines()[2:-2]

    output.insert(0, f'Configuring {router.name}')
    output.append(f'End')
    return '\n'.join(output)


@contextmanager
def open_connection(router: Router, user: User):
    connection = None
    for key, ssh_ip in router.ssh_information.ip_addresses.items():
        try:
            conn_handler: ConnectHandler = ConnectHandler(host=ssh_ip,
                                                          port=router.ssh_information.port,
                                                          username=user.username,
                                                          password=user.ssh_password,
                                                          secret=router.enable_password,
                                                          device_type=router.type)
            conn_handler.enable()
        except Exception:
            continue
        connection = conn_handler
        break
    if connection is None:
        raise Exception("Cannot connect to router")

    try:
        yield connection
    finally:
        connection.disconnect()


def execute_conf_commands_v2(router: Router, user: User, commands: str | list[str],
                             connection: netmiko.BaseConnection | None = None) -> str:
    is_connection = False if connection is None else True
    if is_connection:
        output: list = connection.send_config_set(commands).splitlines()[2:-2]
    else:
        with open_connection(router=router, user=user) as connection:
            output: list = connection.send_config_set(commands).splitlines()[2:-2]

    output.insert(0, f'Configuring {router.name}')
    output.append(f'End')
    return '\n'.join(output)


if __name__ == "__main__":
    from resources.ssh.SSHInformation import SSHInformation

    u = User(username='admin12', ssh_password='ZAQ!2wsx')
    r = Router(name='R1',
               ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1'}),
               type='cisco_ios',
               enable_password='ZSEDCxzaqwe')

    print(execute_conf_commands_v2(router=r, user=u, commands='do sh version'))
    print(execute_conf_commands(router=r, user=u, commands='do sh process cpu'))
