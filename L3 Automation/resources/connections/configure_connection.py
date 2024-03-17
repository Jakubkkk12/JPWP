import netmiko
from netmiko import ConnectHandler
from resources.devices.Router import Router
from resources.user.User import User


def connection_test(connection: netmiko.BaseConnection) -> bool:
    pass


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


