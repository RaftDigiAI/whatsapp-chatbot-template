from enum import Enum


class AppStringEnum(str, Enum):
    """Base Enum class for strings"""

    def __str__(self):
        return self.value


class AppNumberEnum(int, Enum):
    """Base Enum class for int's"""

    def __str__(self):
        return str(self.value)
