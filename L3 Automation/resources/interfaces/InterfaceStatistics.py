from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class ErrorsStatistics:
    """
    Represents statistics related to errors on an interface.

    Attributes:
        input_errors (int, optional): The number of input errors on the interface. Defaults to None.
        output_errors (int, optional): The number of output errors on the interface. Defaults to None.
        output_buffer_failures (int, optional): The number of output buffer failures on the interface. Defaults to None.
        runts (int, optional): The number of runts (undersized frames) on the interface. Defaults to None.
        giants (int, optional): The number of giants (oversized frames) on the interface. Defaults to None.
        crc (int, optional): The number of CRC (Cyclic Redundancy Check) errors on the interface. Defaults to None.
        frame (int, optional): The number of frame errors on the interface. Defaults to None.
        throttles (int, optional): The number of throttles (flow control events) on the interface. Defaults to None.
        overrun (int, optional): The number of overrun errors on the interface. Defaults to None.
        ignored (int, optional): The number of ignored errors on the interface. Defaults to None.
    """
    input_errors: int = None
    output_errors: int = None
    output_buffer_failures: int = None
    runts: int = None
    giants: int = None
    crc: int = None
    frame: int = None
    throttles: int = None
    overrun: int = None
    ignored: int = None


@dataclass(slots=True, kw_only=True)
class InformationStatistics:
    """
    Represents statistics related to information and status of a network interface.

    Attributes:
        collision (int, optional): The number of collisions detected on the interface. Defaults to None.
        late_collision (int, optional): The number of late collisions detected on the interface. Defaults to None.
        broadcast (int, optional): The number of broadcast packets received on the interface. Defaults to None.
        packets_input (int, optional): The total number of packets input on the interface. Defaults to None.
        packets_output (int, optional): The total number of packets output on the interface. Defaults to None.
        duplex (str, optional): The duplex mode of the interface (e.g., full, half). Defaults to None.
        speed (str, optional): The speed of the interface (e.g., 10 Mbps, 1 Gbps). Defaults to None.
        layer1_status (str, optional): The layer 1 status of the interface (e.g., up, down). Defaults to None.
        layer2_status (str, optional): The layer 2 status of the interface (e.g., up, down). Defaults to None.
        mtu (int, optional): The Maximum Transmission Unit (MTU) size of the interface. Defaults to None.
        encapsulation (str, optional): The encapsulation type of the interface (e.g., Ethernet, Serial). Defaults to None.
    """
    collision: int = None
    late_collision: int = None
    broadcast: int = None
    packets_input: int = None
    packets_output: int = None
    duplex: str = None
    speed: str = None
    layer1_status: str = None
    layer2_status: str = None
    mtu: int = None
    encapsulation: str = None


@dataclass(slots=True, kw_only=True)
class InterfaceStatistics:
    """
    Represents statistics related to a network interface.

    Attributes:
        information (InformationStatistics, optional): Statistics related to information and status of the interface. Defaults to None.
        errors (ErrorsStatistics, optional): Statistics related to errors on the interface. Defaults to None.
    """
    information: InformationStatistics = None
    errors: ErrorsStatistics = None
