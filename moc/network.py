STA_IF = 0


class WLAN:
    def __init__(self, interface_id: int):
        pass

    def active(self, is_active: bool) -> None:
        """Activate ("up") or deactivate ("down") network interface."""
        ...

    def connect(self, ap, pwd):
        pass

    def disconnect(self) -> None:
        """Disconnect from the currently connected wireless network."""
        ...

    def scan(self):
        pass

    def status(self) -> int:
        """Return the current status of the wireless connection.

        The possible statuses are defined as constants:

            * ``STAT_IDLE`` -- no connection and no activity,
            * ``STAT_CONNECTING`` -- connecting in progress,
            * ``STAT_WRONG_PASSWORD`` -- failed due to incorrect password,
            * ``STAT_NO_AP_FOUND`` -- failed because no access point replied,
            * ``STAT_CONNECT_FAIL`` -- failed due to other problems,
            * ``STAT_GOT_IP`` -- connection successful.
        """
        ...

    def isconnected(self) -> bool:
        return True


    def ifconfig(self, ip: str, subnet: str, gateway: str, dns: str) -> None:
        """Get/set IP-level network interface parameters: IP address, subnet mask,
        gateway and DNS server.
        """
        ...


    def config(self, **kwargs) -> None:
        """Get or set general network interface parameters. These methods allow to work
        with additional parameters beyond standard IP configuration (as dealt with by
        `wlan.ifconfig()`). These include network-specific and hardware-specific
        parameters. For setting parameters, keyword argument syntax should be used,
        multiple parameters can be set at once. For querying, parameters name should
        be quoted as a string, and only one parameter can be queries at time::

            # Set WiFi access point name (formally known as ESSID) and WiFi channel
            ap.config(essid='My AP', channel=11)
            # Query params one by one
            print(ap.config('essid'))
            print(ap.config('channel'))

        Following are commonly supported parameters (availability of a specific parameter
        depends on network technology type, driver, and `MicroPython port`).

        =============  ===========
        Parameter      Description
        =============  ===========
        mac            MAC address (bytes)
        essid          WiFi access point name (string)
        channel        WiFi channel (integer)
        hidden         Whether ESSID is hidden (boolean)
        authmode       Authentication mode supported (enumeration, see module constants)
        password       Access password (string)
        dhcp_hostname  The DHCP hostname to use
        =============  ===========
        """
        ...