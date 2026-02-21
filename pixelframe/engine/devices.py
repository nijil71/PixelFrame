import difflib
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class DevicePreset:
    name: str
    width: int
    height: int
    device_scale_factor: float = 1.0
    is_mobile: bool = False
    has_touch: bool = False
    user_agent: Optional[str] = None

# A curated list of common device presets
DEVICE_PRESETS: Dict[str, DevicePreset] = {
    # Phones
    "pixel 8": DevicePreset("Pixel 8", 412, 915, 2.625, True, True),
    "iphone 15": DevicePreset("iPhone 15", 393, 852, 3.0, True, True),
    "iphone 15 pro max": DevicePreset("iPhone 15 Pro Max", 430, 932, 3.0, True, True),
    "galaxy s23": DevicePreset("Galaxy S23", 360, 780, 3.0, True, True),
    "galaxy z fold 5": DevicePreset("Galaxy Z Fold 5", 344, 904, 2.6, True, True),
    
    # Tablets
    "ipad mini": DevicePreset("iPad Mini", 768, 1024, 2.0, True, True),
    "ipad air": DevicePreset("iPad Air", 820, 1180, 2.0, True, True),
    "ipad pro 11": DevicePreset("iPad Pro 11", 834, 1194, 2.0, True, True),
    "ipad pro 12.9": DevicePreset("iPad Pro 12.9", 1024, 1366, 2.0, True, True),
    "galaxy tab s9": DevicePreset("Galaxy Tab S9", 1600, 2560, 2.0, True, True), # Note: often used landscape, but let's stick to portrait or standard viewport
    
    # Laptops
    "macbook air": DevicePreset("MacBook Air", 1280, 800, 2.0, False, False),
    "macbook pro 14": DevicePreset("MacBook Pro 14", 1512, 982, 2.0, False, False),
    "macbook pro 16": DevicePreset("MacBook Pro 16", 1728, 1117, 2.0, False, False),
    "surface pro 9": DevicePreset("Surface Pro 9", 2880, 1920, 2.0, False, True),
    
    # Desktops
    "desktop 1080p": DevicePreset("Desktop 1080p", 1920, 1080, 1.0, False, False),
    "desktop 1440p": DevicePreset("Desktop 1440p", 2560, 1440, 1.0, False, False),
    "desktop 4k": DevicePreset("Desktop 4K", 3840, 2160, 2.0, False, False),
}


def get_device(query: str) -> Optional[DevicePreset]:
    """Fuzzy match a query string to a device preset."""
    query_lower = query.lower().strip()
    
    # Exact match
    if query_lower in DEVICE_PRESETS:
        return DEVICE_PRESETS[query_lower]
        
    # Fuzzy match
    matches = difflib.get_close_matches(query_lower, DEVICE_PRESETS.keys(), n=1, cutoff=0.6)
    if matches:
        return DEVICE_PRESETS[matches[0]]
        
    return None

def get_devices(queries: List[str]) -> List[DevicePreset]:
    """Get multiple devices by name, ignoring invalid names."""
    devices = []
    for query in queries:
        device = get_device(query)
        if device:
            devices.append(device)
    return devices

def list_devices() -> List[str]:
    """Return a sorted list of available device names."""
    return sorted(d.name for d in DEVICE_PRESETS.values())
