"""Translate application settings changes into queued device commands."""

from collections.abc import Callable, Mapping
from typing import Any


class DeviceCommandService:
    def __init__(self, controller: Any) -> None:
        self._controller = controller

    def _submit(self, *args: Any, **kwargs: Any) -> None:
        self._controller.call(*args, **kwargs)

    def set_dpi(self, values: Any, selected: int = 0, colors: Any = None) -> None:
        self._submit("set_dpi", values, selected=selected, colors=colors)

    def set_active_dpi(self, values: Any, selected: int) -> None:
        self._submit("set_active_dpi", values, selected)

    def apply_buttons(self, codes: Any, macros: Any) -> None:
        self._submit("apply_macro_buttons", codes, macros)

    def set_lighting(self, mode: int, color: Any) -> None:
        self._submit("set_lighting", mode, color=color)

    def set_polling_rate(self, hz: int) -> None:
        self._submit("set_polling_rate", hz)

    def set_lod(self, mm: int) -> None:
        self._submit("set_lod", mm)

    def set_power(self, sleep_min: int, move_wakeup: bool, move_lighting: bool) -> None:
        self._submit("set_power", sleep_time=sleep_min,
                     move_wakeup=move_wakeup, move_lighting=move_lighting)

    def set_sensor_flags(self, angle_snap: bool, motion_sync: bool, ripple: bool) -> None:
        self._submit("set_sensor_flags", angle_snap=angle_snap,
                     motion_sync=motion_sync, ripple=ripple)

    def factory_reset(self) -> None:
        self._submit("factory_reset")

    def apply_config(
        self,
        previous: Mapping[str, Any] | None,
        config: Mapping[str, Any],
        resolve_bindings: Callable[[Any], tuple[Any, Any]],
    ) -> None:
        def changed(section):
            return previous is None or previous.get(section) != config.get(section)

        if changed("dpi"):
            dpi = config.get("dpi", {})
            self.set_dpi(dpi.get("values", []),
                         selected=dpi.get("selected", 0), colors=dpi.get("colors"))
        if changed("polling_hz"):
            self.set_polling_rate(config.get("polling_hz", 500))
        if changed("lod_mm"):
            self.set_lod(config.get("lod_mm", 2))
        if changed("lighting"):
            light = config.get("lighting", {})
            self.set_lighting(light.get("mode", 2),
                              tuple(light.get("color", (0, 0, 255))))
        if changed("power"):
            power = config.get("power", {})
            self.set_power(power.get("sleep_min", 20),
                           power.get("move_wakeup", True),
                           power.get("move_lighting", True))
        if changed("sensor"):
            sensor = config.get("sensor", {})
            self.set_sensor_flags(sensor.get("angle_snap", False),
                                  sensor.get("motion_sync", True),
                                  sensor.get("ripple", False))
        if changed("buttons"):
            self.apply_buttons(*resolve_bindings(config.get("buttons", [])))
