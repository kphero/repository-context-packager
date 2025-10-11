import logging
import os

try:
    import toml
except ImportError:
    toml = None


DEFAULT_CONFIG_FILE = ".scan-repo-config.toml"


def load_config_file(path: str = DEFAULT_CONFIG_FILE) -> dict:
    """
    Load configuration from a TOML file if available.
    Returns an empty dict if no config file or toml not installed.
    """
    if not os.path.exists(path):
        logging.debug("No config file found at %s", path)
        return {}

    if toml is None:
        logging.warning("TOML support not found. Install 'toml' package to enable config file support.")
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = toml.load(f)
        logging.debug("Loaded config from %s", path)
        return cfg
    except Exception as e:
        logging.warning("Failed to load config file %s: %s", path, e)
        return {}


def merge_config(args, cfg: dict, key: str, cast, current_value):
    """
    Merge CLI args with config defaults.
    - If CLI provided a value, keep it.
    - Otherwise, try to pull from config and cast it.
    - If casting fails, log a warning and return the current value.
    """
    # If CLI already provided something meaningful, keep it
    if current_value not in (None, [], False):
        return current_value

    if key in cfg:
        try:
            # Special handling for booleans
            if cast is bool:
                val = cfg[key]
                if isinstance(val, bool):
                    return val
                return str(val).lower() == "true"
            # Lists
            if cast is list and not isinstance(cfg[key], list):
                return [cfg[key]]
            return cast(cfg[key])
        except Exception:
            logging.warning("Invalid value for %s in config; ignoring.", key)

    return current_value