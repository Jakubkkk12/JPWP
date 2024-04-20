import netmiko
from netmiko import ConnectHandler
from resources.devices.Router import Router
from resources.user.User import User


def connection_enable_test(connection: netmiko.BaseConnection) -> bool:
    try:
        connection.enable()
    except Exception:
        return False
    return True


def create_connection_to_router(router: Router, user: User) -> netmiko.BaseConnection:
    for key, ssh_ip in router.ssh_information.ip_addresses.items():
        try:
            conn_handler = ConnectHandler(host=ssh_ip,
                                          port=router.ssh_information.port,
                                          username=user.username,
                                          password=user.ssh_password,
                                          secret=router.enable_password,
                                          device_type=router.type
                                          )
        except TimeoutError as e:
            # print w konsoli aplikacji
            continue
        return conn_handler
    raise Exception("Cannot connect to router")


def close_connection(connection: netmiko.BaseConnection) -> None:
    connection.disconnect()


def execute_conf_commands(router: Router, user: User, commands: str | list[str],
                          connection: netmiko.BaseConnection | None = None) -> str:
    is_connection = False if connection is None else True
    if not is_connection:
        connection = create_connection_to_router(router, user)
        connection.enable()

    output: str = connection.send_config_set(commands)

    if not is_connection:
        close_connection(connection)

    try:
        _: list = output.splitlines()[2:-2]
        _.insert(0, f'Configuring {router.name}')
        _.append(f'End')
        return '\n'.join(_)
    except IndexError:
        return f'Execution on {router.name} failed'
