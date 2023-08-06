# pylint: disable=not-callable

from typing import Dict, Callable, Union

class MethodGroup:
    """Groups methods to be used by an asyncjsonrpc Client or Server."""

    def __init__(self):
        """Initializes a MethodGroup."""

        self.__methods__: Dict[str, Callable] = {}

    def add_method(self, method: Callable, name: str = None) -> None:
        """Adds a method to this MethodGroup.

        The method will be added with the provided name, or with the method's name if a name is not specified.

        Arguments:
            method: Method to be added.

        Keyword Arguments:
            name: Name for the method, if not set then the name will be automatically determined from the
                method. (default: None)

        Raises:
            ValueError: raised when the group already contains a method with the same name.
        """

        name = name or method.__name__
        if name in self.__methods__:
            raise ValueError(f'A method with the name "{name}" already exists in this MethodGroup')

        self.__methods__[name] = method

    def remove_method(self, method: Union[Callable, str]) -> None:
        """Removes a method from this MethodGroup.

        The method argument may be either the method itself, or the method's name as a string.

        Arguments:
            method: Method to be removed, as either the method itself or the method's name as
                a string.

        Raises:
            ValueError: raised when the group does not contain the specified method.
        """

        name = method.__name__ if callable(method) else method

        if not name in self.__methods__:
            raise ValueError(f'A method with the name "{name}" does not exist in this MethodGroup')

        del self.__methods__[name]

    def get_method_by_name(self, method_name: str) -> Callable:
        """Gets a method from this MethodGroup by name.

        Arguments:
            method_name: Name of the method to be retrieved.

        Returns:
            Retrieved method, or None if no method with the specified name exists.
        """

        return self.__methods__.get(method_name)

    def method(self, decorated: Callable) -> Callable:
        """Decorator. Adds the decorated method to this MethodGroup.

        Arguments:
            decorated: Method to be decorated.

        Returns:
            Decorated method.
        """

        self.add_method(decorated)
        return decorated