import json, os, sys


def get_env_var(var_name) -> str:
  try:
    return os.environ[var_name]
  except KeyError:
    sys.stderr.write(f"Cannot get {var_name} env var\nExiting!")
    sys.exit(1)