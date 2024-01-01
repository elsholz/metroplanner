from typing import Dict


class ViewerCache:
    """
    TODO 
    """
    def __init__(self) -> None:
        self.__plans = {}
        self.__planstates = {}

    def get_plan(shortlink: str) -> Dict:
        pass

    def get_planstate(shortlink: str) -> Dict:
        pass

    def invalidate_cache(shortlink: str) -> None:
        pass
