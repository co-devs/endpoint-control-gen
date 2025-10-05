"""
batch_generator.py

This module provides a generator for creating Windows batch scripts that implement
security controls such as file associations and firewall rules.
"""

from datetime import datetime
from typing import Dict, Any
from generators.base_generator import BaseArtifactGenerator


class BatchGenerator(BaseArtifactGenerator):
    """
    Generates Windows batch scripts to apply security controls based on provided settings.
    Supports file associations and firewall rules.
    """

    def generate(self, control_name: str, settings: Dict[str, Any]) -> str:
        """
        Generate a batch script string based on the control name and settings.

        Args:
            control_name (str): The name of the security control.
            settings (Dict[str, Any]): Dictionary containing settings such as
                'file_associations' and/or 'firewall_rules'.

        Returns:
            str: The generated batch script as a string.
        """
        batch_lines = [
            "@echo off",
            f"REM Windows Security Control: {control_name}",
            f"REM Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "REM Check for administrator privileges",
            "net session >nul 2>&1",
            "if %errorLevel% neq 0 (",
            "    echo This script requires Administrator privileges",
            "    pause",
            "    exit /b 1",
            ")",
            "",
            "echo Implementing security control...",
            "",
        ]

        # Add file association commands if present in settings
        if "file_associations" in settings:
            batch_lines.append("REM File Association Changes")
            for ext, app in settings["file_associations"].items():
                batch_lines.extend(
                    [
                        f"assoc {ext}={app}File",
                        f'ftype {app}File="{app}" "%%1"',
                    ]
                )
            batch_lines.append("")

        # Add firewall rule commands if present in settings
        if "firewall_rules" in settings:
            batch_lines.append("REM Windows Firewall Rules")
            for rule in settings["firewall_rules"]:
                batch_lines.append(
                    f"netsh advfirewall firewall add rule name=\"{rule['name']}\" dir=out action=block program=\"{rule['program']}\""
                )
            batch_lines.append("")

        # Add WinX menu modification commands if present in settings
        if "winx_removal" in settings:
            batch_lines.extend(
                [
                    "REM WinX Menu Modification - Apply to all users and default profile",
                    "echo Modifying WinX menu for all users...",
                    "",
                    "REM Process each user profile",
                    'for /D %%U in (C:\\Users\\*) do (',
                    '    if exist "%%U\\AppData\\Local\\Microsoft\\Windows\\WinX" (',
                    '        echo Processing: %%~nxU',
                ]
            )

            for item in settings["winx_removal"]:
                batch_lines.append(
                    f'        del /F /S /Q "%%U\\AppData\\Local\\Microsoft\\Windows\\WinX\\*{item}*" 2>nul'
                )

            batch_lines.extend(
                [
                    "    )",
                    ")",
                    "",
                    "REM Modify default user profile for new users",
                    'if exist "C:\\Users\\Default\\AppData\\Local\\Microsoft\\Windows\\WinX" (',
                    '    echo Processing: Default User Profile',
                ]
            )

            for item in settings["winx_removal"]:
                batch_lines.append(
                    f'    del /F /S /Q "C:\\Users\\Default\\AppData\\Local\\Microsoft\\Windows\\WinX\\*{item}*" 2>nul'
                )

            batch_lines.extend(
                [
                    ")",
                    "",
                    "REM Restart Explorer to apply changes",
                    "taskkill /F /IM explorer.exe >nul 2>&1",
                    "start explorer.exe",
                    "",
                ]
            )

        # Add Windows hotkey control commands if present in settings
        if "disable_all_hotkeys" in settings or "disabled_hotkeys" in settings:
            batch_lines.extend(
                [
                    "REM Windows Hotkey Control",
                    "echo Configuring Windows hotkey restrictions...",
                    "",
                ]
            )

            # Option 1: Disable all Windows hotkeys via NoWinKeys policy
            if settings.get("disable_all_hotkeys", False):
                batch_lines.extend(
                    [
                        "REM Disable ALL Windows hotkeys (system-wide)",
                        "echo   Disabling all Windows hotkeys (system-wide)...",
                        'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoWinKeys /t REG_DWORD /d 1 /f',
                        "",
                    ]
                )

            # Option 2: Disable specific hotkeys via DisabledHotkeys setting
            if settings.get("disabled_hotkeys") and len(settings["disabled_hotkeys"]) > 0:
                hotkeys_string = "".join(settings["disabled_hotkeys"])
                batch_lines.extend(
                    [
                        f"REM Disable specific Windows hotkeys: {hotkeys_string}",
                        f"echo   Disabling specific hotkeys: {hotkeys_string}",
                        "",
                        "REM Process each user profile",
                        'for /D %%U in (C:\\Users\\*) do (',
                        '    if exist "%%U\\NTUSER.DAT" (',
                        '        echo     Processing: %%~nxU',
                        '        REM Load user hive',
                        '        reg load "HKU\\TempUser_%%~nxU" "%%U\\NTUSER.DAT" 2>nul',
                        f'        reg add "HKU\\TempUser_%%~nxU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v DisabledHotkeys /t REG_SZ /d "{hotkeys_string}" /f 2>nul',
                        '        reg unload "HKU\\TempUser_%%~nxU" 2>nul',
                        "    )",
                        ")",
                        "",
                        "REM Apply to default user profile for new users",
                        'reg load "HKU\\DefaultUser" "C:\\Users\\Default\\NTUSER.DAT" 2>nul',
                        f'reg add "HKU\\DefaultUser\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v DisabledHotkeys /t REG_SZ /d "{hotkeys_string}" /f 2>nul',
                        'reg unload "HKU\\DefaultUser" 2>nul',
                        "",
                    ]
                )

        batch_lines.extend(
            [
                "echo Security control implementation completed!",
                "echo Please reboot the system to ensure all changes take effect.",
                "pause",
            ]
        )

        return "\n".join(batch_lines)

    def get_file_extension(self) -> str:
        """
        Returns the file extension for the generated batch script.

        Returns:
            str: The file extension ('bat').
        """
        return "bat"

    def get_mime_type(self) -> str:
        """
        Returns the MIME type for the generated batch script.

        Returns:
            str: The MIME type ('text/plain').
        """
        return "text/plain"
