import random
import math
import time
import timeit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Polygon, Point

# --- Polygon Initialization ---
def generate_polygon(num_points, radius=10):
    """Generate a valid simple polygon without self-intersections."""
    points = [
        (
            math.cos(2 * math.pi * i / num_points) * random.uniform(0.8, 1) * radius,
            math.sin(2 * math.pi * i / num_points) * random.uniform(0.8, 1) * radius
        )
        for i in range(num_points)
    ]

    # Calculate centroid to sort points by angle
    centroid = (
        sum(x for x, y in points) / num_points,
        sum(y for x, y in points) / num_points
    )
    points = sorted(points, key=lambda p: math.atan2(p[1] - centroid[1], p[0] - centroid[0]))

    # Create and validate the polygon
    polygon = Polygon(points)
    if not polygon.is_valid or not polygon.is_simple:
        raise ValueError("Generated polygon is invalid or self-intersecting")

    return polygon

# --- Gauss (Shoelace) Method ---
def polygon_area(coords):
    """Calculate the polygon area using the Shoelace formula."""
    n = len(coords)
    area = 0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

# --- Monte Carlo Method ---
def monte_carlo_area(polygon, num_points=10000, max_iterations=1_000_000):
    """Estimate the polygon area using the Monte Carlo method."""
    min_x, min_y, max_x, max_y = polygon.bounds
    inside_count = 0

    for _ in range(num_points):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        point = Point(x, y)

        if polygon.contains(point):
            inside_count += 1

    box_area = (max_x - min_x) * (max_y - min_y)
    return box_area * (inside_count / num_points)

# --- Benchmarking and Error Investigation ---
def benchmark_methods(vertices_list):
    """Benchmark Shapely, Gauss, and Monte Carlo methods."""
    results = []

    for num_vertices in vertices_list:
        polygon = generate_polygon(num_vertices)
        coords = list(polygon.exterior.coords)

        # --- Shapely Method ---
        time_shapely = timeit.timeit(lambda: polygon.area, number=1)

        # --- Gauss Method ---
        time_gauss = timeit.timeit(lambda: polygon_area(coords), number=1)
        area_gauss = polygon_area(coords)

        # --- Monte Carlo Method with Iteration Control ---
        num_iterations = 10000
        max_iterations = 1_000_000  # Safety limit
        while True:
            area_mc = monte_carlo_area(polygon, num_points=num_iterations)
            error = abs((area_mc - polygon.area) / polygon.area)

            if error < 0.01 or num_iterations > max_iterations:
                break  # Stop when the error is acceptable or max iterations are reached
            num_iterations = int(num_iterations * 1.5)  # More efficient increase

        time_mc = timeit.timeit(lambda: monte_carlo_area(polygon, num_iterations), number=1)

        # Store results
        results.append({
            'num_vertices': num_vertices,
            'area_shapely': polygon.area,
            'area_gauss': area_gauss,
            'area_mc': area_mc,
            'error_mc': error,
            'time_shapely': time_shapely,
            'time_gauss': time_gauss,
            'time_mc': time_mc,
            'iterations_mc': num_iterations
        })

    return results

# --- Plotting Functions ---
def plot_execution_times(results):
    """Plot execution time vs number of vertices."""
    num_vertices = [result['num_vertices'] for result in results]
    time_shapely = [result['time_shapely'] for result in results]
    time_gauss = [result['time_gauss'] for result in results]
    time_mc = [result['time_mc'] for result in results]

    plt.figure(figsize=(12, 6))
    plt.plot(num_vertices, time_shapely, label='Shapely', marker='o')
    plt.plot(num_vertices, time_gauss, label='Gauss', marker='o')
    plt.plot(num_vertices, time_mc, label='Monte Carlo', marker='o')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs Number of Vertices')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_monte_carlo_iterations(results):
    """Plot error vs Monte Carlo iterations."""
    iterations = [result['iterations_mc'] for result in results]
    errors = [result['error_mc'] for result in results]

    plt.figure(figsize=(12, 6))
    plt.plot(iterations, errors, marker='o')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Monte Carlo Iterations')
    plt.ylabel('Error')
    plt.title('Error vs Monte Carlo Iterations')
    plt.grid(True)
    plt.show()

# --- Save Results to a Table ---
def save_results_to_csv(results, filename='polygon_benchmark_results.csv'):
    """Save the benchmark results to a CSV file."""
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f'Results saved to {filename}')

# --- Main Execution ---
vertices_list = [10, 50, 100]
results = benchmark_methods(vertices_list)

# Print Results as Table
df = pd.DataFrame(results)
print(df)

# Plot Results
plot_execution_times(results)
plot_monte_carlo_iterations(results)

# Save Results to CSV
save_results_to_csv(results)
