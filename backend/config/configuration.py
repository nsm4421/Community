from dataclasses import dataclass
from os.path import abspath, dirname
from os import environ

current_file_path = abspath(__file__)
default_base_dir = dirname(dirname(dirname(current_file_path)))

@dataclass
class BaseConfig:
    """
        기본 세팅
    """
    PORT:int = 8000
    BASE_DIR = default_base_dir
    DB_POOL_RECYCLE:int = 900
    DE_ECHO:bool = True

@dataclass
class DevConfig(BaseConfig):
    """
        개발용 세팅
    """
    RELOAD:bool = True

@dataclass
class ProdConfig(BaseConfig):
    """
        배포용 세팅
    """
    RELOAD:bool = False

def get_configuration():
    """
        현재 설정 가져오기
        - os.environ == "prod" → ProdConfig
        - else → DevConfig
    """
    config = {
        "prod" : ProdConfig(),
        "dev" : DevConfig()
    }
    return config.get(environ.get("API_ENV", "dev"))