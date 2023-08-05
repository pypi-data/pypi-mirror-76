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

from pumpkin_supmcu.supmcu import set_values, SupMCUSerialMaster, get_version_string
from putdig.common import compare_versions, import_bus_telemetry
from pathlib import Path


class PumInj(cli.Application):
    """
    A command line program that takes in a set of flags and injects the given telemetry into a SupMCU module.

    """
    port = cli.SwitchAttr(
        ["-p", "--port"],
        str,
        mandatory=True,
        help="COM# (Windows), device path (Linux, type i2cdriver), or bus # (Linux/Kubos, type linux/kubos) to I2C "
             "Master device or comma-separated list of serial ports for type serial"
    )
    i2c_type = cli.SwitchAttr(
        ["-t", "--type"],
        str,
        mandatory=True,
        help="Type of I2C device at -p. Can be i2cdriver, aardvark, linux, or serial, all other values rejected"
    )
    file = cli.SwitchAttr(
        ["-g", "--generated-set"],
        cli.ExistingFile,
        mandatory=True,
        help="The JSON file of generated telemetry to inject"
    )
    ignore = cli.Flag(
        ["-i", "--ignore"],
        help="If set, PumInj will ignore any extra modules in the file that are not found on the I2C bus"
    )

    def main(self):
        self.modules = import_bus_telemetry(Path(self.file))
        self.i2c_type = self.i2c_type.lower()
        if self.i2c_type == "i2cdriver":
            if I2CDriverMaster is None:
                raise NotImplementedError("I2CDriverMaster is not implemented for this system")
            master = I2CDriverMaster(self.port)
        elif self.i2c_type == "aardvark":
            if I2CAardvarkMaster is None:
                raise NotImplementedError("I2CAardvarkMaster is not implemented for this system")
            master = I2CAardvarkMaster(self.port)
        elif self.i2c_type == "linux":
            if I2CLinuxMaster is None:
                raise NotImplementedError("I2CLinuxMaster is not implemented for this system")
            master = I2CLinuxMaster(int(self.port))
        elif self.i2c_type == "kubos":
            if I2CKubosMaster is None:
                raise NotImplementedError("I2CKubosMaster is not implemented for this system")
            master = I2CKubosMaster(int(self.port))
        elif self.i2c_type == "serial":
            try:
                master = SupMCUSerialMaster([mod.cmd_name for mod in self.modules], self.port.split(','))
            except IndexError:
                if not self.ignore:
                    raise
        else:
            raise ValueError("Type must be 'i2cdriver, 'aardvark', 'linux', or 'serial'")
        if not isinstance(master, SupMCUSerialMaster):
            valid_addresses = master.get_bus_devices()
            addresses = [mod.address for mod in self.modules]
            for addr in addresses:
                if addr not in valid_addresses and not self.ignore:
                    raise IndexError("Modules to inject were not found on the I2C bus")
        for mod in self.modules:
            version = get_version_string(master, mod.address, mod.cmd_name)
            if compare_versions(version, mod.version):
                for telem in mod.module_telemetry:
                    if telem.simulatable:
                        set_values(master, mod.address, mod.cmd_name, telem.idx, telem.sup_telemetry.items)
            else:
                raise ValueError(f"Module version mismatch.  Expected value '{mod.version}' != '{version}'")


def execute():
    PumInj.run()


if __name__ == "__main__":
    execute()
