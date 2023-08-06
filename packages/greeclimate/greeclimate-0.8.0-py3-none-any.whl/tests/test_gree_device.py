import enum
import socket
import unittest

from greeclimate.discovery import Discovery
from greeclimate.device import Device, DeviceInfo
from greeclimate.exceptions import DeviceNotBoundError, DeviceTimeoutError
from greeclimate.network_helper import Props
from unittest.mock import patch

class FakeProps(enum.Enum):
    FAKE = "fake"

class GreeDeviceTestCase(unittest.IsolatedAsyncioTestCase):
    @patch("greeclimate.network_helper.search_devices")
    @patch("greeclimate.network_helper.bind_device")
    async def test_get_device_info(self, mock_bind, mock_search):
        # DeviceInfo("192.168.1.29", 7000, "f4911e7aca59", "1e7aca59")

        mock_info = ("1.1.1.0", "7000", "aabbcc001122", "MockDevice1", "MockBrand", "MockModel", "0.0.1-fake")
        mock_search.return_value = [mock_info]
        mock_bind.return_value = "St8Vw1Yz4Bc7Ef0H"

        """ The only way to get the key through binding is by scanning first
        """
        devices = await Discovery.search_devices()
        device = Device(devices[0])
        await device.bind()

        self.assertIsNotNone(devices)
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].ip, mock_info[0])
        self.assertEqual(devices[0].port, mock_info[1])
        self.assertEqual(devices[0].mac, mock_info[2])
        self.assertEqual(devices[0].name, mock_info[3])
        self.assertEqual(devices[0].brand, mock_info[4])
        self.assertEqual(devices[0].model, mock_info[5])
        self.assertEqual(devices[0].version, mock_info[6])

        self.assertIsNotNone(device)
        self.assertEqual(device.device_key, "St8Vw1Yz4Bc7Ef0H")

    @patch("greeclimate.network_helper.search_devices")
    @patch("greeclimate.network_helper.bind_device")
    async def test_get_device_key_timeout(self, mock_bind, mock_search):

        mock_search.return_value = [
            ("1.1.1.0", "7000", "aabbcc001122", "MockDevice1")
        ]
        mock_bind.side_effect = socket.timeout

        """ The only way to get the key through binding is by scanning first
        """
        devices = await Discovery.search_devices()
        device = Device(devices[0])

        with self.assertRaises(DeviceNotBoundError):
            await device.bind()

        self.assertIsNotNone(device)
        self.assertIsNone(device.device_key)


class GreeDeviceStateTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._device = Device(
            ("192.168.1.29", 7000, "f4911e7aca59", "1e7aca59")
        )
        await self._device.bind(key="St8Vw1Yz4Bc7Ef0H")

    def getMockState(self):
        return {
            "Pow": 1,
            "Mod": 3,
            "SetTem": 25,
            "TemUn": 0,
            "WdSpd": 0,
            "Air": 0,
            "Blo": 0,
            "Health": 0,
            "SwhSlp": 0,
            "Lig": 1,
            "SwingLfRig": 1,
            "SwUpDn": 1,
            "Quiet": 0,
            "Tur": 0,
            "StHt": 0,
            "SvSt": 0,
            "TemRec": 0,
            "HeatCoolType": 0,
        }

    def getMockStateOff(self):
        return {
            "Pow": 0,
            "Mod": 0,
            "SetTem": 0,
            "TemUn": 0,
            "WdSpd": 0,
            "Air": 0,
            "Blo": 0,
            "Health": 0,
            "SwhSlp": 0,
            "Lig": 0,
            "SwingLfRig": 0,
            "SwUpDn": 0,
            "Quiet": 0,
            "Tur": 0,
            "StHt": 0,
            "SvSt": 0,
            "TemRec": 0,
            "HeatCoolType": 0,
        }

    def getMockStateOn(self):
        return {
            "Pow": 1,
            "Mod": 1,
            "SetTem": 1,
            "TemUn": 1,
            "WdSpd": 1,
            "Air": 1,
            "Blo": 1,
            "Health": 1,
            "SwhSlp": 1,
            "Lig": 1,
            "SwingLfRig": 1,
            "SwUpDn": 1,
            "Quiet": 1,
            "Tur": 1,
            "StHt": 1,
            "SvSt": 1,
            "TemRec": 0,
            "HeatCoolType": 0,
        }

    @patch("greeclimate.network_helper.request_state")
    async def test_update_properties(self, mock_request):
        mock_request.return_value = self.getMockState()

        for p in Props:
            self.assertIsNone(self._device.get_property(p))

        await self._device.update_state()

        for p in Props:
            self.assertIsNotNone(
                self._device.get_property(p), f"Property {p} was unexpectedly None"
            )
            self.assertEqual(self._device.get_property(p), self.getMockState()[p.value])

    @patch("greeclimate.network_helper.request_state", side_effect=socket.timeout)
    async def test_update_properties_timeout(self, mock_request):
        mock_request.return_value = self.getMockState()

        for p in Props:
            self.assertIsNone(self._device.get_property(p))

        with self.assertRaises(DeviceTimeoutError):
            await self._device.update_state()

    @patch("greeclimate.network_helper.send_state")
    async def test_set_properties(self, mock_request):

        for p in Props:
            self.assertIsNone(self._device.get_property(p))

        self._device.power = True
        self._device.mode = 1
        self._device.target_temperature = 1
        self._device.temperature_units = 1
        self._device.fan_speed = 1
        self._device.fresh_air = True
        self._device.xfan = True
        self._device.anion = True
        self._device.sleep = True
        self._device.light = True
        self._device.horizontal_swing = 1
        self._device.vertical_swing = 1
        self._device.quiet = True
        self._device.turbo = True
        self._device.steady_heat = True
        self._device.power_save = True

        await self._device.push_state_update()

        mock_request.assert_called_once()

        for p in Props:
            if p not in (Props.TEMP_BIT, Props.UNKNOWN_HEATCOOLTYPE):
                self.assertIsNotNone(
                    self._device.get_property(p), f"Property {p} was unexpectedly None"
                )
                self.assertEqual(
                    self._device.get_property(p), self.getMockStateOn()[p.value]
                )

    @patch("greeclimate.network_helper.send_state", side_effect=socket.timeout)
    async def test_set_properties_timeout(self, mock_request):

        for p in Props:
            self.assertIsNone(self._device.get_property(p))

        self._device.power = True
        self._device.mode = 1
        self._device.target_temperature = 1
        self._device.temperature_units = 1
        self._device.fan_speed = 1
        self._device.fresh_air = True
        self._device.xfan = True
        self._device.anion = True
        self._device.sleep = True
        self._device.light = True
        self._device.horizontal_swing = 1
        self._device.vertical_swing = 1
        self._device.quiet = True
        self._device.turbo = True
        self._device.steady_heat = True
        self._device.power_save = True

        with self.assertRaises(DeviceTimeoutError):
            await self._device.push_state_update()


    async def test_uninitialized_properties(self):

        for p in Props:
            self.assertIsNone(self._device.get_property(p))

        self.assertFalse(self._device.power)
        self.assertIsNone(self._device.mode)
        self.assertIsNone(self._device.target_temperature)
        self.assertIsNone(self._device.temperature_units)
        self.assertIsNone(self._device.fan_speed)
        self.assertFalse(self._device.fresh_air)
        self.assertFalse(self._device.xfan)
        self.assertFalse(self._device.anion)
        self.assertFalse(self._device.sleep)
        self.assertFalse(self._device.light)
        self.assertIsNone(self._device.horizontal_swing)
        self.assertIsNone(self._device.vertical_swing)
        self.assertFalse(self._device.quiet)
        self.assertFalse(self._device.turbo)
        self.assertFalse(self._device.steady_heat)
        self.assertFalse(self._device.power_save)


