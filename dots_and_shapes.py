import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
import random
from datetime import datetime

# --- Geometry Helpers ---

def side_lengths(points):
    diffs = np.diff(np.vstack([points, points[0]]), axis=0)
    return np.linalg.norm(diffs, axis=1)

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

# --- Shape Generators ---

def generate_random_triangle(max_size=1.5, min_side=0.3, min_angle=30):
    while True:
        points = np.random.rand(3, 2) * max_size
        v1 = points[1] - points[0]
        v2 = points[2] - points[0]
        area = 0.5 * abs(v1[0] * v2[1] - v1[1] * v2[0])
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

def generate_random_polygon(min_vertices=6, max_vertices=8, max_size=1.5, min_side=0.1, min_angle=15):
    while True:
        n = np.random.randint(min_vertices, max_vertices + 1)
        points = np.random.rand(n, 2) * max_size
        poly = Polygon(points)
        if not poly.is_valid or poly.area < 0.01:
            continue
        coords = np.array(poly.exterior.coords)[:-1]
        if len(coords) < min_vertices:
            continue
        lengths = side_lengths(coords)
        angles = interior_angles(coords)
        if (lengths >= min_side).all() and (angles >= min_angle).all():
            return coords

# --- Placement and Rotation Helpers ---

def place_shape_randomly(shape, square_size=2.0):
    min_x, min_y = shape.min(axis=0)
    max_x, max_y = shape.max(axis=0)
    tx = np.random.uniform(0 - min_x, square_size - max_x)
    ty = np.random.uniform(0 - min_y, square_size - max_y)
    return shape + np.array([tx, ty])

def rotate_shape(shape, angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    R = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                  [np.sin(angle_rad),  np.cos(angle_rad)]])
    center = shape.mean(axis=0)
    return (shape - center) @ R.T + center

def place_rotated_shape_randomly(shape, angle_deg, square_size=2.0):
    rotated = rotate_shape(shape, angle_deg)
    min_x, min_y = rotated.min(axis=0)
    max_x, max_y = rotated.max(axis=0)
    if max_x - min_x > square_size or max_y - min_y > square_size:
        raise ValueError("Rotated shape too big to fit")
    tx = np.random.uniform(0 - min_x, square_size - max_x)
    ty = np.random.uniform(0 - min_y, square_size - max_y)
    return rotated + np.array([tx, ty])

def compute_centroid(shape):
    poly = Polygon(shape)
    return np.array(poly.centroid.coords[0])

# --- Generate Base Shapes ---

triangle_base = generate_random_triangle()
square_base = generate_random_quadrilateral()
polygon_base = generate_random_polygon()

# --- Setup Plot ---

fig, axs = plt.subplots(3, 4, figsize=(12, 9))
axs = axs.flatten()

# --- Subplot 0: outlines + vertices + reference point ---

triangle0 = place_shape_randomly(triangle_base)
square0 = place_shape_randomly(square_base)
polygon0 = place_shape_randomly(polygon_base)
ref0 = compute_centroid(polygon0)

axs[0].add_patch(plt.Rectangle((0, 0), 2, 2, edgecolor='black', facecolor='none'))
axs[0].plot(*np.vstack([triangle0, triangle0[0]]).T, color='red')
axs[0].scatter(triangle0[:, 0], triangle0[:, 1], color='red', s=20)
axs[0].plot(*np.vstack([square0, square0[0]]).T, color='blue')
axs[0].scatter(square0[:, 0], square0[:, 1], color='blue', s=20)
axs[0].plot(*np.vstack([polygon0, polygon0[0]]).T, color='green')
axs[0].scatter(polygon0[:, 0], polygon0[:, 1], color='green', s=20)
axs[0].scatter(ref0[0], ref0[1], color='cyan', s=30, marker='*')
axs[0].set_xlim(0, 2)
axs[0].set_ylim(0, 2)
axs[0].set_aspect('equal')
axs[0].axis('off')

# --- Subplots 1–11 ---

for i in range(1, 12):
    if i >= 4:
        tri = place_rotated_shape_randomly(triangle_base, random.uniform(0, 360))
        sqr = place_rotated_shape_randomly(square_base, random.uniform(0, 360))
        poly = place_rotated_shape_randomly(polygon_base, random.uniform(0, 360))
    else:
        tri = place_shape_randomly(triangle_base)
        sqr = place_shape_randomly(square_base)
        poly = place_shape_randomly(polygon_base)

    ref = compute_centroid(poly)
    axs[i].add_patch(plt.Rectangle((0, 0), 2, 2, edgecolor='black', facecolor='none'))

    if i >= 8:
        axs[i].scatter(tri[:, 0], tri[:, 1], color='black', s=20)
        axs[i].scatter(sqr[:, 0], sqr[:, 1], color='black', s=20)
        axs[i].scatter(poly[:, 0], poly[:, 1], color='black', s=20)
    else:
        axs[i].scatter(tri[:, 0], tri[:, 1], color='red', s=20)
        axs[i].scatter(sqr[:, 0], sqr[:, 1], color='blue', s=20)
        axs[i].scatter(poly[:, 0], poly[:, 1], color='green', s=20)

    axs[i].scatter(ref[0], ref[1], color='cyan', s=30, marker='*')
    axs[i].set_xlim(0, 2)
    axs[i].set_ylim(0, 2)
    axs[i].set_aspect('equal')
    axs[i].axis('off')

# --- Finalize Plot ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"shapes_{timestamp}.pdf"
plt.tight_layout()
plt.savefig(filename, format='pdf', bbox_inches='tight')
plt.show()