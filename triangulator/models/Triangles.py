"""Module contenant la classe Triangles."""

import struct

from pointset_manager.models.PointSet import PointSet
from triangulator.models.Triangle import Triangle


class Triangles:
    """Classe représentant un ensemble de triangles."""

    def __init__(self, list_of_triangle: list, pointset: PointSet):
        """Permet de créer un ensemble de triangles.

        Args:
            list_of_triangle (list): La liste des triangles.
            pointset (PointSet): Le pointset associé au triangle.

        Raises:
            TypeError: Si le pointset n'est pas un PointSet

        """
        if type(pointset) is not PointSet:
            raise TypeError
        
        self.triangles: list = list_of_triangle
        self.ps: PointSet = pointset
    
    def __len__(self) -> int:
        """Permet de retourner le nombre de triangles."""
        return len(self.triangles)
    
    def add_triangles(self, triangle: Triangle) -> None:
        """Permet d'ajouter un triangle à l'ensemble.

        Args:
            triangle (Triangle): Le triangle à ajouter.

        Raises:
            TypeError: Si le triangle n'est pas de type Triangle.

        """
        if type(triangle) is not Triangle:
            raise TypeError
        
        self.triangles.append(triangle)

    def to_bytes(self) -> str:
        """Permet de convertir l'ensemble de triangles en bytes.

        Raises:
            ValueError: Si l'ensemble de triangles est vide.

        Returns:
            str: La représentation en bytes de l'ensemble de triangles.

        """
        if len(self.triangles) <= 0:
            raise ValueError

        res = self.ps.to_bytes()
        res += struct.pack("<L", len(self.triangles))
        
        for t in self.triangles:
            res += t.to_bytes()

        return res
    
    @staticmethod
    def from_bytes(source: bytes|bytearray) -> "Triangles":
        """Permet de convertir des bytes en Triangles.

        Args:
            source (bytes | bytearray): Les bytes à convertir.

        Raises:
            TypeError: Si le source n'est pas de type bytes ou bytearray.
            ValueError: Si le source n'est pas valide.

        Returns:
            Triangles: L'ensemble de triangles converti.

        """
        if type(source) is not bytes and type(source) is not bytearray:
            raise TypeError
        
        try:
            ps_nb_points = struct.unpack("<L", source[:4])[0]
        except Exception as err:
            raise ValueError from err
        
        ps_len = 4 + ps_nb_points * 8
        ps = PointSet.from_bytes(source[:ps_len])

        try:
            nb_triangles = struct.unpack("<L", source[ps_len:ps_len+4])[0]
        except Exception as err:
            raise ValueError from err
        
        expected_len = ps_len + 4 + nb_triangles * 12
        if len(source) != expected_len:
            raise ValueError

        triangles = []
        for i in range(ps_len + 4, expected_len, 12):
            triangles.append(Triangle.from_bytes(source[i:i+12], ps))
        
        return Triangles(triangles, ps)
