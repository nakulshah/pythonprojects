import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
import random

# --- Geometry Helpers ---

def side_lengths(points):
    """Returns the lengths of the sides of a polygon defined by points."""
    diffs = np.diff(np.vstack([points, points[0]]), axis=0)
    return np.linalg.norm(diffs, axis=1)

def interior_angles(points):
    """Returns the interior angles (in degrees) of a polygon defined by points."""
    angles = []
    n = len(points)
    for i in range(n):
        p0, p1, p2 = points[i - 1], points[i], points[(i + 1) % n]
        v1, v2 = p0 - p1, p2 - p1
        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)
        angle = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
        angles.append(np.rad2deg(angle))
    return np.array(angles)

# --- Shape Generators with Constraints ---

def generate_random_triangle(max_size=1.5, min_side=0.3, min_angle=30):
    while True:
        pts = np.random.rand(3, 2) * max_size
        area = 0.5 * abs(np.cross(pts[1] - pts[0], pts[2] - pts[0]))
        if area < 0.01:
            continue
        if (side_lengths(pts) >= min_side).all() and (interior_angles(pts) >= min_angle).all():
            return pts

def generate_random_quadrilateral(max_size=1.5, min_side=0.3, min_angle=30):
    while True:
        pts = np.random.rand(4, 2) * max_size
        poly = Polygon(pts)
        if poly.is_valid and poly.area >= 0.01:
            coords = np.array(poly.exterior.coords)[:-1]
            if (side_lengths(coords) >= min_side).all() and (interior_angles(coords) >= min_angle).all():
                return coords

def generate_random_polygon(min_vertices=5, max_vertices=7, max_size=1.5, min_side=0.1, min_angle=15):
    while True:
        n = np.random.randint(min_vertices, max_vertices + 1)
        points = np.random.rand(n, 2) * max_size
        poly = Polygon(points)

        if not poly.is_valid or poly.area < 0.01:
            continue

        pts = np.array(poly.exterior.coords)[:-1]
        lengths = side_lengths(pts)
        angles = interior_angles(pts)

        if (lengths >= min_side).all() and (angles >= min_angle).all():
            return pts

# --- Placement Helpers ---

def place_shape_randomly(shape, square_size=2.0):
    min_xy, max_xy = shape.min(axis=0), shape.max(axis=0)
    tx = np.random.uniform(0 - min_xy[0], square_size - max_xy[0])
    ty = np.random.uniform(0 - min_xy[1], square_size - max_xy[1])
    return shape + np.array([tx, ty])

def rotate_and_place(shape, angle_deg, square_size=2.0):
    angle_rad = np.deg2rad(angle_deg)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                [np.sin(angle_rad),  np.cos(angle_rad)]])
    center = shape.mean(axis=0)
    rotated = (shape - center) @ rotation_matrix.T + center
    min_xy, max_xy = rotated.min(axis=0), rotated.max(axis=0)
    if np.any((max_xy - min_xy) > square_size):
        raise ValueError("Shape too large after rotation.")
    tx = np.random.uniform(0 - min_xy[0], square_size - max_xy[0])
    ty = np.random.uniform(0 - min_xy[1], square_size - max_xy[1])
    return rotated + np.array([tx, ty])

# --- Plotting Helpers ---

def draw_shape(ax, shape, color='black', ref_point=None):
    ax.scatter(shape[:, 0], shape[:, 1], color=color, s=20)
    if ref_point is not None:
        ax.scatter(ref_point[0], ref_point[1], color='cyan', s=30, marker='*')

def draw_box(ax):
    ax.add_patch(plt.Rectangle((0, 0), 2, 2, edgecolor='black', facecolor='none'))

def setup_ax(ax):
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    ax.axis('off')

# --- Generate Base Shapes ---

triangle = generate_random_triangle()
quadrilateral = generate_random_quadrilateral()
polygon = generate_random_polygon()
polygon_ref = polygon.mean(axis=0)

# --- Setup Figure ---

fig, axs = plt.subplots(3, 4, figsize=(12, 9))
axs = axs.flatten()

# --- Subplot 0: outlines + vertices + ref point ---

tri0 = place_shape_randomly(triangle)
quad0 = place_shape_randomly(quadrilateral)
poly0 = place_shape_randomly(polygon)
ref0 = polygon_ref + (poly0.mean(axis=0) - polygon.mean(axis=0))  # adjusted

axs[0].plot(*np.vstack([tri0, tri0[0]]).T, color='red')
axs[0].scatter(tri0[:, 0], tri0[:, 1], color='red', s=20)
axs[0].plot(*np.vstack([quad0, quad0[0]]).T, color='blue')
axs[0].scatter(quad0[:, 0], quad0[:, 1], color='blue', s=20)
axs[0].plot(*np.vstack([poly0, poly0[0]]).T, color='green')
axs[0].scatter(poly0[:, 0], poly0[:, 1], color='green', s=20)
axs[0].scatter(ref0[0], ref0[1], color='cyan', s=30, marker='x')
draw_box(axs[0])
setup_ax(axs[0])

# --- Subplots 1 to 11 ---
for i in range(1, 12):
    if i >= 4:
        tri = rotate_and_place(triangle, random.uniform(0, 360))
        quad = rotate_and_place(quadrilateral, random.uniform(0, 360))
        poly = rotate_and_place(polygon, random.uniform(0, 360))
        ref = poly.mean(axis=0)
    else:
        tri = place_shape_randomly(triangle)
        quad = place_shape_randomly(quadrilateral)
        poly = place_shape_randomly(polygon)
        ref = poly.mean(axis=0)

    color = 'black' if i >= 8 else None
    draw_box(axs[i])
    draw_shape(axs[i], tri, color or 'red')
    draw_shape(axs[i], quad, color or 'blue')
    draw_shape(axs[i], poly, color or 'green', ref_point=ref)
    setup_ax(axs[i])

plt.tight_layout()
plt.savefig("shapes.pdf", format='pdf', bbox_inches='tight')
plt.show()