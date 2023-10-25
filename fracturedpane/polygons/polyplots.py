import plotly.graph_objects as go
import numpy as np

def plot_polygons(polygons):
    """Visualize polygons with color encoding and hover information."""

    # Base RGB color. This is just an example; you can choose a different base color.
    base_color = [100, 150, 200]
    
    fig = go.Figure()
    
    for poly in polygons:
        encoding = poly['encoding']
        r, g, b = base_color
        
        # Adjust colors based on the encoding.
        for bit in encoding[::-1]:
            if bit == '1':
                r = (r + 20) % 255
            elif bit == '0':
                g = (g - 30) % 255
        
        color = f'rgb({r},{g},{b})'
        
        text = f"Concept: {poly['concept']}<br>Encoding: {encoding}"

        fig.add_trace(go.Scatter(x=np.array(poly['polygon'])[:, 0],
                                 y=np.array(poly['polygon'])[:, 1],
                                 fill='toself',
                                 fillcolor=color,
                                 hoverinfo='text',
                                 text=text,
                                 name=text,
                                 line_shape='linear',
                                 mode='lines',
                                 line=dict(color=color),
                                 opacity=1))
    
    fig.update_layout(showlegend=True, xaxis_visible=False, yaxis_visible=False, plot_bgcolor='rgba(0,0,0,0)')
    fig.show()

# Sample usage
# polygons = [{'encoding': '10',
