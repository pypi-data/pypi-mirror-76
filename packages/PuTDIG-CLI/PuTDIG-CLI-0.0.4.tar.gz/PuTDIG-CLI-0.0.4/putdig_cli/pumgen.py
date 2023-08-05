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
import json
import sys
from plumbum import cli
from pathlib import Path
from enum import Enum

from putdig.common import import_bus_telemetry_definition, export_dataclass, \
        SupMCUModuleTelemetrySet, Telemetry, import_bus_telemetry, validate_value
from pumpkin_supmcu.supmcu import TelemetryDataItem


options = """
B. Back
Q. Quit and save
Ctrl-C to quit without saving
"""


class ResponseType(Enum):
    """The type of response recieved through user input"""
    NORMAL = 1
    BACK = 2


class PumGen(cli.Application):
    """A command line program to generate and edit telemetry"""
    def_file = cli.SwitchAttr(
        ["-d", "--input-file"],
        str,
        mandatory=True,
        help="The definiton file to pattern the telemetry data after or a telemetry file to edit a copy of"
    )
    """The definiton file to pattern the telemetry data after or a telemetry file to edit a copy of"""
    file = cli.SwitchAttr(
        ["-f", "--output-file"],
        str,
        default=None,
        help="The file to save JSON data to"
    )
    """The file to save JSON data to"""
    quiet = cli.Flag(
        ["-q", "--quiet"],
        requires=("--output-file",),
        excludes=("--interactive",),
        help="Runs without outputing anything to stdout"
    )
    """Runs without outputing anything to stdout"""
    pretty = cli.Flag(
        ["-p", "--pretty"],
        excludes=("--interactive",),
        help="Format the JSON output"
    )
    """Format the JSON output"""
    interactive = cli.Flag(
        ["-i", "--interactive"],
        excludes=("--pretty", "--quiet", "--module"),
        help="Starts an interactive session for manually setting telemetry values",
    )
    """Starts an interactive session for manually setting telemetry values"""
    module = cli.SwitchAttr(
        ["-m", "--module"],
        str,
        default='',
        requires=("--telemetry", "--value"),
        help="What module to edit the data for",
        group="Editing"
    )
    """What module to edit the data for"""
    telemetry = cli.SwitchAttr(
        ["-t", "--telemetry"],
        str,
        default='',
        requires=("--module", "--value"),
        help="What telemetry to edit from the slected module",
        group="Editing"
    )
    """What telemetry to edit from the slected module"""
    item = cli.SwitchAttr(
        ["-n", "--item"],
        int,
        default=-1,
        requires=("--module", "--telemetry", "--value"),
        help="The number of the item to edit, if you are only editing one value of a telemetry object with more than one",
        group="Editing"
    )
    """The number of the item to edit, if you are only editing one value of a telemetry object with more than one"""
    value = cli.SwitchAttr(
        ["-v", "--value"],
        str,
        default='',
        requires=("--module", "--telemetry"),
        help="The value to set the telemetry item to.",
        group="Editing"
    )
    """The value to set the telemetry item to."""

    def main(self):
        """
        Main entry point for pumgen, can be run in interactive mode or edit/generate telemetry set.
        """
        # Load module set
        # Assume module definition, if unable to deserialize, import as previously generated telemetry set.
        try:
            module_defs = import_bus_telemetry_definition(Path(self.def_file))
            self.modules = [SupMCUModuleTelemetrySet.from_definition(mod_def) for mod_def in module_defs]
        except KeyError:
            self.modules = import_bus_telemetry(Path(self.def_file))
        if not self.interactive:
            self.main_non_interactive()
        else:
            # Enter interactive mode
            try:
                self.choose_module()
            except KeyboardInterrupt:
                print("\n\nExiting without saving")
                sys.exit(0)

    def main_non_interactive(self):
        """
        Main function when the `-i` flag is missing from the parameter set.
        """
        # Non interactive mode
        # If a value is specified, user must be editing existing value.
        if self.value != '':
            try:
                mod = next(m for m in self.modules if m.name.lower() == self.module.lower())
            except StopIteration as e:
                raise ValueError(f"{self.module} is not a module in this file") from e
            try:
                telemetries = mod.module_telemetry + mod.supmcu_telemetry
                telem = next(t for t in telemetries if t.name.lower() == self.telemetry.lower())
            except StopIteration as e:
                raise ValueError(f"{self.telemetry} was not found in {mod.name}") from e
            try:
                if self.item == -1 and len(telem.sup_telemetry.items) > 1:
                    raise ValueError(f"{telem.name} has more than one data item, please select one with the --item flag")
                it = telem.sup_telemetry.items[self.item]
            except IndexError as e:
                raise ValueError(f"{self.item} is not a valid telemetry data item index in {telem.name}") from e
            val = validate_value(self.value, it.data_type, idx=self.item, max_size=telem.size)
            if not val:
                raise ValueError(f"`{self.value}` is not a valid value for {self.telemetry}[{self.item}].")
            it.set_value(val)
        # Save telemetry set to file, or just dump to stdout if no file specified
        if self.file is not None:
            export_dataclass(self.modules, Path(self.file))
            if not self.quiet:
                if self.pretty:
                    print(json.dumps(json.loads(export_dataclass(self.modules)), indent=4))
                else:
                    print(export_dataclass(self.modules))
        else:
            if self.pretty:
                print(json.dumps(json.loads(export_dataclass(self.modules)), indent=4))
            else:
                print(export_dataclass(self.modules))

    def check_options(self, user_input: str) -> ResponseType:
        """
        Checks the user input for commands.

        :param user_input: The string inputted by the user
        :return: an enum saying whether or not the input is normal, and if not, what command to run
        """
        user_input = user_input.lower().strip()
        if user_input == "b":
            return ResponseType.BACK
        elif user_input == "q":
            self.quit()
        else:
            return ResponseType.NORMAL

    def choose_module(self):
        """
        Gives the user a choice of what module to edit
        """
        while True:
            print("\nWelcome to pumgen, please select a module to set telemetry for:\n")
            # Listing the options
            for idx, mod in enumerate(self.modules):
                print(f"{str(idx + 1) + '.':<3} {mod.name}")
            print(options)
            choice = input("Choice: ")
            if self.check_options(choice) == ResponseType.BACK:
                self.choose_module()
            elif self.check_options(choice) == ResponseType.NORMAL:
                # Making sure that the choice is an integer
                try:
                    choice = int(choice)
                except ValueError:
                    print("Please choose a module by entering its number.")
                    continue
                # Making sure that the number inputed is one of the options
                if choice > len(self.modules):
                    print("Please choose a one of the displayed modules")
                    continue
                self.choose_telemetry(self.modules[choice - 1])

    def choose_telemetry(self, module: SupMCUModuleTelemetrySet):
        """
        Gives a user a choice of what telemetry to edit from the selected module

        :param module: What module to edit the telemetry of.
        """
        while True:
            print(f"\nPlease select a telemetry in the {module.name} to set value for:\n")
            telemetry = module.supmcu_telemetry + module.module_telemetry
            telemetry = [tel for tel in telemetry if tel.simulatable == True]
            # Listing the options
            for idx, telem in enumerate(telemetry):
                print(f"{str(idx + 1) + '.':<3} [{str(telem.type).split('.')[-1]}] {telem.name}")
            print(options)
            choice = input("Choice: ")
            if self.check_options(choice) == ResponseType.BACK:
                return
            elif self.check_options(choice) == ResponseType.NORMAL:
                # Making sure that the choice is an integer
                try:
                    choice = int(choice)
                except ValueError:
                    print("Please choose a telemetry item by entering its number.")
                    continue
                # Making sure that the number inputed is one of the options
                if choice > len(telemetry):
                    print("Please choose one of the displayed telemetry items")
                    continue

                print(f"Selected: {module.name} -> [{str(telemetry[choice - 1].type).split('.')[-1]}] {telemetry[choice - 1].name}")
                if len(telemetry[choice - 1].sup_telemetry.items) == 1:
                    print("Current value: " + telemetry[choice - 1].sup_telemetry.items[0].string_value)
                    self.edit_item(telemetry[choice - 1].sup_telemetry.items[0], max_size=telemetry[choice - 1].size)
                else:
                    self.choose_item(telemetry[choice - 1])

    def choose_item(self, telemetry: Telemetry):
        """
        If the given telemetry has more than one data item, this function
        offers a choice between them

        :param telemetry: the telemtry object to edit a data item from
        """
        while True:
            print("Current Values:")
            # Listing the options
            for idx, item in enumerate(telemetry.sup_telemetry.items):
                print(f"\t{idx + 1:<2} [{str(item.data_type).split('.')[-1]}]. {item.string_value}")
            print(options)
            choice = input("Choice: ")
            if self.check_options(choice) == ResponseType.BACK:
                return
            elif self.check_options(choice) == ResponseType.NORMAL:
                # Making sure that the choice is an integer
                try:
                    choice = int(choice)
                except ValueError:
                    print("Please choose a value to edit by entering its number.")
                    continue
                # Making sure that the number inputed is one of the options
                if choice > len(telemetry.sup_telemetry.items):
                    print("Please choose one of the displayed telemetry values")
                    continue
                self.edit_item(telemetry.sup_telemetry.items[choice - 1], choice)

    def edit_item(self, item: TelemetryDataItem, idx: int = -1, max_size: int = -1):
        """
        Allows a user to modify a :any:`TelemtryDataItem`'s value, and verifies that the inputed value is valid

        :param item: The data item to edit
        :param idx: If there are more than on data items in the parent SupMCUTelemetry object, this is the index of the selected one
        :param max_size: The maximum size of the telemetry data.  Only matters when this is the only data item in its parent.
        """
        while True:
            # Printing a prompt that looks like:
            # New Value [<data type> (e.g. Hex8)]: <user input here>
            # or
            # New Value for #<number selected> [<data type> (e.g. uint16_t)]: <user input here>
            print("New value", end='')
            if idx != -1:
                print(" for #" + str(idx), end='')
            val = input(f" [{str(item.data_type).split('.')[-1]}]: ")
            if self.check_options(val) == ResponseType.BACK:
                # Return back to the previous function, no value specified
                return

            # Validate value, set if valid value.
            val = validate_value(val, item.data_type, idx, max_size)
            if val is not False:
                item.set_value(val)
                return
            else:
                continue

    def quit(self):
        """
        If not specified in the flags, this allows the user to select a filename to save to, and then save the edited telemetry data before exiting.
        """
        if self.file is None:
            self.file = input("Filename to data as: ")
        export_dataclass(self.modules, Path(self.file))
        print(f"Saved data as \"{self.file}\"")
        sys.exit(0)


def execute():
    PumGen.run()


if __name__ == "__main__":
    execute()
