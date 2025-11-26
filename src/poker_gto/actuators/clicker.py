"""Clicker actuator for VRChat Poker."""

import sys
import time


class Clicker:
    """Actuator for clicking at specific screen coordinates."""

    def __init__(self):
        self._impl = None
        if sys.platform == "win32":
            try:
                import pydirectinput

                self._impl = pydirectinput
                # Disable fail-safe to avoid crashes if mouse hits corner
                pydirectinput.FAILSAFE = False
            except ImportError:
                print("Warning: pydirectinput not found on Windows.")
        elif sys.platform == "linux":
            try:
                import inputtino

                self._impl = inputtino.Mouse()
            except ImportError:
                print("Warning: inputtino not found on Linux.")

    def click(self, x: int, y: int, duration: float = 0.1) -> None:
        """Click at the specified coordinates.

        Args:
            x: X coordinate.
            y: Y coordinate.
            duration: Duration of the press (for long press).
        """
        if self._impl is None:
            print(f"[MOCK] Click at ({x}, {y}) duration={duration}")
            return

        if sys.platform == "win32":
            # Windows implementation using pydirectinput
            self._impl.moveTo(x, y)
            self._impl.mouseDown()
            time.sleep(duration)
            self._impl.mouseUp()
        elif sys.platform == "linux":
            # Linux implementation using inputtino
            # inputtino.Mouse.move_abs(x, y) might need screen dimensions or normalized coords?
            # Let's assume it takes pixel coords if not specified otherwise, or check docs.
            # But based on dir(), it has move_abs.
            # Usually inputtino works with absolute coords mapped to screen.
            self._impl.move_abs(x, y)
            self._impl.press("left")
            time.sleep(duration)
            self._impl.release("left")
