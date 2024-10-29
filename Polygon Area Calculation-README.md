Polygon Area Calculation

Project Overview

This project demonstrates and compares different methods to calculate the area of polygons using three techniques:

Shapely Library Method:

A fast and reliable area calculation using the Shapely Python library.

Gauss (Shoelace) Formula: A mathematical formula to compute the area based on the vertices of the polygon.

Monte Carlo Method: A statistical approach that estimates the area by sampling random points inside a bounding box.

The goal is to explore the accuracy, execution time, and performance of these methods for polygons with varying numbers of vertices. We also investigate how the number of Monte Carlo iterations influences the error rate. 

Project Files

main.py:

 Contains the complete code for generating polygons, area calculation using three methods, benchmarking, plotting results, and saving them to a CSV file.
polygon_benchmark_results.csv: A table of results generated from running the code with different polygons.

README.md: This documentation explaining the project, methods, results, and insights.

Project Dependencies

Before running the code, install the required libraries using: 

pip install numpy pandas shapely matplotlib

Formulas and Concepts Used

1. Shapely Library Area Calculation

Shapely’s built-in method calculates the polygon’s area efficiently using robust algorithms.

area = polygon.area

2. Gauss (Shoelace) Formula

This method computes the area by multiplying the vertices' coordinates following the Shoelace pattern.

def polygon_area(coords):
    n = len(coords)
    area = 0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

3. Monte Carlo Method

This method estimates the area by randomly generating points inside the polygon’s bounding box. The proportion of points that land inside the polygon is used to estimate its area.
    
    def monte_carlo_area(polygon, num_points=10000):
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

What We Did ?

Polygon Generation: We created polygons with varying numbers of vertices (10, 50, 100) using a circular distribution pattern.
Area Calculation: We calculated the polygon area using:
Shapely’s built-in method
Gauss formula
Monte Carlo estimation with adaptive iterations to control error rates
Benchmarking Execution Time: We measured and compared the execution time of the three methods.
Monte Carlo Error Analysis: We adjusted the number of iterations dynamically until the error was below 1%.
Results Visualization: We plotted the execution time vs. vertices and error vs. iterations to understand the performance and accuracy.
Saving Results: All benchmark results were saved to a CSV file for easy reference.

Results and Insights

Accuracy Comparison:

The Shapely method provided the most accurate and fastest results.

The Gauss formula was very accurate but required custom implementation and careful handling of vertices.

The Monte Carlo method achieved reasonable accuracy, but it required more iterations for complex polygons to reach an error below 1%.
Execution Time Analysis:

The Shapely method was the fastest, followed by the Gauss formula.

The Monte Carlo method was slower, especially when more iterations were required to reduce the error margin.

Monte Carlo Iteration Control:

We dynamically adjusted the iterations to achieve an error rate of less than 1%.
As expected, the error decreased with more iterations, but this also increased the computation time.

Conclusion

In this project, we learned:

How to generate polygons programmatically and calculate their area using different methods.
The importance of benchmarking and comparing algorithms in terms of accuracy and speed.
How Monte Carlo methods work and the trade-off between accuracy and computation time.
How to visualize results using graphs for better insight into the performance of different algorithms.

Usage Instructions

Run the Code: Execute the main.py script to generate polygons, benchmark the area calculations, and visualize the results.

View Results: Check the polygon_benchmark_results.csv file for detailed results of the benchmarks.

Modify Parameters: Adjust the vertices_list or num_points to experiment with different polygons and Monte Carlo iterations.