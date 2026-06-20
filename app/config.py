import os
import re
from dataclasses import dataclass, field
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def project_path(env_name: str, default: str) -> Path:
    path = Path(os.getenv(env_name, default)).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


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

    allowed_extensions: set[str] = field(
        default_factory=lambda: {
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
    )

    lang_icons: dict[str, str] = field(
        default_factory=lambda: {
            "py": "🐍",
            "cpp": "⚙️",
            "c": "⚙️",
            "js": "📜",
            "json": "🧾",
            "md": "📄",
            "txt": "📄",
        }
    )

    filename_pattern: re.Pattern = re.compile(r"^(\d+)(?:part(\d+))?$")


APP_CONFIG = AppConfig(
    dns=os.getenv("APP_DNS", "localhost"),
    host=os.getenv("APP_HOST", "0.0.0.0"),
    port=int(os.getenv("APP_PORT", "8000")),
)

APP_PATHS = AppPaths(
    codes_dir=project_path("FILES_DIR", "app/code_storage"),
    static_dir=project_path("STATIC_DIR", "app/static"),
    templates_dir=project_path("TEMPLATES_DIR", "app/templates"),
    views_json=project_path("VIEWS_FILE", "app/views.json"),
)

APP_VARIABLES = AppVariables()
