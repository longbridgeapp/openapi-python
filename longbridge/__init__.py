from . import engine_uniffi

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__package__)

appid = engine_uniffi.AppId.OPENAPI
env = engine_uniffi.Env.PROD
app_info = engine_uniffi.AppInfo(appid, env, version=__version__)
engine_uniffi.init_engine(app_info)

__all__ = ["http"]
