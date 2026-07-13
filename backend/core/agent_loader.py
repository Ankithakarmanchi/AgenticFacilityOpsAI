import importlib
import pkgutil
from fastapi import FastAPI
from api import __path__ as api_path


def register_all_agents(app: FastAPI) -> None:
    """
    Scans backend/api/ for any module that exposes a `router`
    object and registers it automatically. Adding a new agent
    = adding a new file here. No edits to app.py required.
    """
    for _, module_name, _ in pkgutil.iter_modules(api_path):
        module = importlib.import_module(f"api.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)
            print(f"[agent_loader] Registered agent router: {module_name}")