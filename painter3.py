import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# Updated database of base colors with RGB values and density
db_colors = {
    "Burnt Sienna": {"rgb": [58, 22, 14], "density": 1073},
    "Burnt Umber": {"rgb": [50, 27, 15], "density": 1348},
    "Cadmium Orange Hue": {"rgb": [221, 105, 3], "density": 1338},
    "Cadmium Red Deep Hue": {"rgb": [171, 1, 5], "density": 902},
    "Cadmium Red Medium": {"rgb": [221, 63, 0], "density": 1547},
    "Cadmium Red Light": {"rgb": [225, 83, 0], "density": 1573},
    "Cadmium Red Dark": {"rgb": [166, 0, 9], "density": 1055},
    "Cadmium Yellow Hue": {"rgb": [255, 193, 0], "density": 1230},
    "Cadmium Yellow Light": {"rgb": [255, 194, 0], "density": 1403},
    "Cadmium Yellow Medium": {"rgb": [255, 161, 0], "density": 1534},
    "Cerulean Blue Hue": {"rgb": [0, 74, 91], "density": 1216},
    "Cobalt Blue": {"rgb": [0, 39, 71], "density": 1317},
    "Dioxazine Purple": {"rgb": [215, 17, 115], "density": 1268},
    "French Ultramarine": {"rgb": [8, 8, 32], "density": 1277},
    "Ivory Black": {"rgb": [27, 28, 28], "density": 1228},
    "Lamp Black": {"rgb": [21, 21, 20], "density": 958},
    "Lemon Yellow": {"rgb": [239, 173, 0], "density": 1024},
    "Magenta": {"rgb": [98, 4, 32], "density": 1822},
    "Permanent Alizarin Crimson": {"rgb": [74, 16, 16], "density": 1217},
    "Permanent Rose": {"rgb": [130, 0, 24], "density": 1227},
    "Permanent Sap Green": {"rgb": [28, 42, 10], "density": 1041},
    "Phthalo Blue (Red Shade)": {"rgb": [17, 12, 37], "density": 1080},
    "Phthalo Green (Yellow Shade)": {"rgb": [0, 32, 24], "density": 1031},
    "Phthalo Green (Blue Shade)": {"rgb": [3, 26, 33], "density": 1021},
    "Prussian Blue": {"rgb": [15, 11, 11], "density": 984},
    "Raw Sienna": {"rgb": [117, 70, 17], "density": 1211},
    "Raw Umber": {"rgb": [37, 28, 20], "density": 1273},
    "Titanium White": {"rgb": [249, 245, 234], "density": 1423},
    "Viridian": {"rgb": [0, 53, 40], "density": 1149},
    "Yellow Ochre": {"rgb": [187, 128, 18], "density": 1283},
    "Zinc White (Mixing White)": {"rgb": [250, 242, 222], "density": 1687},
}

# Convert color dictionary to a KDTree for quick nearest color matching
color_names = list(db_colors.keys())
color_values = np.array([db_colors[color]["rgb"] for color in color_names])
kdtree = KDTree(color_values)

def find_closest_colors(target_rgb, n=3):
    """Finds the n closest colors from the base color dataset."""
    _, indices = kdtree.query(target_rgb, k=n)
    return [color_names[i] for i in indices]

def generate_recipe(target_rgb, closest_colors):
    """Generates a recipe using closest matching colors and their densities."""
    densities = np.array([db_colors[color]["density"] for color in closest_colors])
    proportions = densities / densities.sum() * 100
    return dict(zip(closest_colors, proportions))

def plot_color(rgb, title):
    """Plots a color box with the given RGB value."""
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.set_facecolor(np.array(rgb) / 255)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    st.pyplot(fig)

# Streamlit UI
st.title("Painter App - Color Recipe Generator")

# User Input
r = st.number_input("Red (0-255)", min_value=0, max_value=255, value=128)
g = st.number_input("Green (0-255)", min_value=0, max_value=255, value=128)
b = st.number_input("Blue (0-255)", min_value=0, max_value=255, value=128)

# Display entered color
st.write("### Entered Color:")
plot_color((r, g, b), "Desired Color")

if st.button("Generate Recipe"):
    closest_colors = find_closest_colors((r, g, b))
    recipe = generate_recipe((r, g, b), closest_colors)
    
    st.write("### Paint Recipe:")
    for color, percentage in recipe.items():
        st.write(f"{color}: {percentage:.2f}%")
        plot_color(db_colors[color]["rgb"], color)
    
    # Comparison visualization
    st.write("### Comparison of Resultant Colors:")
    fig, axes = plt.subplots(1, len(recipe) + 1, figsize=(len(recipe) * 2, 2))
    colors = [(r, g, b)] + [db_colors[color]["rgb"] for color in recipe]
    titles = ["Desired"] + list(recipe.keys())
    
    for ax, color, title in zip(axes, colors, titles):
        ax.set_facecolor(np.array(color) / 255)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
    
    st.pyplot(fig)
