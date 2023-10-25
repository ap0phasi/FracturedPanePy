import plotly.graph_objects as go
import numpy as np

import colorsys

def darken_rgb(rgb, factor=0.85):  # Factor determines how much to darken. 0.85 means 15% darker.
    # Convert RGB to HSV
    r, g, b = [x/255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    
    # Darken the value
    v = max(0, v * factor)
    
    # Convert back to RGB
    return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))

def binary_to_hsv(binary_encoding):
    depth = len(binary_encoding)
    total_splits = 2**depth
    current_position = int(binary_encoding, 2) if binary_encoding else 0
    hue = (360 / total_splits) * current_position
    
    saturation = 1.0  # Maximum vividness
    
    base_value = 0.8
    min_value = 0.3
    value = max(base_value * (0.95 ** depth), min_value)  # Adjust the multiplier based on the desired decrement.
    
    # Convert to [0,1] range
    hue /= 360.0
    
    return hue, saturation, value

def binary_to_rgb(binary_encoding):
    h, s, v = binary_to_hsv(binary_encoding)
    return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))

def plot_polygons(polygons, show_unnamed = False):
    """Visualize polygons with color encoding and hover information."""
    
    fig = go.Figure()
    
    for poly in polygons:
        
        if not show_unnamed and (poly['concept'] == "" and not poly['encoding'] == ''):
            continue
        
        encoding = poly['encoding']
        
 
        fill_color = 'rgb' + str(binary_to_rgb(encoding[::-1]))
        line_color = 'rgb' + str(darken_rgb(binary_to_rgb(encoding[::-1])))
        
        text = f"Concept: {poly['concept']}<br>Encoding: {encoding}"

        fig.add_trace(go.Scatter(x=np.array(poly['polygon'])[:, 0],
                                 y=np.array(poly['polygon'])[:, 1],
                                 fill='toself',
                                 fillcolor=fill_color,
                                 hoverinfo='text',
                                 hoveron='fills',
                                 text=text,
                                 name=text,
                                 line_shape='linear',
                                 mode='lines',
                                 line=dict(color=line_color),
                                 opacity=1))
    
    fig.update_layout(showlegend=True, xaxis_visible=False, yaxis_visible=False, plot_bgcolor='rgba(0,0,0,0)')
    fig.show()

if __name__ == "__main__":
    for encoding in ["", "0", "1", "00", "01", "10", "11", "010", "011"]:
        print(f"{encoding}: {binary_to_rgb(encoding)}")
