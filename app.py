import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="SimGuard AI - MVP", layout="wide")

st.title("🚨 SimGuard AI – Crowd & Emergency Simulation (MVP)")
st.write(
    "A simulation-based system to visualize crowd congestion and evacuation risks "
    "during emergency situations."
)

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Simulation Controls")

grid_size = st.sidebar.slider("Venue Size (Grid)", 20, 60, 40)
crowd_size = st.sidebar.slider("Number of People", 50, 500, 200)
emergency = st.sidebar.selectbox(
    "Emergency Type",
    ["None", "Fire", "Exit Blocked", "Medical Emergency"]
)

run_simulation = st.sidebar.button("Run Simulation")

# -----------------------------
# Simulation Logic
# -----------------------------
def simulate_crowd(grid_size, crowd_size, emergency):
    grid = np.zeros((grid_size, grid_size))

    # Random crowd placement
    x = np.random.randint(0, grid_size, crowd_size)
    y = np.random.randint(0, grid_size, crowd_size)

    for i in range(crowd_size):
        grid[x[i], y[i]] += 1

    # Add risk amplification during emergency
    if emergency != "None":
        center = grid_size // 2
        for i in range(grid_size):
            for j in range(grid_size):
                distance = np.sqrt((i - center) ** 2 + (j - center) ** 2)
                if distance < grid_size / 4:
                    grid[i, j] += 3  # congestion spike

    return grid

# -----------------------------
# Visualization
# -----------------------------
if run_simulation:
    st.subheader("📊 Simulation Output")

    grid = simulate_crowd(grid_size, crowd_size, emergency)

    fig, ax = plt.subplots()
    heatmap = ax.imshow(grid, cmap="hot")
    plt.colorbar(heatmap, ax=ax)
    ax.set_title("Crowd Density Heatmap")

    st.pyplot(fig)

    # Risk Analysis
    max_density = np.max(grid)

    st.subheader("⚠️ Risk Analysis")
    if max_density > 10:
        st.error("High congestion detected! Stampede risk possible.")
        st.write("Suggested Action: Open additional exits and redirect crowd flow.")
    elif max_density > 5:
        st.warning("Moderate congestion detected.")
        st.write("Suggested Action: Monitor crowd and prepare evacuation guidance.")
    else:
        st.success("Crowd conditions are stable.")
        st.write("Suggested Action: Continue monitoring.")

else:
    st.info("Adjust parameters from the sidebar and click **Run Simulation**.")
