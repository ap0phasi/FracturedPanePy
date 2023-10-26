import pandas as pd
from polygons.polyslice import make_slice
from polygons.polyplots import plotly_polygons
from ontology.diff_ont import generate_ontology_tree, prepare_belonging_df

import math
import random

def compute_angle(point1, point2):
    """
    Calculate the angle (in degrees) between two points using the arctangent function.
    """
    delta_y = point2[1] - point1[1]
    delta_x = point2[0] - point1[0]
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)
    
    # Ensure angle is between 0 and 360
    if angle_deg < 0:
        angle_deg += 360
    
    return angle_deg


def next_slicing_angle(fresh_cut):
    """
    Determine the next slicing angle based on the angle of the fresh cut.
    """
    angle_sequence = [90, 0, 45, 135]
    
    # Calculate the angle of the fresh cut
    current_angle = compute_angle(fresh_cut[0], fresh_cut[1])
    
    # Normalize the angle to the range [0, 180)
    current_angle = round((current_angle + 360) % 180)
    
    # Find the position of this angle in the sequence, and get the next angle
    index = angle_sequence.index(current_angle)
    next_index = (index + 1) % len(angle_sequence)
    return angle_sequence[next_index]

def slice_space(df):
    # Initialization
    bounding_rect = [(0,0), (10,0), (10,10), (0,10), (0,0)]
    polygons = [{'encoding': '', 'polygon': bounding_rect, 'concept': '', 'fresh_cut': [(0,0), (10,0)]}]

    angle = 90
    location = random.random() * 0.6 + 0.2
    # Slice the initial polygon
    candidate = ''
    new_poly_0, new_poly_1, new_fresh_cut = make_slice(polygons[0]['polygon'], polygons[0]['fresh_cut'], angle, location)
    name_of_candidate = df[df['encoding'].str[1:] == candidate]['concept'].values[0]
    polygons.append({'encoding': '0', 'polygon': new_poly_0, 'concept': '', 'fresh_cut': new_fresh_cut})
    polygons.append({'encoding': '1', 'polygon': new_poly_1, 'concept': name_of_candidate, 'fresh_cut': new_fresh_cut})

    candidates = ['1','0']
    
    # Traversal
    while candidates:
        print(candidates)
        candidate = candidates.pop(0)
        if not df[df['encoding'].str[1:] == candidate].empty:
            # Determine parent encoding, polygon, and fresh cut
            parent_encoding = candidate
            parent_data = [poly for poly in polygons if poly['encoding'] == parent_encoding][0]
            parent_polygon = parent_data['polygon']
            fresh_cut = parent_data['fresh_cut']
            
            # Determine slicing angle
            print(compute_angle(fresh_cut[0], fresh_cut[1]))
            angle = next_slicing_angle(fresh_cut)
            print(angle)
            location = random.random() * 0.6 + 0.2
            
            # Slice the polygon
            polygon_0, polygon_1, new_fresh_cut = make_slice(parent_polygon, fresh_cut, angle, location) 
            
            # Save polygons and update candidates
            name_of_candidate = df[df['encoding'].str[1:] == candidate]['concept'].values[0] if not df[df['encoding'].str[1:] == candidate].empty else ""
            polygons.append({'encoding': '0' + candidate, 'polygon': polygon_0, 'concept': '', 'fresh_cut': new_fresh_cut})
            polygons.append({'encoding': '1' + candidate, 'polygon': polygon_1, 'concept': name_of_candidate, 'fresh_cut': new_fresh_cut})
            candidates.extend(['1' + candidate, '0' + candidate])
    
    return polygons

if __name__ == "__main__":
    belongings = [
        {"parent": "Science", "concept": "Physics"},
        {"parent": "Physics", "concept": "Quantum Mechanics"},
        {"parent": "Physics", "concept": "Relativity"},
        {"parent": "Relativity", "concept": "General Relativity"},
        {'parent': "Art", "concept": "Watercolor"},
        {'parent': "Art", "concept": "Ceramics"},
        {'parent': "Watercolor", "concept": "Wet-On-Dry"},
        {'parent': "Watercolor", "concept": "Dry-On-Dry"}
        # ... you can add more belongings here
    ]
    
    # Convert belongings to DataFrame
    belongings_df = pd.DataFrame(belongings)
    
    belongings_df = prepare_belonging_df(belongings_df)

    df = generate_ontology_tree(belongings_df)
    print(df)
    resulting_polygons = slice_space(df)
    print(resulting_polygons)
    
    plotly_polygons(resulting_polygons)
