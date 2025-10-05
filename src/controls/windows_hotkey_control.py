from typing import Dict, Any
from core.base_control import BaseSecurityControl
from core.interfaces import SecurityControlMetadata, RiskLevel


class WindowsHotkeyControl(BaseSecurityControl):
    """
    Security control for disabling Windows hotkeys to prevent unauthorized access.

    Supports two modes:
    1. Disable ALL Windows hotkeys via NoWinKeys registry setting
    2. Disable specific hotkeys via DisabledHotkeys registry setting
    """

    COMMON_HOTKEYS = {
        "R": {"description": "Win+R (Run dialog)", "risk": "High - Can be used to execute commands"},
        "X": {"description": "Win+X (WinX menu)", "risk": "Medium - Provides access to admin tools"},
        # "E": {"description": "Win+E (File Explorer)", "risk": "Low - Opens File Explorer"},
        # "D": {"description": "Win+D (Show Desktop)", "risk": "Low - Minimizes all windows"},
        # "L": {"description": "Win+L (Lock screen)", "risk": "None - Security feature"},
        # "I": {"description": "Win+I (Settings)", "risk": "Medium - Access to system settings"},
        # "A": {"description": "Win+A (Action Center)", "risk": "Low - Opens notification center"},
        "S": {"description": "Win+S (Search)", "risk": "Medium - Can search and launch programs"},
        # "T": {"description": "Win+T (Taskbar)", "risk": "Low - Cycles through taskbar items"},
        # "P": {"description": "Win+P (Project/Display)", "risk": "Low - Display settings"},
        # "U": {"description": "Win+U (Ease of Access)", "risk": "Medium - Accessibility settings"},
        # "V": {"description": "Win+V (Clipboard History)", "risk": "Medium - Access to clipboard data"},
    }

    def __init__(self):
        metadata = SecurityControlMetadata(
            name="Windows Hotkey Control",
            description="Disable Windows hotkeys to prevent unauthorized access to system functions",
            risk_level=RiskLevel.MEDIUM,
            purpose="Disable Windows hotkeys (keyboard shortcuts) to limit user access to system functions and prevent bypass of security controls",
            common_targets=list(self.COMMON_HOTKEYS.keys()),
            category="User Interface Security",
        )
        super().__init__(metadata)

    def validate_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Validate the hotkey control settings.

        Args:
            settings: Must contain 'disable_all_hotkeys' (bool) and/or 'disabled_hotkeys' (list)
        """
        if "disable_all_hotkeys" not in settings and "disabled_hotkeys" not in settings:
            return False

        if "disable_all_hotkeys" in settings:
            if not isinstance(settings["disable_all_hotkeys"], bool):
                return False

        if "disabled_hotkeys" in settings:
            if not isinstance(settings["disabled_hotkeys"], list):
                return False
            for hotkey in settings["disabled_hotkeys"]:
                if not isinstance(hotkey, str) or len(hotkey) != 1:
                    return False

        return True

    def get_default_configuration(self) -> Dict[str, Any]:
        """
        Get the default configuration: disable high-risk hotkeys.
        """
        return {
            "disable_all_hotkeys": False,
            "disabled_hotkeys": ["R", "X"],  # Win+R and Win+X are high risk
        }

    def get_configuration_schema(self) -> Dict[str, Any]:
        """
        Get the schema describing available hotkeys.
        """
        return {
            "common_hotkeys": {
                key: f"{config['description']} - Risk: {config['risk']}"
                for key, config in self.COMMON_HOTKEYS.items()
            }
        }
