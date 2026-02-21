from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Breakpoint:
    name: str
    width: int
    height: int
    device_scale_factor: float = 1.0
    is_mobile: bool = False
    has_touch: bool = False
    user_agent: Optional[str] = None

@dataclass
class PixelFrameConfig:
    url: str
    output_dir: str
    full_page: bool
    breakpoints: List[Breakpoint]


DEFAULT_BREAKPOINTS = [
    Breakpoint("mobile", 375, 812),
    Breakpoint("tablet", 768, 1024),
    Breakpoint("laptop", 1366, 768),
    Breakpoint("desktop", 1920, 1080),
]