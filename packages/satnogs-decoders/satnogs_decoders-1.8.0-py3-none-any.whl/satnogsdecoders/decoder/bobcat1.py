# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Bobcat1(KaitaiStruct):
    """:field callsign: frame.basic.callsign
    :field bobcat1: frame.basic.bobcat1
    :field bat_v: frame.basic.bat_v
    :field bat_i_out: frame.basic.bat_i_out
    :field bat_i_in: frame.basic.bat_i_in
    :field bootcount_a3200: frame.basic.bootcount_a3200
    :field resetcause_a3200: frame.basic.resetcause_a3200
    :field bootcause_a3200: frame.basic.bootcause_a3200
    :field uptime_a3200: frame.basic.uptime_a3200
    :field bootcount_ax100: frame.basic.bootcount_ax100
    :field bootcause_ax100: frame.basic.bootcause_ax100
    :field i_pwm: frame.basic.i_pwm
    :field fs_mounted: frame.basic.fs_mounted
    :field antennas_deployed: frame.basic.antennas_deployed
    :field deploy_attempts1: frame.basic.deploy_attempts1
    :field deploy_attempts2: frame.basic.deploy_attempts2
    :field deploy_attempts3: frame.basic.deploy_attempts3
    :field deploy_attempts4: frame.basic.deploy_attempts4
    :field gyro_x: frame.basic.gyro_x
    :field gyro_y: frame.basic.gyro_y
    :field gyro_z: frame.basic.gyro_z
    :field timestamp: frame.basic.timestamp
    :field protocol_version: frame.hk_header.protocol_version
    :field type: frame.hk_header.type
    :field version: frame.hk_header.version
    :field satid: frame.hk_header.satid
    :field checksum: frame.hk_data.a3200_hktable0.checksum
    :field hk_data_a3200_hktable0_timestamp: frame.hk_data.a3200_hktable0.timestamp
    :field source: frame.hk_data.a3200_hktable0.source
    :field hk_data_callsign: frame.hk_data.callsign
    :field hk_data_bobcat1: frame.hk_data.bobcat1
    :field hk_data_bat_v: frame.hk_data.bat_v
    :field hk_data_bat_i_in: frame.hk_data.bat_i_in
    :field hk_data_bat_i_out: frame.hk_data.bat_i_out
    :field solar1_i: frame.hk_data.solar1_i
    :field solar1_v: frame.hk_data.solar1_v
    :field solar2_i: frame.hk_data.solar2_i
    :field solar2_v: frame.hk_data.solar2_v
    :field solar3_i: frame.hk_data.solar3_i
    :field solar3_v: frame.hk_data.solar3_v
    :field novatel_i: frame.hk_data.novatel_i
    :field sdr_i: frame.hk_data.sdr_i
    :field bootcount_p31: frame.hk_data.bootcount_p31
    :field bootcause_p31: frame.hk_data.bootcause_p31
    :field hk_data_bootcount_a3200: frame.hk_data.bootcount_a3200
    :field hk_data_bootcause_a3200: frame.hk_data.bootcause_a3200
    :field hk_data_resetcause_a3200: frame.hk_data.resetcause_a3200
    :field hk_data_uptime_a3200: frame.hk_data.uptime_a3200
    :field temp_mcu: frame.hk_data.temp_mcu
    :field i_gssb1: frame.hk_data.i_gssb1
    :field hk_data_i_pwm: frame.hk_data.i_pwm
    :field panel_temp1: frame.hk_data.panel_temp1
    :field panel_temp2: frame.hk_data.panel_temp2
    :field panel_temp3: frame.hk_data.panel_temp3
    :field panel_temp4: frame.hk_data.panel_temp4
    :field panel_temp5: frame.hk_data.panel_temp5
    :field panel_temp6: frame.hk_data.panel_temp6
    :field panel_temp7: frame.hk_data.panel_temp7
    :field panel_temp8: frame.hk_data.panel_temp8
    :field panel_temp9: frame.hk_data.panel_temp9
    :field p31_temp1: frame.hk_data.p31_temp1
    :field p31_temp2: frame.hk_data.p31_temp2
    :field p31_temp3: frame.hk_data.p31_temp3
    :field p31_temp4: frame.hk_data.p31_temp4
    :field p31_temp5: frame.hk_data.p31_temp5
    :field p31_temp6: frame.hk_data.p31_temp6
    :field flash0_free: frame.hk_data.flash0_free
    :field flash1_free: frame.hk_data.flash1_free
    :field coll_running: frame.hk_data.coll_running
    :field ax100_telemtable_checksum: frame.hk_data.ax100_telemtable.checksum
    :field hk_data_ax100_telemtable_timestamp: frame.hk_data.ax100_telemtable.timestamp
    :field ax100_telemtable_source: frame.hk_data.ax100_telemtable.source
    :field temp_brd: frame.hk_data.temp_brd
    :field temp_pa: frame.hk_data.temp_pa
    :field bgnd_rssi: frame.hk_data.bgnd_rssi
    :field tot_tx_count: frame.hk_data.tot_tx_count
    :field tot_rx_count: frame.hk_data.tot_rx_count
    :field tot_tx_bytes: frame.hk_data.tot_tx_bytes
    :field tot_rx_bytes: frame.hk_data.tot_rx_bytes
    :field hk_data_bootcount_ax100: frame.hk_data.bootcount_ax100
    :field hk_data_bootcause_ax100: frame.hk_data.bootcause_ax100
    :field data: frame.cspheader.data
    :field data_callsign: frame.data.basic.callsign
    :field data_bobcat1: frame.data.basic.bobcat1
    :field data_bat_v: frame.data.basic.bat_v
    :field data_bat_i_out: frame.data.basic.bat_i_out
    :field data_bat_i_in: frame.data.basic.bat_i_in
    :field data_bootcount_a3200: frame.data.basic.bootcount_a3200
    :field data_resetcause_a3200: frame.data.basic.resetcause_a3200
    :field data_bootcause_a3200: frame.data.basic.bootcause_a3200
    :field data_uptime_a3200: frame.data.basic.uptime_a3200
    :field data_bootcount_ax100: frame.data.basic.bootcount_ax100
    :field data_bootcause_ax100: frame.data.basic.bootcause_ax100
    :field data_i_pwm: frame.data.basic.i_pwm
    :field data_fs_mounted: frame.data.basic.fs_mounted
    :field data_antennas_deployed: frame.data.basic.antennas_deployed
    :field data_deploy_attempts1: frame.data.basic.deploy_attempts1
    :field data_deploy_attempts2: frame.data.basic.deploy_attempts2
    :field data_deploy_attempts3: frame.data.basic.deploy_attempts3
    :field data_deploy_attempts4: frame.data.basic.deploy_attempts4
    :field data_gyro_x: frame.data.basic.gyro_x
    :field data_gyro_y: frame.data.basic.gyro_y
    :field data_gyro_z: frame.data.basic.gyro_z
    :field data_timestamp: frame.data.basic.timestamp
    :field hk_frame_protocol_version: frame.hk_frame.hk_header.protocol_version
    :field hk_frame_type: frame.hk_frame.hk_header.type
    :field hk_frame_version: frame.hk_frame.hk_header.version
    :field hk_frame_satid: frame.hk_frame.hk_header.satid
    :field hk_frame_checksum: frame.hk_frame.hk_data.a3200_hktable0.checksum
    :field hk_frame_hk_data_a3200_hktable0_timestamp: frame.hk_frame.hk_data.a3200_hktable0.timestamp
    :field hk_frame_source: frame.hk_frame.hk_data.a3200_hktable0.source
    :field hk_frame_hk_data_callsign: frame.hk_frame.hk_data.callsign
    :field hk_frame_hk_data_bobcat1: frame.hk_frame.hk_data.bobcat1
    :field hk_frame_hk_data_bat_v: frame.hk_frame.hk_data.bat_v
    :field hk_frame_hk_data_bat_i_in: frame.hk_frame.hk_data.bat_i_in
    :field hk_frame_hk_data_bat_i_out: frame.hk_frame.hk_data.bat_i_out
    :field hk_frame_solar1_i: frame.hk_frame.hk_data.solar1_i
    :field hk_frame_solar1_v: frame.hk_frame.hk_data.solar1_v
    :field hk_frame_solar2_i: frame.hk_frame.hk_data.solar2_i
    :field hk_frame_solar2_v: frame.hk_frame.hk_data.solar2_v
    :field hk_frame_solar3_i: frame.hk_frame.hk_data.solar3_i
    :field hk_frame_solar3_v: frame.hk_frame.hk_data.solar3_v
    :field hk_frame_novatel_i: frame.hk_frame.hk_data.novatel_i
    :field hk_frame_sdr_i: frame.hk_frame.hk_data.sdr_i
    :field hk_frame_bootcount_p31: frame.hk_frame.hk_data.bootcount_p31
    :field hk_frame_bootcause_p31: frame.hk_frame.hk_data.bootcause_p31
    :field hk_frame_hk_data_bootcount_a3200: frame.hk_frame.hk_data.bootcount_a3200
    :field hk_frame_hk_data_bootcause_a3200: frame.hk_frame.hk_data.bootcause_a3200
    :field hk_frame_hk_data_resetcause_a3200: frame.hk_frame.hk_data.resetcause_a3200
    :field hk_frame_hk_data_uptime_a3200: frame.hk_frame.hk_data.uptime_a3200
    :field hk_frame_temp_mcu: frame.hk_frame.hk_data.temp_mcu
    :field hk_frame_i_gssb1: frame.hk_frame.hk_data.i_gssb1
    :field hk_frame_hk_data_i_pwm: frame.hk_frame.hk_data.i_pwm
    :field hk_frame_panel_temp1: frame.hk_frame.hk_data.panel_temp1
    :field hk_frame_panel_temp2: frame.hk_frame.hk_data.panel_temp2
    :field hk_frame_panel_temp3: frame.hk_frame.hk_data.panel_temp3
    :field hk_frame_panel_temp4: frame.hk_frame.hk_data.panel_temp4
    :field hk_frame_panel_temp5: frame.hk_frame.hk_data.panel_temp5
    :field hk_frame_panel_temp6: frame.hk_frame.hk_data.panel_temp6
    :field hk_frame_panel_temp7: frame.hk_frame.hk_data.panel_temp7
    :field hk_frame_panel_temp8: frame.hk_frame.hk_data.panel_temp8
    :field hk_frame_panel_temp9: frame.hk_frame.hk_data.panel_temp9
    :field hk_frame_p31_temp1: frame.hk_frame.hk_data.p31_temp1
    :field hk_frame_p31_temp2: frame.hk_frame.hk_data.p31_temp2
    :field hk_frame_p31_temp3: frame.hk_frame.hk_data.p31_temp3
    :field hk_frame_p31_temp4: frame.hk_frame.hk_data.p31_temp4
    :field hk_frame_p31_temp5: frame.hk_frame.hk_data.p31_temp5
    :field hk_frame_p31_temp6: frame.hk_frame.hk_data.p31_temp6
    :field hk_frame_flash0_free: frame.hk_frame.hk_data.flash0_free
    :field hk_frame_flash1_free: frame.hk_frame.hk_data.flash1_free
    :field hk_frame_coll_running: frame.hk_frame.hk_data.coll_running
    :field hk_frame_ax100_telemtable_checksum: frame.hk_frame.hk_data.ax100_telemtable.checksum
    :field hk_frame_hk_data_ax100_telemtable_timestamp: frame.hk_frame.hk_data.ax100_telemtable.timestamp
    :field hk_frame_ax100_telemtable_source: frame.hk_frame.hk_data.ax100_telemtable.source
    :field hk_frame_temp_brd: frame.hk_frame.hk_data.temp_brd
    :field hk_frame_temp_pa: frame.hk_frame.hk_data.temp_pa
    :field hk_frame_bgnd_rssi: frame.hk_frame.hk_data.bgnd_rssi
    :field hk_frame_tot_tx_count: frame.hk_frame.hk_data.tot_tx_count
    :field hk_frame_tot_rx_count: frame.hk_frame.hk_data.tot_rx_count
    :field hk_frame_tot_tx_bytes: frame.hk_frame.hk_data.tot_tx_bytes
    :field hk_frame_tot_rx_bytes: frame.hk_frame.hk_data.tot_rx_bytes
    :field hk_frame_hk_data_bootcount_ax100: frame.hk_frame.hk_data.bootcount_ax100
    :field hk_frame_hk_data_bootcause_ax100: frame.hk_frame.hk_data.bootcause_ax100
    :field framelength: framelength
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        _on = self._root.framelength
        if _on == 57:
            self.frame = self._root.Bc1BasicFrame(self._io, self, self._root)
        elif _on == 144:
            self.frame = self._root.Bc1HkFrame(self._io, self, self._root)
        elif _on == 69:
            self.frame = self._root.Bc1BasicFrameCsp(self._io, self, self._root)
        elif _on == 156:
            self.frame = self._root.Bc1HkFrameCsp(self._io, self, self._root)

    class BeaconElementHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.checksum = self._io.read_u2be()
            self.timestamp = self._io.read_u4be()
            self.source = self._io.read_u2be()


    class Cspheader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_u4be()


    class Bc1HkFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hk_header = self._root.HkHeader(self._io, self, self._root)
            self.hk_data = self._root.HkData(self._io, self, self._root)


    class Bc1HkFrameCsp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cspheader = self._root.Cspheader(self._io, self, self._root)
            self.hk_frame = self._root.Bc1HkFrame(self._io, self, self._root)


    class HkData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.a3200_hktable0 = self._root.BeaconElementHeader(self._io, self, self._root)
            self.callsign = (KaitaiStream.bytes_terminate(self._io.read_bytes(6), 0, False)).decode(u"ASCII")
            self.bobcat1 = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.bat_v = self._io.read_u2be()
            self.bat_i_in = self._io.read_u2be()
            self.bat_i_out = self._io.read_u2be()
            self.solar1_i = self._io.read_u2be()
            self.solar1_v = self._io.read_u2be()
            self.solar2_i = self._io.read_u2be()
            self.solar2_v = self._io.read_u2be()
            self.solar3_i = self._io.read_u2be()
            self.solar3_v = self._io.read_u2be()
            self.novatel_i = self._io.read_u2be()
            self.sdr_i = self._io.read_u2be()
            self.bootcount_p31 = self._io.read_u4be()
            self.bootcause_p31 = self._io.read_u1()
            self.bootcount_a3200 = self._io.read_u2be()
            self.bootcause_a3200 = self._io.read_u1()
            self.resetcause_a3200 = self._io.read_u1()
            self.uptime_a3200 = self._io.read_u4be()
            self.temp_mcu = self._io.read_s2be()
            self.i_gssb1 = self._io.read_u2be()
            self.i_pwm = self._io.read_u2be()
            self.panel_temp1 = self._io.read_s2be()
            self.panel_temp2 = self._io.read_s2be()
            self.panel_temp3 = self._io.read_s2be()
            self.panel_temp4 = self._io.read_s2be()
            self.panel_temp5 = self._io.read_s2be()
            self.panel_temp6 = self._io.read_s2be()
            self.panel_temp7 = self._io.read_s2be()
            self.panel_temp8 = self._io.read_s2be()
            self.panel_temp9 = self._io.read_s2be()
            self.p31_temp1 = self._io.read_s2be()
            self.p31_temp2 = self._io.read_s2be()
            self.p31_temp3 = self._io.read_s2be()
            self.p31_temp4 = self._io.read_s2be()
            self.p31_temp5 = self._io.read_s2be()
            self.p31_temp6 = self._io.read_s2be()
            self.flash0_free = self._io.read_u4be()
            self.flash1_free = self._io.read_u4be()
            self.coll_running = self._io.read_u1()
            self.ax100_telemtable = self._root.BeaconElementHeader(self._io, self, self._root)
            self.temp_brd = self._io.read_s2be()
            self.temp_pa = self._io.read_s2be()
            self.bgnd_rssi = self._io.read_s2be()
            self.tot_tx_count = self._io.read_u4be()
            self.tot_rx_count = self._io.read_u4be()
            self.tot_tx_bytes = self._io.read_u4be()
            self.tot_rx_bytes = self._io.read_u4be()
            self.bootcount_ax100 = self._io.read_u2be()
            self.bootcause_ax100 = self._io.read_u4be()


    class HkHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.protocol_version = self._io.read_u1()
            self.type = self._io.read_u1()
            self.version = self._io.read_u1()
            self.satid = self._io.read_u2be()


    class Basic(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (KaitaiStream.bytes_terminate(self._io.read_bytes(6), 0, False)).decode(u"ASCII")
            self.bobcat1 = (KaitaiStream.bytes_terminate(self._io.read_bytes(9), 0, False)).decode(u"ASCII")
            self.bat_v = self._io.read_u2be()
            self.bat_i_out = self._io.read_u2be()
            self.bat_i_in = self._io.read_u2be()
            self.bootcount_a3200 = self._io.read_u2be()
            self.resetcause_a3200 = self._io.read_u1()
            self.bootcause_a3200 = self._io.read_u1()
            self.uptime_a3200 = self._io.read_u4be()
            self.bootcount_ax100 = self._io.read_u2be()
            self.bootcause_ax100 = self._io.read_u4be()
            self.i_pwm = self._io.read_u2be()
            self.fs_mounted = self._io.read_u1()
            self.antennas_deployed = self._io.read_u1()
            self.deploy_attempts1 = self._io.read_u2be()
            self.deploy_attempts2 = self._io.read_u2be()
            self.deploy_attempts3 = self._io.read_u2be()
            self.deploy_attempts4 = self._io.read_u2be()
            self.gyro_x = self._io.read_s2be()
            self.gyro_y = self._io.read_s2be()
            self.gyro_z = self._io.read_s2be()
            self.timestamp = self._io.read_u4be()


    class Bc1BasicFrameCsp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cspheader = self._root.Cspheader(self._io, self, self._root)
            self.data = self._root.Bc1BasicFrame(self._io, self, self._root)


    class Bc1BasicFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.basic = self._root.Basic(self._io, self, self._root)


    @property
    def framelength(self):
        if hasattr(self, '_m_framelength'):
            return self._m_framelength if hasattr(self, '_m_framelength') else None

        self._m_framelength = self._io.size()
        return self._m_framelength if hasattr(self, '_m_framelength') else None


