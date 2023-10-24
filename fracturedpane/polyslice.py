from shapely.geometry import LineString, MultiPolygon, Polygon, Point
from shapely.ops import polygonize
import matplotlib.pyplot as plt
import math

def plot_polygon(coords, color='-b', fill_color=None):
    xs, ys = zip(*coords)  # Unzip coordinates
    plt.plot(xs, ys, color)
    if fill_color:
        plt.fill(xs, ys, fill_color)

def slice_polys(poly_coords, fresh_cut, angle, location):
    """
    Slices a polygon based on the provided parameters and returns the resulting polygons and slice intersection.
    
    Parameters:
    - poly_coords (list of tuple): List of 2D coordinates representing the input polygon.
    - fresh_cut (list of tuple): Two 2D coordinates on the `poly_coords` indicating the side of the polygon to slice through.
    - angle (float): Angle of the desired slice in degrees.
    - location (float): A value between 0 and 1 indicating how far along the `fresh_cut` to start the slice.
    
    Returns:
    - keep_polys (list of Polygon): List of resultant Polygon objects after the slice.
    - slice_intersect (list of tuple): 2D coordinates of the slice intersection on the original polygon.
    """
    
    # Convert input to Shapely's Polygon and LineString
    poly = Polygon(poly_coords)
    
    # Calculate the starting point of the slice based on the location
    base_x = fresh_cut[0][0] + location * (fresh_cut[1][0] - fresh_cut[0][0])
    base_y = fresh_cut[0][1] + location * (fresh_cut[1][1] - fresh_cut[0][1])

    # Compute bounding box diagonal
    minx, miny, maxx, maxy = poly.bounds
    diagonal = math.sqrt((maxx - minx)**2 + (maxy - miny)**2)
    
    # Calculate start and end points for the slicing line using the bounding box diagonal
    end_x = base_x - diagonal * 10 * math.cos(math.radians(angle))
    end_y = base_y - diagonal * 10 * math.sin(math.radians(angle))
    start_x = base_x + diagonal * 10 * math.cos(math.radians(angle))
    start_y = base_y + diagonal * 10 * math.sin(math.radians(angle))

    slice_line = LineString([(start_x, start_y), (end_x, end_y)])
    slice_intersect = list(poly.intersection(slice_line).coords)
    
    # Union the exterior lines of the polygon with the slicing line
    unioned = poly.boundary.union(slice_line)
    
    # Use polygonize to split and filter out polygons outside of the original polygon
    keep_polys = [p for p in polygonize(unioned) if p.representative_point().within(poly)]
    return keep_polys, slice_intersect

def make_slice(poly_coords, fresh_cut, angle, location):
    """
    Uses the `slice_polys` function to slice a polygon and then extracts and returns the coordinates of the sliced polygons.
    
    Parameters:
    - poly_coords (list of tuple): List of 2D coordinates representing the input polygon.
    - fresh_cut (list of tuple): Two 2D coordinates on the `poly_coords` indicating the side of the polygon to slice through.
    - angle (float): Angle of the desired slice in degrees.
    - location (float): A value between 0 and 1 indicating how far along the `fresh_cut` to start the slice.
    
    Returns:
    - slice1_coords (list of tuple): Coordinates of the first sliced polygon.
    - slice2_coords (list of tuple): Coordinates of the second sliced polygon.
    - slice_intersect (list of tuple): 2D coordinates of the slice intersection on the original polygon.
    """
    keep_polys, slice_intersect = slice_polys(poly_coords, fresh_cut, angle, location)
    # Extract coordinates from the new polygons
    slice1_coords = list(keep_polys[0].exterior.coords)
    slice2_coords = list(keep_polys[1].exterior.coords)
    
    # Return new polygons and the new fresh cut
    return slice1_coords, slice2_coords, slice_intersect

if __name__ == "__main__":
   # Initiate the original polygon and the first slice parameters
    # Starting with a simple square, we are choosing the bottom edge as our first 'fresh_cut'
    # The first slice will be made at an angle of 90 degrees, 65% along the bottom edge.
    poly_coords = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    fresh_cut = [(0,0), (10,0)]
    angle = 90
    location = 0.65

    # Perform the first slice and plot the resulting polygons
    new_polys = make_slice(poly_coords, fresh_cut, angle, location)
    plot_polygon(new_polys[0], color='-b', fill_color='lightblue')
    plot_polygon(new_polys[1], color='-b', fill_color='lightyellow')

    # For the next slice, we'll take the first of the newly created polygons
    # We'll slice it at a 45-degree angle, halfway along the previous slicing edge
    poly_coords = new_polys[0]
    fresh_cut = new_polys[2]
    angle = 45
    location = 0.50

    new_polys = make_slice(poly_coords, fresh_cut, angle, location)
    plot_polygon(new_polys[0], color='-b', fill_color='lightblue')
    plot_polygon(new_polys[1], color='-b', fill_color='lightgreen')

    # Taking the first polygon from the previous slice, we'll make another slice
    # This time, it'll be at a 135-degree angle, 25% along the previously sliced edge
    poly_coords = new_polys[0]
    fresh_cut = new_polys[2]
    angle = 135
    location = 0.25

    new_polys = make_slice(poly_coords, fresh_cut, angle, location)
    plot_polygon(new_polys[0], color='-b', fill_color='lightblue')
    plot_polygon(new_polys[1], color='-b', fill_color='red')

    # Show the plotted polygons
    plt.show()