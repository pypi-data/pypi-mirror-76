# ##############################################################################
#  (C) Copyright 2019 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
from abc import abstractmethod
from enum import Enum
from typing import Protocol, NamedTuple, Iterable


class MultimeterMode(Enum):
    """
    Different types of measurements that can be taken.
    """
    VoltageDC = 1,
    VoltageAC = 2,
    CurrentDC = 3,
    CurrentAC = 4,
    Resistance = 5,
    ResistanceFourWire = 6


MultimeterCapability = NamedTuple('MultimeterCapabilities', [])
"""Classify the capabilities of the multimeter that apply to all channels"""
MultimeterChannelCapability = NamedTuple('MultimeterChannelCapabilities', [('digits', float),
                                                                             ('max_current', float),
                                                                             ('max_voltage', float),
                                                                             ('min_voltage', float),
                                                                             ('modes', Iterable[MultimeterMode])])


class Multimeter(Protocol):
    """
    A protocol representing the interface to a digital multimeter.
    """
    @abstractmethod
    def measure(self, channel: int, mode: MultimeterMode) -> float:
        """
        Measures `channel` returning the measurement taken.

        :param channel: The channel to take the measurement on.
        :param mode: The measurement mode to use when taking the measurement.
        :return: mV/mA/mOhms measurement taken.
        """
        raise NotImplementedError()
