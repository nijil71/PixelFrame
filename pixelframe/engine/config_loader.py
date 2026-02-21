import yaml
from pathlib import Path
from pixelframe.engine.config import PixelFrameConfig, DEFAULT_BREAKPOINTS, Breakpoint
from pixelframe.engine.devices import get_devices

def load_config(path: str) -> PixelFrameConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    if not data:
        raise ValueError(f"Config file {path} is empty or invalid.")
        
    if "url" not in data:
        raise ValueError("Config file must specify a 'url'.")
        
    output_dir = data.get("output", data.get("output_dir", "pixelframe-output"))
    full_page = data.get("full_page", True)
    
    breakpoints = []
    
    if "devices" in data:
        devices_input = data["devices"]
        if isinstance(devices_input, str):
            device_names = [d.strip() for d in devices_input.split(",")]
        else:
            device_names = devices_input
            
        found_devices = get_devices(device_names)
        breakpoints = [
            Breakpoint(
                name=d.name,
                width=d.width,
                height=d.height,
                device_scale_factor=d.device_scale_factor,
                is_mobile=d.is_mobile,
                has_touch=d.has_touch,
                user_agent=d.user_agent
            ) for d in found_devices
        ]
        
    elif "breakpoints" in data:
        for bp in data["breakpoints"]:
            name = bp.get("name", "custom")
            width = bp.get("width")
            height = bp.get("height")
            
            if not width or not height:
                raise ValueError("Custom breakpoints must specify 'width' and 'height'.")
                
            scale = bp.get("device_scale_factor", 1.0)
            is_mobile = bp.get("is_mobile", False)
            has_touch = bp.get("has_touch", False)
            user_agent = bp.get("user_agent", None)
            
            breakpoints.append(Breakpoint(
                name=name, width=width, height=height, 
                device_scale_factor=scale, is_mobile=is_mobile, 
                has_touch=has_touch, user_agent=user_agent
            ))
            
    if not breakpoints:
        breakpoints = DEFAULT_BREAKPOINTS
        
    return PixelFrameConfig(
        url=data["url"],
        output_dir=output_dir,
        full_page=full_page,
        breakpoints=breakpoints
    )
