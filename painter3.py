import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

# Hardcoded base colors (RGB values)
BASE_COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128)
}

# Convert color dictionary to a KDTree for quick nearest color matching
color_names = list(BASE_COLORS.keys())
color_values = np.array(list(BASE_COLORS.values()))
kdtree = KDTree(color_values)

def find_closest_colors(target_rgb, n=3):
    """Finds the n closest colors from the base color dictionary."""
    _, indices = kdtree.query(target_rgb, k=n)
    return [color_names[i] for i in indices]

def generate_recipe(target_rgb, closest_colors):
    """Generates a simple recipe with percentage composition."""
    percentages = np.random.dirichlet(np.ones(len(closest_colors)), size=1)[0] * 100
    return dict(zip(closest_colors, percentages))

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
    
    st.write("### Closest Paint Matches:")
    for color, percentage in recipe.items():
        st.write(f"{color}: {percentage:.2f}%")
        plot_color(BASE_COLORS[color], color)
    
    # Comparison visualization
    st.write("### Comparison of Resultant Colors:")
    fig, axes = plt.subplots(1, len(recipe) + 1, figsize=(len(recipe) * 2, 2))
    colors = [(r, g, b)] + [BASE_COLORS[color] for color in recipe]
    titles = ["Desired"] + list(recipe.keys())
    
    for ax, color, title in zip(axes, colors, titles):
        ax.set_facecolor(np.array(color) / 255)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
    
    st.pyplot(fig)
