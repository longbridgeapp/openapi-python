import importlib, os

dir = importlib.util.find_spec("longbridge").origin[:-12]
os.system(f"cp {dir}/libengine_uniffi.so ./longbridge/")
os.system(f"cp ./longbridge/engine_uniffi.py {dir}/")
