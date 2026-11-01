"""Data.ini parser matching the shipped configuration format."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .keys import key_id_for_vk  # noqa: F401  (re-export convenience)


DEFAULT_BUTTONS = [
    [0x01, 0x00, 0xF0, 0x00, 1],
    [0x01, 0x00, 0xF1, 0x00, 1],
    [0x01, 0x00, 0xF2, 0x00, 1],
    [0x04, 0x00, 0x01, 0x00, 1],
    [0x04, 0x00, 0x02, 0x00, 1],
]


@dataclass
class DeviceConfig:
    vid: int = 0x04D9
    pid: int = 0xA09F
    dpi: int = 8
    sensor: int = 3311
    password: str = "FB1570"
    distance: int = 0
    distance_min: int = 0
    distance_max: int = 2
    distance_values: list[int] = field(default_factory=lambda: [0, 1, 2, 0, 0, 0, 0, 0])
    ver_h: int = 2
    ver_l: int = 1
    update: bool = False
    buttons: list[list[int]] = field(default_factory=list)
    source_path: Path | None = None

    def __post_init__(self) -> None:
        if not self.buttons:
            self.buttons = [row[:] for row in _default_button_rows()]

    @property
    def has_password(self) -> bool:
        return len(self.password) == 6

    @property
    def key(self) -> bytes:
        return self.password.encode("latin1", "replace")[:6].ljust(6, b"\0")

    def raw_button(self, index: int) -> list[int]:
        if 0 <= index < len(self.buttons):
            return self.buttons[index]
        return [0, 0, 0, 0, 1]

    def button_is_computed(self, index: int) -> bool:
        return bool(self.raw_button(index)[4])

    def distance_value_for_stage(self, stage: int) -> int:
        if 0 <= stage < len(self.distance_values):
            return self.distance_values[stage] & 0xFF
        return 0

    def to_ini_text(self) -> str:
        lines = ["[Default]", f"VID={self.vid:04x}", f"PID={self.pid:04X}"]
        lines.append(f"DPI={self.dpi}")
        lines.append(f"Sensor={self.sensor}")
        lines.append(f"Distance={self.distance}")
        lines.append(f"Distance_Min={self.distance_min}")
        lines.append(f"Distance_Max={self.distance_max}")
        lines.append("Distance_Value=" + ",".join(str(v) for v in self.distance_values))
        lines.append(f"Password={self.password}")
        lines.append(f"Ver_H={self.ver_h}")
        lines.append(f"Ver_L={self.ver_l}")
        lines.append(f"Update={1 if self.update else 0}")
        lines.append("")
        lines.append("[BUTTON]")
        for i, row in enumerate(self.buttons, 1):
            lines.append(f"{i}=" + ",".join(f"{b:02X}" for b in row))
        return "\n".join(lines) + "\n"

    def save(self, path: Path) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(self.to_ini_text(), encoding="utf-8")
        tmp.replace(path)


def _default_button_rows() -> list[list[int]]:
    rows: list[list[int]] = []
    for i in range(64):
        if i < len(DEFAULT_BUTTONS):
            rows.append(DEFAULT_BUTTONS[i][:])
        else:
            rows.append([0x00, 0x00, 0x00, 0x00, 0])
    return rows


def load_config(path: Path) -> DeviceConfig:
    if not path.exists():
        cfg = DeviceConfig()
        cfg.source_path = path
        return cfg

    defaults: dict[str, str] = {}
    button_lines: dict[int, str] = {}
    section = ""
    for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("//") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if section == "default":
            defaults[key] = value
        elif section == "button":
            try:
                button_lines[int(key)] = value
            except ValueError:
                pass

    def _int(name: str, fallback: int) -> int:
        try:
            return int(defaults.get(name, str(fallback)), 0)
        except ValueError:
            return fallback

    def _hex(name: str, fallback: int) -> int:
        text = defaults.get(name)
        if not text:
            return fallback
        try:
            return int(text, 16)
        except ValueError:
            return fallback

    cfg = DeviceConfig(
        vid=_hex("VID", 0x04D9),
        pid=_hex("PID", 0xA09F),
        dpi=_int("DPI", 8),
        sensor=_int("Sensor", 3311),
        password=defaults.get("Password", ""),
        distance=_int("Distance", 0),
        distance_min=_int("Distance_Min", 0),
        distance_max=_int("Distance_Max", 2),
        ver_h=_int("Ver_H", 2),
        ver_l=_int("Ver_L", 1),
        update=bool(_int("Update", 0)),
    )
    values = defaults.get("Distance_Value")
    if values:
        parsed: list[int] = []
        for token in values.split(","):
            try:
                parsed.append(int(token.strip(), 0) & 0xFF)
            except ValueError:
                parsed.append(0)
        cfg.distance_values = (parsed + [0] * 8)[:8]

    rows = _default_button_rows()
    for index, text in button_lines.items():
        if not (1 <= index <= 64):
            continue
        parts = [p.strip() for p in text.split(",") if p.strip()]
        vals: list[int] = []
        for p in parts[:5]:
            try:
                vals.append(int(p, 16))
            except ValueError:
                vals.append(0)
        vals = (vals + [0, 0, 0, 0, 1])[:5]
        vals = [v & 0xFF for v in vals[:4]] + [1 if vals[4] else 0]
        rows[index - 1] = vals
    cfg.buttons = rows
    cfg.source_path = path
    return cfg
