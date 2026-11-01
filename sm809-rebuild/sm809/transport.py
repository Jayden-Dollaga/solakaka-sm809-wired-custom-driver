"""HID transport implemented with ctypes (SetupAPI + HID.DLL).

Matches MSDriver.dll's behaviour:
  * control interface  UsagePage 0xFF00 / Usage 0xFF00
  * monitor interface  UsagePage 0xFF01 / Usage 0xFF01
  * feature reports are 9 bytes: report ID 0 + 8-byte packet
  * bulk blocks are 33 bytes: report ID 0 + 32-byte payload
  * input reports start with report ID 6: [6, eventHi, eventLo, value]
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import sys
import threading
import time
from dataclasses import dataclass
from typing import Callable

IS_WINDOWS = sys.platform == "win32"


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_uint32),
        ("Data2", ctypes.c_uint16),
        ("Data3", ctypes.c_uint16),
        ("Data4", ctypes.c_ubyte * 8),
    ]


GUID_DEVINTERFACE_HID = GUID(
    0x4D1E55B2, 0xF16F, 0x11CF,
    (0x88, 0xCB, 0x00, 0x11, 0x11, 0x00, 0x00, 0x30),
)

DIGCF_PRESENT = 0x02
DIGCF_DEVICEINTERFACE = 0x10
OPEN_EXISTING = 3
FILE_FLAG_OVERLAPPED = 0x40000000
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
ERROR_IO_PENDING = 997
WAIT_OBJECT_0 = 0
WAIT_TIMEOUT = 258


class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wt.DWORD),
        ("InterfaceClassGuid", GUID),
        ("Flags", wt.DWORD),
        ("Reserved", ctypes.c_void_p),
    ]


class SP_DEVICE_INTERFACE_DETAIL_DATA_W(ctypes.Structure):
    _fields_ = [
        ("cbSize", wt.DWORD),
        ("DevicePath", ctypes.c_wchar * 1),
    ]


class HIDD_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Size", wt.ULONG),
        ("VendorID", wt.USHORT),
        ("ProductID", wt.USHORT),
        ("VersionNumber", wt.USHORT),
    ]


class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", ctypes.c_void_p),
        ("InternalHigh", ctypes.c_void_p),
        ("Offset", wt.DWORD),
        ("OffsetHigh", wt.DWORD),
        ("hEvent", wt.HANDLE),
    ]


@dataclass
class HidInterface:
    path: str
    vendor_id: int
    product_id: int
    usage_page: int
    usage: int
    input_length: int
    output_length: int
    feature_length: int
    product: str = ""


class HidLibrary:
    def __init__(self) -> None:
        if not IS_WINDOWS:
            raise OSError("HID transport requires Windows")
        self.setupapi = ctypes.windll.setupapi
        self.hid = ctypes.windll.hid
        self.kernel32 = ctypes.windll.kernel32
        self._configure()

    def _configure(self) -> None:
        k = self.kernel32
        k.CreateFileW.restype = wt.HANDLE
        k.CreateFileW.argtypes = [
            wt.LPCWSTR, wt.DWORD, wt.DWORD, ctypes.c_void_p, wt.DWORD, wt.DWORD, wt.HANDLE,
        ]
        k.CloseHandle.argtypes = [wt.HANDLE]
        k.WriteFile.argtypes = [
            wt.HANDLE, ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD), ctypes.c_void_p,
        ]
        k.ReadFile.argtypes = [
            wt.HANDLE, ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD), ctypes.POINTER(OVERLAPPED),
        ]
        k.CreateEventW.restype = wt.HANDLE
        k.CreateEventW.argtypes = [ctypes.c_void_p, wt.BOOL, wt.BOOL, wt.LPCWSTR]
        k.WaitForSingleObject.argtypes = [wt.HANDLE, wt.DWORD]
        k.GetOverlappedResult.argtypes = [
            wt.HANDLE, ctypes.POINTER(OVERLAPPED), ctypes.POINTER(wt.DWORD), wt.BOOL,
        ]
        k.CancelIoEx.argtypes = [wt.HANDLE, ctypes.POINTER(OVERLAPPED)]
        k.SetLastError(0)

        self.hid.HidD_GetAttributes.argtypes = [wt.HANDLE, ctypes.POINTER(HIDD_ATTRIBUTES)]
        self.hid.HidD_GetPreparsedData.argtypes = [wt.HANDLE, ctypes.POINTER(ctypes.c_void_p)]
        self.hid.HidD_FreePreparsedData.argtypes = [ctypes.c_void_p]
        self.hid.HidP_GetCaps.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.hid.HidD_SetFeature.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.ULONG]
        self.hid.HidD_GetFeature.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.ULONG]
        self.hid.HidD_GetProductString.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.ULONG]

        self.setupapi.SetupDiGetClassDevsW.restype = wt.HANDLE
        self.setupapi.SetupDiGetClassDevsW.argtypes = [
            ctypes.POINTER(GUID), wt.LPCWSTR, wt.HWND, wt.DWORD,
        ]
        self.setupapi.SetupDiEnumDeviceInterfaces.argtypes = [
            wt.HANDLE, ctypes.c_void_p, ctypes.POINTER(GUID), wt.DWORD,
            ctypes.POINTER(SP_DEVICE_INTERFACE_DATA),
        ]
        self.setupapi.SetupDiGetDeviceInterfaceDetailW.argtypes = [
            wt.HANDLE, ctypes.POINTER(SP_DEVICE_INTERFACE_DATA), ctypes.c_void_p, wt.DWORD,
            ctypes.POINTER(wt.DWORD), ctypes.c_void_p,
        ]
        self.setupapi.SetupDiDestroyDeviceInfoList.argtypes = [wt.HANDLE]

    # -- enumeration -------------------------------------------------------
    def enumerate(self) -> list[HidInterface]:
        out: list[HidInterface] = []
        info = self.setupapi.SetupDiGetClassDevsW(
            ctypes.byref(GUID_DEVINTERFACE_HID), None, None,
            DIGCF_PRESENT | DIGCF_DEVICEINTERFACE,
        )
        if info == INVALID_HANDLE_VALUE or not info:
            return out
        try:
            index = 0
            while True:
                iface = SP_DEVICE_INTERFACE_DATA()
                iface.cbSize = ctypes.sizeof(SP_DEVICE_INTERFACE_DATA)
                if not self.setupapi.SetupDiEnumDeviceInterfaces(
                    info, None, ctypes.byref(GUID_DEVINTERFACE_HID), index, ctypes.byref(iface)
                ):
                    break
                index += 1
                required = wt.DWORD(0)
                self.setupapi.SetupDiGetDeviceInterfaceDetailW(
                    info, ctypes.byref(iface), None, 0, ctypes.byref(required), None
                )
                if required.value <= 0:
                    continue
                buf = (ctypes.c_ubyte * required.value)()
                detail = ctypes.cast(buf, ctypes.POINTER(SP_DEVICE_INTERFACE_DETAIL_DATA_W))
                detail.contents.cbSize = ctypes.sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA_W)
                if not self.setupapi.SetupDiGetDeviceInterfaceDetailW(
                    info, ctypes.byref(iface), buf, required.value, ctypes.byref(required), None
                ):
                    continue
                # DevicePath starts at offset 4 (after the DWORD cbSize); the
                # declared c_wchar[1] field would only read the first "\" of
                # "\\?\hid#...", so read the whole wide string from the buffer.
                path = ctypes.wstring_at(ctypes.addressof(buf) + 4)
                entry = self._describe(path)
                if entry:
                    out.append(entry)
        finally:
            self.setupapi.SetupDiDestroyDeviceInfoList(info)
        return out

    def _describe(self, path: str) -> HidInterface | None:
        handle = self.kernel32.CreateFileW(
            path, 0, 3, None, OPEN_EXISTING, 0, None
        )
        if handle == INVALID_HANDLE_VALUE or not handle:
            return None
        try:
            attrs = HIDD_ATTRIBUTES()
            attrs.Size = ctypes.sizeof(HIDD_ATTRIBUTES)
            if not self.hid.HidD_GetAttributes(handle, ctypes.byref(attrs)):
                return None
            pp = ctypes.c_void_p()
            if not self.hid.HidD_GetPreparsedData(handle, ctypes.byref(pp)):
                return None
            try:
                caps = (ctypes.c_ubyte * 256)()
                if self.hid.HidP_GetCaps(pp, caps) < 0:
                    return None
                import struct
                usage, usage_page, inp, outp, feat = struct.unpack_from("<HHHHH", bytes(caps), 0)
            finally:
                self.hid.HidD_FreePreparsedData(pp)
            product = ""
            try:
                pbuf = ctypes.create_unicode_buffer(256)
                if self.hid.HidD_GetProductString(handle, pbuf, ctypes.sizeof(pbuf)):
                    product = pbuf.value
            except Exception:
                pass
            return HidInterface(
                path=path,
                vendor_id=attrs.VendorID,
                product_id=attrs.ProductID,
                usage_page=usage_page,
                usage=usage,
                input_length=inp,
                output_length=outp,
                feature_length=feat,
                product=product,
            )
        finally:
            self.kernel32.CloseHandle(handle)

    def find(self, vid: int, pid: int, usage_page: int, usage: int) -> HidInterface | None:
        for entry in self.enumerate():
            if entry.vendor_id == vid and entry.product_id == pid:
                if entry.usage_page == usage_page and entry.usage == usage:
                    return entry
        return None

    def find_control(self, vid: int, pid: int) -> HidInterface | None:
        entry = self.find(vid, pid, 0xFF00, 0xFF00)
        if entry:
            return entry
        candidates = [e for e in self.enumerate() if e.vendor_id == vid and e.product_id == pid]
        for entry in candidates:
            if entry.output_length >= 33 or entry.feature_length >= 9:
                return entry
        return None

    def find_monitor(self, vid: int, pid: int) -> HidInterface | None:
        return self.find(vid, pid, 0xFF01, 0xFF01)

    # -- handles -----------------------------------------------------------
    def open(self, path: str, *, read: bool = True, write: bool = True,
             overlapped: bool = False) -> int:
        access = (GENERIC_READ if read else 0) | (GENERIC_WRITE if write else 0)
        flags = FILE_FLAG_OVERLAPPED if overlapped else 0
        handle = self.kernel32.CreateFileW(path, access, 3, None, OPEN_EXISTING, flags, None)
        if handle == INVALID_HANDLE_VALUE or not handle:
            raise OSError(f"cannot open HID device: {path}")
        return handle

    def close(self, handle: int) -> None:
        if handle:
            self.kernel32.CloseHandle(handle)

    def set_feature(self, handle: int, packet: bytes) -> bool:
        if len(packet) != 8:
            raise ValueError("feature packet must be 8 bytes")
        buf = (ctypes.c_ubyte * 9)()
        buf[0] = 0
        for i, b in enumerate(packet):
            buf[i + 1] = b
        return bool(self.hid.HidD_SetFeature(handle, buf, 9))

    def get_feature(self, handle: int) -> bytes:
        buf = (ctypes.c_ubyte * 9)()
        buf[0] = 0
        if not self.hid.HidD_GetFeature(handle, buf, 9):
            return b""
        return bytes(buf[1:9])

    def write_block(self, handle: int, block: bytes) -> bool:
        if len(block) != 32:
            raise ValueError("block must be 32 bytes")
        data = (ctypes.c_ubyte * 33)()
        data[0] = 0
        for i, b in enumerate(block):
            data[i + 1] = b
        written = wt.DWORD(0)
        ok = self.kernel32.WriteFile(handle, data, 33, ctypes.byref(written), None)
        return bool(ok) and written.value >= 32

    def read_input_once(self, handle: int, timeout_ms: int = 500) -> bytes | None:
        buf = (ctypes.c_ubyte * 128)()
        ov = OVERLAPPED()
        event = self.kernel32.CreateEventW(None, True, False, None)
        if not event:
            return None
        ov.hEvent = event
        try:
            read = wt.DWORD(0)
            ok = self.kernel32.ReadFile(handle, buf, 128, ctypes.byref(read), ctypes.byref(ov))
            if not ok and ctypes.get_last_error() != ERROR_IO_PENDING:
                return None
            result = self.kernel32.WaitForSingleObject(event, timeout_ms)
            if result != WAIT_OBJECT_0:
                self.kernel32.CancelIoEx(handle, ctypes.byref(ov))
                self.kernel32.WaitForSingleObject(event, 100)
                return None
            if not self.kernel32.GetOverlappedResult(handle, ctypes.byref(ov), ctypes.byref(read), False):
                return None
            if read.value <= 0:
                return None
            return bytes(buf[: read.value])
        finally:
            self.kernel32.CloseHandle(event)


class HidTransport:
    """Control channel + optional input monitor."""

    def __init__(self, config, *, demo: bool = False):
        self.config = config
        self.demo = demo or not IS_WINDOWS
        self.lib: HidLibrary | None = None
        self.control: HidInterface | None = None
        self.monitor: HidInterface | None = None
        self.handle: int | None = None
        self.monitor_handle: int | None = None
        self.lock = threading.RLock()
        self.sent_packets: list[bytes] = []
        self.sent_blocks: list[bytes] = []
        self._stop = threading.Event()
        self._monitor_thread: threading.Thread | None = None
        self.on_event: Callable[[int, int], None] | None = None
        self.on_disconnect: Callable[[], None] | None = None
        if not self.demo:
            self.lib = HidLibrary()

    @property
    def connected(self) -> bool:
        return self.demo or self.handle is not None

    def enumerate(self) -> list[HidInterface]:
        if self.demo or self.lib is None:
            return []
        try:
            return [e for e in self.lib.enumerate()
                    if e.vendor_id == self.config.vid and e.product_id == self.config.pid]
        except Exception:
            return []

    def open(self) -> bool:
        if self.demo:
            self.sent_packets.clear()
            self.sent_blocks.clear()
            return True
        assert self.lib is not None
        with self.lock:
            if self.handle is not None:
                return True
            control = self.lib.find_control(self.config.vid, self.config.pid)
            if control is None:
                return False
            try:
                self.handle = self.lib.open(control.path, read=True, write=True)
            except OSError:
                self.handle = None
                return False
            self.control = control
            monitor = self.lib.find_monitor(self.config.vid, self.config.pid)
            if monitor is not None:
                try:
                    self.monitor_handle = self.lib.open(
                        monitor.path, read=True, write=False, overlapped=True
                    )
                    self.monitor = monitor
                    self._stop.clear()
                    self._monitor_thread = threading.Thread(
                        target=self._read_loop, name="sm809-monitor", daemon=True
                    )
                    self._monitor_thread.start()
                except OSError:
                    self.monitor_handle = None
                    self.monitor = None
            return True

    def close(self) -> None:
        self._stop.set()
        with self.lock:
            if self.lib is not None:
                if self.monitor_handle:
                    self.lib.close(self.monitor_handle)
                if self.handle:
                    self.lib.close(self.handle)
            self.monitor_handle = None
            self.handle = None
            self.control = None
            self.monitor = None

    # -- I/O ---------------------------------------------------------------
    def set_feature(self, packet: bytes) -> bool:
        if len(packet) != 8:
            raise ValueError("packet must be 8 bytes")
        self.sent_packets.append(bytes(packet))
        if self.demo:
            return True
        if self.lib is None or self.handle is None:
            return False
        with self.lock:
            try:
                return self.lib.set_feature(self.handle, packet)
            except Exception:
                return False

    def get_feature(self) -> bytes:
        if self.demo:
            return self._demo_reply()
        if self.lib is None or self.handle is None:
            return b""
        with self.lock:
            try:
                return self.lib.get_feature(self.handle)
            except Exception:
                return b""

    def write_block(self, block: bytes) -> bool:
        if len(block) != 32:
            raise ValueError("block must be 32 bytes")
        self.sent_blocks.append(bytes(block))
        if self.demo:
            return True
        if self.lib is None or self.handle is None:
            return False
        with self.lock:
            try:
                return self.lib.write_block(self.handle, block)
            except Exception:
                return False

    def _demo_reply(self) -> bytes:
        # The service deobfuscates the reply when a password is configured.
        from .protocol import deobfuscate, obfuscate
        cfg = self.config
        if self.sent_packets:
            last = self.sent_packets[-1]
            try:
                plain = deobfuscate(last, cfg.key) if cfg.has_password else last
            except Exception:
                plain = last
            cmd = plain[0]
            if cmd == 0x80:
                reply = bytes((0x00, cfg.ver_h & 0xFF, cfg.ver_l & 0xFF, 0, 0, 0, 0, 0))
                return obfuscate(reply, cfg.key)
        reply = bytes((0x00, 0xAA, 0xDD, 0x3B, 0x62, 0, 0, 0))
        return obfuscate(reply, cfg.key) if cfg.has_password else reply

    def inject_event(self, event: int, value: int) -> None:
        if self.on_event:
            self.on_event(event, value)

    def _read_loop(self) -> None:
        assert self.lib is not None and self.monitor_handle is not None
        failures = 0
        while not self._stop.is_set():
            try:
                data = self.lib.read_input_once(self.monitor_handle, 250)
            except Exception:
                data = None
            if data is None:
                failures += 1
                if failures in (40, 120):
                    # Let the manager's presence poll decide; avoid killing a
                    # healthy device because a report was slow.
                    pass
                continue
            failures = 0
            if len(data) >= 4 and data[0] == 0x06:
                event = (data[1] << 8) | data[2]
                value = data[3]
                if self.on_event:
                    try:
                        self.on_event(event, value)
                    except Exception:
                        pass
        if self.on_disconnect:
            try:
                self.on_disconnect()
            except Exception:
                pass


def describe_interfaces(config) -> str:
    """Diagnostics text used by the About/Device panel."""
    try:
        lib = HidLibrary()
    except Exception as exc:
        return f"HID library unavailable: {exc}"
    lines = [f"VID {config.vid:04X}  PID {config.pid:04X}"]
    found = False
    for entry in lib.enumerate():
        if entry.vendor_id != config.vid or entry.product_id != config.pid:
            continue
        found = True
        lines.append(
            f"usage {entry.usage_page:04X}/{entry.usage:04X}  "
            f"in={entry.input_length} out={entry.output_length} feat={entry.feature_length}"
            + (f"  {entry.product}" if entry.product else "")
        )
    if not found:
        lines.append("No matching HID interfaces present.")
    return "\n".join(lines)
