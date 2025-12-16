"""Module contenant la classe Point."""

import math
import struct


class Point:
    """Classe représentant un point 2D."""
    
    def __init__(self, x: float, y: float):
        """Permet d'initialiser un point.

        Args:
            x (float): Coordonnée x du point.
            y (float): Coordonnée y du point.

        Raises:
            TypeError: Si x ou y ne sont pas des float.
            ValueError: Si x ou y sont NaN ou infinis.
        
        """
        if type(x) is not float:
            raise TypeError
        if type(y) is not float:
            raise TypeError
        if math.isnan(x) or math.isinf(x):
            raise ValueError
        if math.isnan(y) or math.isinf(y):
            raise ValueError

        self.x: float = x
        self.y: float = y
    
    def to_bytes(self) -> str:
        """Permet de convertir un point en bytes.

        Returns:
            str: Les bytes du point.
        
        """
        return struct.pack("<ff", self.x, self.y)
       
    @staticmethod
    def from_bytes(source: bytes|bytearray) -> "Point":
        """Permet de convertir des bytes en point.

        Args:
            source (bytes | bytearray): Les bytes du point.

        Raises:
            TypeError: Si le source n'est pas de type bytes ou bytearray.
            ValueError: Si le source n'a pas exactement 8 octets.
            ValueError: Si les bytes ne peuvent pas être décodés.

        Returns:
            Point: Le point correspondant aux bytes.
        
        """
        if type(source) is not bytes and type(source) is not bytearray:
            raise TypeError
        if len(source) != 8:
            raise ValueError

        try:
            x, y = struct.unpack("<ff", source)
        except Exception as err:
            raise ValueError from err
        
        return Point(x, y)