"""Module contenant la classe Triangle."""

import struct

from pointset_manager.models.PointSet import PointSet


class Triangle:
    """Classe représentant un triangle."""

    def __init__(self, indices: tuple):
        """Permet d'initialiser un triangle.

        Args:
            indices (tuple): Les indices des points du triangle.

        Raises:
            ValueError: Si le tuple n'a pas exactement 3 éléments.
            TypeError: Si les éléments du tuple ne sont pas des entiers.

        """
        if len(indices) != 3:
            raise ValueError

        for i in indices:
            if type(i) is not int:
                raise TypeError

        self.indices: tuple = indices
    
    def to_bytes(self) -> str:
        """Permet de convertir un triangle en bytes.

        Returns:
            str: Les bytes du triangle.

        """
        return struct.pack("<LLL", self.indices[0], self.indices[1], self.indices[2])
    
    @staticmethod
    def from_bytes(source: bytes|bytearray, pointset: PointSet) -> "Triangle":
        """Permet de convertir des bytes en triangle.

        Args:
            source (bytes | bytearray): Les bytes du triangle.
            pointset (PointSet): Le pointset contenant les points du triangle.

        Raises:
            TypeError: Si le source n'est pas un bytes ou un bytearray.
            ValueError: Si le source n'a pas exactement 12 octets.
            ValueError: Si le pointset est None.
            IndexError: Si les indices ne sont pas valides.

        Returns:
            Triangle: Le triangle correspondant aux bytes.

        """
        if type(source) is not bytes and type(source) is not bytearray:
            raise TypeError
        if len(source) != 12:
            raise ValueError
        if pointset is None:
            raise ValueError

        try:
            indices = struct.unpack("<LLL", source)
        except Exception as err:
            raise ValueError from err
        
        try:
            for i in indices:
                pointset.points[i]
        except Exception as err:
            raise IndexError from err
        
        return Triangle(indices)