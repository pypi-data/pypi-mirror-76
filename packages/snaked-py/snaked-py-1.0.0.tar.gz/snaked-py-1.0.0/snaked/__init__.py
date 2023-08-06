"""
Snaked is a lightweight high-performance wrapper for accessing camelCase and PascalCase python objects using snake_case syntax.
"""

__version__ = "1.0.0"
__author__ = "Squirrel-Preslash"
__license__ = "MIT"
__all__ = ("Snaked", "clear_cache")


from typing import Any
from stringcase import camelcase, pascalcase, snakecase

class Snaked(object):
    """ Enables snake-case access to camelCase and PascalCase attributes and methods on an object """

    def __init__(self, target: Any, use_cache: bool=True) -> None:
        """ Create a snake-case-access wrapper on the given target object

        Parameters
        ----------
        target: Object to wrap for snake-case access
        use_cache: When a certain snake_cased attribute was resolved to camelCase/PascalCase, don't re-resolve every time the snake_cased attribute is being accessed but return the previously resolved attribute. Improves Performance.
        """

        self.__target = target
        self.__use_cache = use_cache
        self.__resolution_cache = {}
    
    def __getattr__(self, name: str) -> Any:
        if self.__use_cache and name in self.__resolution_cache:
            return getattr(self.__target, self.__resolution_cache[name])
        if hasattr(self.__target, name):
            if self.__use_cache: self.__resolution_cache[name] = name
            return getattr(self.__target, name)
        else:
            camel_case = camelcase(name)
            if hasattr(self.__target, camel_case) and snakecase(name) == name:
                # snakecase(name) == name makes sure that we're only auto-converting snake-case names. Anything else may lead to unexpected results.
                if self.__use_cache: self.__resolution_cache[name] = camel_case
                return getattr(self.__target, camel_case)
            else:
                pascal_case = pascalcase(name)
                if hasattr(self.__target, pascal_case) and snakecase(name) == name:
                    # snakecase(name) == name makes sure that we're only auto-converting snake-case names. Anything else may lead to unexpected results.
                    if self.__use_cache: self.__resolution_cache[name] = pascal_case
                    return getattr(self.__target, pascal_case)
                else:
                    if name == "__clear_cache":
                        return self.__clear_cache
                    return getattr(self.__target, name) # go through the usual (now definitely error-throwing) routine of obtaining an attribute
        
    def __clear_cache(self) -> None:
        """ Clear the attribute resolution cache """
        del self.__resolution_cache
        self.__resolution_cache = {}

def clear_cache(snaked_object: Snaked) -> None:
    """ Clear the attribute resolution cache of a Snaked object
    Parameters
    ----------
    snaked_object: An instance of the Snaked class
    """

    if isinstance(snaked_object, Snaked):
        snaked_object.__clear_cache()
    else:
        raise TypeError("clear_cache() requires 1 argument that is an instance of 'Snaked'.")