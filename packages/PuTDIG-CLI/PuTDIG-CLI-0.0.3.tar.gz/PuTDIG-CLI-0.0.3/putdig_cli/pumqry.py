#!/usr/bin/env python3
# coding: utf-8
###############################################################################
# (C) Copyright 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                             #
# This file may be distributed under the terms of the License                 #
# Agreement provided with this software.                                      #
#                                                                             #
# THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
# INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
# FITNESS FOR A PARTICULAR PURPOSE.                                           #
###############################################################################

from plumbum import cli

# Try and import all of the various I2CMaster implementations.
try:
    from pumpkin_supmcu.i2cdriver import I2CDriverMaster
except ImportError:
    I2CDriverMaster = None
try:
    from pumpkin_supmcu.linux import I2CLinuxMaster
except ImportError:
    I2CLinuxMaster = None
try:
    from pumpkin_supmcu.aardvark import I2CAardvarkMaster
except ImportError:
    I2CAardvarkMaster = None
try:
    from pumpkin_supmcu.kubos import I2CKubosMaster
except ImportError:
    I2CKubosMaster = None

from putdig.common import export_dataclass, discover_bus_telemetry, SupMCUModuleTelemetrySet
from pathlib import Path
import json
import sys


class PumQry(cli.Application):
    """
    A command line program that takes in a set of flags then outputs the telemetry definition or data.
    """
    port = cli.SwitchAttr(
        ["-p", "--port"],
        str,
        mandatory=True,
        help="COM# (Windows), device path (Linux, type i2cdriver), or bus # (Linux/Kubos, type linux/kubos) to I2C "
             "Master device "
    )
    i2c_type = cli.SwitchAttr(
        ["-t", "--type"],
        str,
        mandatory=True,
        help="Type of I2C device at -p. Can be i2cdriver, aardvark, linux, kubos, all other values rejected"
    )
    file = cli.SwitchAttr(
        ["-f", "--file"],
        str,
        default=None,
        help="The file to save JSON data to"
    )
    quiet = cli.Flag(
        ["-q", "--quiet"],
        requires=("--file",),
        help="Runs without outputing anything to stdout"
    )
    pretty = cli.Flag(
        ["-d", "--pretty"],
        help="Format the JSON output"
    )
    list_addrs = cli.Flag(
        ["-l", "--list"],
        requires=("--port", "--type"),
        excludes=("--file", "--quiet", "--pretty"),
        help="List all of the available i2c addresses without getting telemetry data"
    )
    definition = cli.Flag(
        ["-e", "--definition"],
        help="Saves the telemetry as a telemetry definition instead of telemetry data"
    )

    def main(self, *addresses: str):
        self.i2c_type = self.i2c_type.lower()
        if self.i2c_type == "i2cdriver":
            if I2CDriverMaster is None:
                raise NotImplementedError("I2CDriverMaster is not implemented for this system")
            i2c_master = I2CDriverMaster(self.port)
        elif self.i2c_type == "aardvark":
            if I2CAardvarkMaster is None:
                raise NotImplementedError("I2CAardvarkMaster is not implemented for this system")
            i2c_master = I2CAardvarkMaster(self.port)
        elif self.i2c_type == "linux":
            if I2CLinuxMaster is None:
                raise NotImplementedError("I2CLinuxMaster is not implemented for this system")
            i2c_master = I2CLinuxMaster(int(self.port))
        elif self.i2c_type == "kubos":
            if I2CKubosMaster is None:
                raise NotImplementedError("I2CKubosMaster is not implemented for this system")
            i2c_master = I2CKubosMaster(int(self.port))
        else:
            raise ValueError("Type must be 'i2cdriver, 'aardvark', or 'linux'")
        # converts the addresses from strings to base 10 integers
        if self.list_addrs:
            print(*(hex(addr) for addr in i2c_master.get_bus_devices()), sep=" ")
            sys.exit(0)
        addresses = tuple(int(addr, 16) for addr in addresses)
        if len(addresses) > 0:
            telemetry = discover_bus_telemetry(i2c_master, addresses)
        else:
            telemetry = discover_bus_telemetry(i2c_master)
        if not self.definition:
            telemetry = [SupMCUModuleTelemetrySet.from_definition(mod_def) for mod_def in telemetry]
        if self.file is not None:
            export_dataclass(telemetry, Path(self.file))
            if not self.quiet:
                if self.pretty:
                    print(json.dumps(json.loads(export_dataclass(telemetry)), indent=4))
                else:
                    print(export_dataclass(telemetry))
        else:
            if self.pretty:
                print(json.dumps(json.loads(export_dataclass(telemetry)), indent=4))
            else:
                print(export_dataclass(telemetry))


def execute():
    PumQry.run()


if __name__ == "__main__":
    execute()
