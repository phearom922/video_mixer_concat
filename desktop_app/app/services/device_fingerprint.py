"""Device fingerprinting service for Windows."""
import platform
import subprocess
import winreg
from typing import Optional


def get_machine_guid() -> Optional[str]:
    """Get Windows MachineGuid from registry."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography"
        )
        guid, _ = winreg.QueryValueEx(key, "MachineGuid")
        winreg.CloseKey(key)
        return guid
    except (OSError, FileNotFoundError, ValueError):
        return None


def get_hostname() -> str:
    """Get system hostname."""
    return platform.node()


def get_cpu_serial() -> Optional[str]:
    """Get CPU serial number (fallback method)."""
    try:
        result = subprocess.run(
            ["wmic", "cpu", "get", "ProcessorId"],
            capture_output=True,
            text=True,
            timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            return lines[1].strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    return None


def get_disk_serial() -> Optional[str]:
    """Get disk serial number (fallback method)."""
    try:
        result = subprocess.run(
            ["wmic", "diskdrive", "get", "serialnumber"],
            capture_output=True,
            text=True,
            timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            return lines[1].strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    return None


def get_device_fingerprint() -> str:
    """
    Get device fingerprint.
    
    Primary: MachineGuid from registry
    Fallback: Combination of hostname + CPU serial + disk serial
    """
    # Try primary method
    machine_guid = get_machine_guid()
    if machine_guid:
        return machine_guid
    
    # Fallback method
    parts = [get_hostname()]
    
    cpu_serial = get_cpu_serial()
    if cpu_serial:
        parts.append(cpu_serial)
    
    disk_serial = get_disk_serial()
    if disk_serial:
        parts.append(disk_serial)
    
    # Join parts with separator
    return "|".join(parts)
