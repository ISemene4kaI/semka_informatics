import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set, Dict

@dataclass
class AppConfig:
    dns: str
    host: str
    port: int
    
@dataclass
class AppPaths:
    codes_dir: Path
    static_dir: Path
    templates_dir: Path
    
    views_json: Path
    
@dataclass
class AppVariables:
    max_file_bytes: int = 1_000_000
    
    allowed_extensions: Set[str] = {
        "py",
        "js",
        "html",
        "css",
        "cpp",
        "c",
        "java",
        "txt",
        "md",
        "json",
    }
    
    lang_icons: Dict[str, str] = {
        "py": "🐍",
        "cpp": "⚙️",
        "c": "⚙️",
        "js": "📜",
        "json": "🧾",
        "md": "📄",
        "txt": "📄",
    }

    filename_pattern: re.Pattern = re.compile(r"^(\d+)(?:part(\d+))?$")