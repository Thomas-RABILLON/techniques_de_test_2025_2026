"""Module contenant la classe PointSet."""

import struct

from pointset_manager.models.Point import Point


class PointSet:
    """Classe représentant un ensemble de points."""
    
    def __init__(self, list_of_point: list):
        """Permet de créer un ensemble de points.

        Args:
            list_of_point (list): La liste des points.
        
        """
        self.points: list = list_of_point
    
    def __len__(self) -> int:
        """Permet de retourner le nombre de points."""
        return len(self.points)
    
    def add_point(self, point: Point) -> None:
        """Permet d'ajouter un point à l'ensemble.

        Args:
            point (Point): Le point à ajouter.

        Raises:
            TypeError: Si le point n'est pas de type Point.
        
        """
        if type(point) is not Point:
            raise TypeError
        
        self.points.append(point)

    def to_bytes(self) -> str:
        """Permet de convertir l'ensemble de points en bytes.

        Raises:
            ValueError: Si l'ensemble de points est vide.

        Returns:
            str: La représentation en bytes de l'ensemble de points.
        
        """
        if len(self.points) <= 0:
            raise ValueError

        res = struct.pack("<L", len(self.points))

        for point in self.points:
            res += point.to_bytes()

        return res

    @staticmethod
    def from_bytes(source: bytes|bytearray) -> "PointSet":
        """Permet de convertir des bytes en PointSet.

        Args:
            source (bytes | bytearray): Les bytes à convertir.

        Raises:
            TypeError: Si le source n'est pas de type bytes ou bytearray.
            ValueError: Si le source n'est pas valide.

        Returns:
            PointSet: L'ensemble de points converti.
        
        """
        if type(source) is not bytes and type(source) is not bytearray:
            raise TypeError
        if len(source) < 4:
            raise ValueError
        
        try:
            nb_points = struct.unpack("<L", source[:4])[0]
        except Exception as err:
            raise ValueError from err
        
        excepted_len = 4 + nb_points * 8
        if len(source) != excepted_len:
            raise ValueError
        
        points = []
        for i in range(4, excepted_len, 8):
            points.append(Point.from_bytes(source[i:i+8]))

        return PointSet(points)
