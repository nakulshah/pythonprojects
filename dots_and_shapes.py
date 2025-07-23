import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
import random

# --- Geometry helpers ---

def side_lengths(points):
    diffs = np.diff(np.vstack([points, points[0]]), axis=0)
    lengths = np.linalg.norm(diffs, axis=1)
    return lengths

def interior_angles(points):
    angles = []
    n = len(points)
    for i in range(n):
        p0 = points[i - 1]
        p1 = points[i]
        p2 = points[(i + 1) % n]

        v1 = p0 - p1
        v2 = p2 - p1

        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)

        angle = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
        angles.append(np.rad2deg(angle))
    return np.array(angles)

# --- Shape generators with constraints ---

def generate_random_triangle(max_size=1.5, min_side=0.3, min_angle=30):
    while True:
        points = np.random.rand(3, 2) * max_size

        area = 0.5 * abs(
            points[0,0]*(points[1,1]-points[2,1]) +
            points[1,0]*(points[2,1]-points[0,1]) +
            points[2,0]*(points[0,1]-points[1,1])
        )
        if area < 0.01:
            continue

        lengths = side_lengths(points)
        angles = interior_angles(points)

        if (lengths >= min_side).all() and (angles >= min_angle).all():
            return points

def generate_random_quadrilateral(max_size=1.5, min_side=0.3, min_angle=30):
    while True:
        points = np.random.rand(4, 2) * max_size
        poly = Polygon(points)
        if not poly.is_valid or poly.area < 0.01:
            continue

        pts = np.array(poly.exterior.coords)[:-1]
        lengths = side_lengths(pts)
        angles = interior_angles(pts)

        if (lengths >= min_side).all() and (angles >= min_angle).all():
            return pts

def generate_random_polygon(min_vertices=5, max_vertices=8, max_size=1.5, min_side=0.1, min_angle=5):
    while True:
        n = np.random.randint(min_vertices, max_vertices + 1)
        points = np.random.rand(n, 2) * max_size
        poly = Polygon(points).convex_hull
        if not poly.is_valid or poly.area < 0.01:
            continue
        pts = np.array(poly.exterior.coords)[:-1]

        lengths = side_lengths(pts)
        angles = interior_angles(pts)

        if (lengths >= min_side).all() and (angles >= min_angle).all():
            return pts

# --- Placement and rotation helpers ---

def place_shape_randomly(shape, ref_point=None, square_size=2.0):
    min_x, min_y = shape.min(axis=0)
    max_x, max_y = shape.max(axis=0)
    tx = np.random.uniform(0 - min_x, square_size - max_x)
    ty = np.random.uniform(0 - min_y, square_size - max_y)
    transformed_shape = shape + np.array([tx, ty])
    if ref_point is not None:
        transformed_ref = ref_point + np.array([tx, ty])
        return transformed_shape, transformed_ref
    return transformed_shape, None

def place_rotated_shape_randomly(shape, angle_deg, ref_point=None, square_size=2.0):
    angle_rad = np.deg2rad(angle_deg)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    centroid = shape.mean(axis=0)
    rotated_shape = (shape - centroid) @ rotation_matrix.T + centroid
    rotated_ref = None
    if ref_point is not None:
        rotated_ref = (ref_point - centroid) @ rotation_matrix.T + centroid

    min_x, min_y = rotated_shape.min(axis=0)
    max_x, max_y = rotated_shape.max(axis=0)
    if max_x - min_x > square_size or max_y - min_y > square_size:
        raise ValueError("Rotated shape too big to fit in box.")
    tx = np.random.uniform(0 - min_x, square_size - max_x)
    ty = np.random.uniform(0 - min_y, square_size - max_y)
    return rotated_shape + np.array([tx, ty]), rotated_ref + np.array([tx, ty]) if rotated_ref is not None else None

# --- Generate base shapes ---
triangle_base = generate_random_triangle()
square_base = generate_random_quadrilateral()
polygon_base = generate_random_polygon()

# --- Compute polygon reference point ---
polygon_ref = polygon_base.mean(axis=0)

# --- Setup figure and axes ---
fig, axs = plt.subplots(3, 4, figsize=(12, 9))
axs = axs.flatten()

# --- Subplot 0: outlines + vertices + reference point ---
triangle1, _ = place_shape_randomly(triangle_base)
square1, _ = place_shape_randomly(square_base)
polygon1, polyref1 = place_shape_randomly(polygon_base, polygon_ref)

axs[0].add_patch(plt.Rectangle((0, 0), 2, 2, edgecolor='black', facecolor='none'))
axs[0].plot(*np.vstack([triangle1, triangle1[0]]).T, color='red', linewidth=1)
axs[0].scatter(triangle1[:, 0], triangle1[:, 1], color='red', s=20)
axs[0].plot(*np.vstack([square1, square1[0]]).T, color='blue', linewidth=1)
axs[0].scatter(square1[:, 0], square1[:, 1], color='blue', s=20)
axs[0].plot(*np.vstack([polygon1, polygon1[0]]).T, color='green', linewidth=1)
axs[0].scatter(polygon1[:, 0], polygon1[:, 1], color='green', s=20)
axs[0].scatter(polyref1[0], polyref1[1], color='cyan', s=30, marker='x')

axs[0].set_xlim(0, 2)
axs[0].set_ylim(0, 2)
axs[0].set_aspect('equal')
axs[0].axis('off')

# --- Subplots 1 to 11 ---
for i in range(1, 12):
    if i >= 4:
        angle_tri = random.uniform(0, 360)
        angle_sqr = random.uniform(0, 360)
        angle_poly = random.uniform(0, 360)
        tri, _ = place_rotated_shape_randomly(triangle_base, angle_tri)
        sqr, _ = place_rotated_shape_randomly(square_base, angle_sqr)
        poly, polyref = place_rotated_shape_randomly(polygon_base, angle_poly, polygon_ref)
    else:
        tri, _ = place_shape_randomly(triangle_base)
        sqr, _ = place_shape_randomly(square_base)
        poly, polyref = place_shape_randomly(polygon_base, polygon_ref)

    axs[i].add_patch(plt.Rectangle((0, 0), 2, 2, edgecolor='black', facecolor='none'))

    if i >= 8:
        axs[i].scatter(tri[:, 0], tri[:, 1], color='black', s=20)
        axs[i].scatter(sqr[:, 0], sqr[:, 1], color='black', s=20)
        axs[i].scatter(poly[:, 0], poly[:, 1], color='black', s=20)
    else:
        axs[i].scatter(tri[:, 0], tri[:, 1], color='red', s=20)
        axs[i].scatter(sqr[:, 0], sqr[:, 1], color='blue', s=20)
        axs[i].scatter(poly[:, 0], poly[:, 1], color='green', s=20)

    # Draw polygon reference point
    axs[i].scatter(polyref[0], polyref[1], color='cyan', s=30, marker='x')

    axs[i].set_xlim(0, 2)
    axs[i].set_ylim(0, 2)
    axs[i].set_aspect('equal')
    axs[i].axis('off')

plt.tight_layout()
plt.savefig("shapes.pdf", format='pdf', bbox_inches='tight')
plt.show()