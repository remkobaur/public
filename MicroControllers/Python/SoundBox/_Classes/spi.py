#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Compatibility shim for legacy `spi` API used in this project.

Provides openSPI/transfer/closeSPI on top of `spidev`.
"""

import re

try:
    import spidev
except ImportError as err:
    raise ImportError(
        "spidev is required for RFID/NFC SPI access. Install with: "
        "sudo apt install -y python3-spidev"
    ) from err

_spi_dev = None


def _parse_device(device):
    match = re.match(r"^/dev/spidev(\d+)\.(\d+)$", device)
    if not match:
        raise ValueError("Invalid SPI device path: %s" % device)
    return int(match.group(1)), int(match.group(2))


def openSPI(device="/dev/spidev0.0", speed=1000000):
    global _spi_dev
    bus, chip_select = _parse_device(device)
    _spi_dev = spidev.SpiDev()
    _spi_dev.open(bus, chip_select)
    _spi_dev.max_speed_hz = int(speed)
    _spi_dev.mode = 0


def transfer(data):
    if _spi_dev is None:
        raise RuntimeError("SPI not initialized. Call openSPI() first.")
    return _spi_dev.xfer2(list(data))


def closeSPI():
    global _spi_dev
    if _spi_dev is not None:
        _spi_dev.close()
        _spi_dev = None
