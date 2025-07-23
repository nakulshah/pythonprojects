import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
import random

def generate_equilateral_triangle(side_length=0.5):
    angles = np.deg2rad([0, 120, 240])
    x = side_length * np.cos(angles)
    y = side_length * np.sin(angles)
    return np.vstack((x, y)).T

def generate_square_points(side_length):
    return np.array([
        [0, 0],
        [side_length, 0],
        [side_length, side_length],
        [0, side_length]
    ])

def place_shape_randomly(shape, square_size=2.0):
    min_x, min_y = shape.min(axis=0)
    max_x, max_y = shape.max(axis=0)
    tx = np.random.uniform(0 - min_x, square_size - max_x)
    ty = np.random.uniform(0 - min_y, square_size - max_y)
    return shape + np.array([tx, ty])

def shapes_intersect(polygon1_pts, polygon2_pts):
    poly1 = Polygon(polygon1_pts)
    poly2 = Polygon(polygon2_pts)
    return poly1.intersects(poly2)

def place_shapes_with_intersection(triangle_base, square_base, square_size=2.0, max_attempts=500):
    for _ in range(max_attempts):
        tri = place_shape_randomly(triangle_base, square_size)
        sqr = place_shape_randomly(square_base, square_size)
        if shapes_intersect(tri, sqr):
            return tri, sqr
    raise RuntimeError("Could not place triangle and square with intersection after many attempts.")

def generate_random_triangle(max_size=1.5):
    while True:
        points = np.random.rand(3, 2) * max_size
        # Calculate signed area using shoelace formula
        x, y = points[:, 0], points[:, 1]
        area = 0.5 * abs(x[0]*(y[1] - y[2]) + x[1]*(y[2] - y[0]) + x[2]*(y[0] - y[1]))
        if area > 0.01:
            return points

def generate_random_quadrilateral(max_size=1.5):
    while True:
        points = np.random.rand(4, 2) * max_size
        poly = Polygon(points)
        if poly.is_valid and poly.area > 0.01:
            return np.array(poly.exterior.coords)[:-1]


def rotate_shape(shape, angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    centroid = shape.mean(axis=0)
    rotated = (shape - centroid) @ rotation_matrix.T + centroid
    return rotated

def place_rotated_shape_randomly(shape, angle_deg, square_size=2.0):
    rotated = rotate_shape(shape, angle_deg)
    min_x, min_y = rotated.min(axis=0)
    max_x, max_y = rotated.max(axis=0)

    if max_x - min_x > square_size or max_y - min_y > square_size:
        raise ValueError("Rotated shape too big to fit in box.")

    tx = np.random.uniform(0 - min_x, square_size - max_x)
    ty = np.random.uniform(0 - min_y, square_size - max_y)

    return rotated + np.array([tx, ty])

# --- Plotting ---
fig, axs = plt.subplots(3, 4, figsize=(12, 9))
axs = axs.flatten()  # flatten for easy indexing

# Generate base shapes with random sizes
triangle_base = generate_random_triangle(max_size=1.5)
square_base = generate_random_quadrilateral(max_size=2)

# Subplot 1 (index 0): outlines + vertices
triangle1 = place_shape_randomly(triangle_base)
square1 = place_shape_randomly(square_base)

axs[0].add_patch(plt.Rectangle((0, 0), 2, 2, edgecolor='black', facecolor='none'))
axs[0].plot(*np.vstack([triangle1, triangle1[0]]).T, color='black', linewidth=1)
axs[0].scatter(triangle1[:, 0], triangle1[:, 1], color='red', s=20)
axs[0].plot(*np.vstack([square1, square1[0]]).T, color='black', linewidth=1)
axs[0].scatter(square1[:, 0], square1[:, 1], color='blue', s=20)
axs[0].set_xlim(0, 2)
axs[0].set_ylim(0, 2)
axs[0].set_aspect('equal')
axs[0].axis('off')

# Subplots 2 to 12 (indices 1 to 11)
for i in range(1, 12):
    if i >= 4:  # indices 4 to 11: rotated placement
        angle_tri = random.uniform(0, 360)
        angle_sqr = random.uniform(0, 360)
        tri = place_rotated_shape_randomly(triangle_base, angle_tri)
        sqr = place_rotated_shape_randomly(square_base, angle_sqr)
    else:  # indices 1 to 3: just placed, no rotation
        tri = place_shape_randomly(triangle_base)
        sqr = place_shape_randomly(square_base)

    axs[i].add_patch(plt.Rectangle((0, 0), 2, 2, edgecolor='black', facecolor='none'))

    if i >= 8:  # indices 8–11: black vertices
        axs[i].scatter(tri[:, 0], tri[:, 1], color='black', s=20)
        axs[i].scatter(sqr[:, 0], sqr[:, 1], color='black', s=20)
    else:  # colored vertices
        axs[i].scatter(tri[:, 0], tri[:, 1], color='red', s=20)
        axs[i].scatter(sqr[:, 0], sqr[:, 1], color='blue', s=20)

    axs[i].set_xlim(0, 2)
    axs[i].set_ylim(0, 2)
    axs[i].set_aspect('equal')
    axs[i].axis('off')

plt.tight_layout()
plt.savefig("shapes.pdf", format='pdf', bbox_inches='tight')
plt.show()

