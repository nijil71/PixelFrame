from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Breakpoint:
    name: str
    width: int
    height: int

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