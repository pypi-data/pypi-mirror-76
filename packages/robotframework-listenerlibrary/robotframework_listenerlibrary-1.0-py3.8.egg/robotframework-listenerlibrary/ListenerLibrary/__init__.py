import pkg_resources
from .keywords import ListenerLibraryKeywords


#__version__ = pkg_resources.get_distribution("robotframework-listenerlibrary").version


class ListenerLibrary(ListenerLibraryKeywords):
    """
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"