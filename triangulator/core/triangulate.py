"""Module contenant la classe Triangulator."""

from pointset_manager.models.PointSet import PointSet
from triangulator.models.Triangle import Triangle
from triangulator.models.Triangles import Triangles


class Triangulator:
    """Classe Triangulator."""
    
    @staticmethod
    def triangulate(pointset: PointSet) -> Triangles:
        """Permet de calculer la triangulation en utilisant l'algorithme de Delaunay.

        Args:
            pointset (PointSet): Le pointset à trianguler.

        Raises:
            ValueError: Si le pointset contient moins de 3 points.
            ValueError: Si les points sont colinéaires.

        Returns:
            Triangles: La triangulation du pointset.

        """
        if len(pointset) < 3:
            raise ValueError
        
        points = [(p.x, p.y) for p in pointset.points]
        
        if Triangulator._are_points_collinear(points):
            raise ValueError
        
        triangles_indices = Triangulator._delaunay_triangulation(points)
        triangles = [Triangle(tuple(tri)) for tri in triangles_indices]
        
        return Triangles(triangles, pointset)


    @staticmethod
    def _are_points_collinear(points: list[tuple[float, float]]) -> bool:
        if len(points) < 3:
            return True
        (x1, y1), (x2, y2), (x3, y3) = points[0], points[1], points[2]
        area = x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)
        if area != 0:
            return False
        for i in range(3, len(points)):
            xi, yi = points[i]
            if (yi - y1)*(x2 - x1) != (y2 - y1)*(xi - x1):
                return False
        return True

    @staticmethod
    def _delaunay_triangulation(points: list[tuple[float, float]]) -> list[list[int]]:
        if len(points) < 3:
            return []
        if len(points) == 3:
            return [[0, 1, 2]]

        super_triangle = Triangulator._create_super_triangle(points)
        extended_points = points + super_triangle
        triangles = [(len(points), len(points)+1, len(points)+2)]

        for i, p in enumerate(points):
            bad_triangles = []
            for tri in triangles:
                if Triangulator._point_in_circumcircle(p, tri, extended_points):
                    bad_triangles.append(tri)
            
            polygon = []
            for tri in bad_triangles:
                for edge in Triangulator._triangle_edges(tri):
                    if not Triangulator._edge_shared_by_triangles(edge, bad_triangles):
                        polygon.append(edge)

            # Supprimer triangles mauvais
            triangles = [t for t in triangles if t not in bad_triangles]

            # Ajouter triangles avec le point courant
            for edge in polygon:
                triangles.append((edge[0], edge[1], i))

        # Supprimer triangles contenant les sommets du super-triangle
        final_triangles = []
        for tri in triangles:
            if all(v < len(points) for v in tri):
                final_triangles.append(list(tri))

        return final_triangles

    @staticmethod
    def _create_super_triangle(
            points: list[tuple[float, float]]) -> list[tuple[float, float]]:
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        dx = max_x - min_x
        dy = max_y - min_y
        max_dim = max(dx, dy)
        mid_x = (min_x + max_x)/2
        mid_y = (min_y + max_y)/2
        return [
            (mid_x - 2*max_dim, mid_y - max_dim),
            (mid_x, mid_y + 2*max_dim),
            (mid_x + 2*max_dim, mid_y - max_dim)
        ]

    @staticmethod
    def _point_in_circumcircle(
            point: tuple[float, float], triangle: tuple[int, int, int], 
            points: list[tuple[float, float]]) -> bool:
        p1 = points[triangle[0]]
        p2 = points[triangle[1]]
        p3 = points[triangle[2]]
        ax, ay = p1
        bx, by = p2
        cx, cy = p3
        px, py = point

        d = 2*(ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))
        if abs(d) < 1e-12:
            return False

        ux = ((ax**2 + ay**2) * (by - cy) +
              (bx**2 + by**2) * (cy - ay) +
              (cx**2 + cy**2) * (ay - by)) / d
        uy = ((ax**2 + ay**2) * (cx - bx) +
              (bx**2 + by**2) * (ax - cx) +
              (cx**2 + cy**2) * (bx - ax)) / d

        r2 = (ax - ux)**2 + (ay - uy)**2
        dist2 = (px - ux)**2 + (py - uy)**2

        return dist2 <= r2 + 1e-12

    @staticmethod
    def _triangle_edges(tri: tuple[int, int, int]) -> list[tuple[int, int]]:
        return [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]

    @staticmethod
    def _edge_shared_by_triangles(
            edge: tuple[int, int],
            triangles: list[tuple[int, int, int]]
    ) -> bool:
        count = 0
        for tri in triangles:
            edges = Triangulator._triangle_edges(tri)
            if edge in edges or (edge[1], edge[0]) in edges:
                count += 1
                if count > 1:
                    return True
        return False
