class ClickHouseMetaClass(type):
    """
        Metaclass implementing the singleton pattern for ClickHouseMetaClass instances.

        This metaclass ensures that only one instance of a class using ClickHouseMetaClass
        is created and returned when called.

        Attributes:
            _instance: The single instance of the class.

        Methods:
            __call__(self, *args, **kwargs): Overrides the call behavior of the class.
                If the _instance attribute is None, it creates a new instance using the
                super().__call__() method and assigns it to _instance. Otherwise, it
                returns the existing instance.

        Usage:
            class MyClass(metaclass=ClickHouseMetaClass):
                pass

            obj1 = MyClass()
            obj2 = MyClass()

            obj1 is obj2  # True
        """

    _instance = None

    def __call__(self, *args, **kwargs):
        """
                Overrides the call behavior of the class.

                If the _instance attribute is None, it creates a new instance using the
                super().__call__() method and assigns it to _instance. Otherwise, it
                returns the existing instance.

                Args:
                    *args: Positional arguments to be passed to the class constructor.
                    **kwargs: Keyword arguments to be passed to the class constructor.

                Returns:
                    The instance of the class.

                Raises:
                    Any exceptions raised by the class constructor.
        """

        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
        return self._instance
