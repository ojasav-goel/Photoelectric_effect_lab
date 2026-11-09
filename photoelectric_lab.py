
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from scipy.stats import linregress

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Photoelectric Effect Virtual Lab",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------

H = 6.62607015e-34       # Planck's constant (J s)
E = 1.602176634e-19      # Electron charge (C)
C = 299792458            # Speed of light (m/s)

# ---------------------------------------------------------
# METAL DATABASE
# Work functions are approximate experimental values.
# ---------------------------------------------------------

METALS = {
    "Cesium (Cs)": 2.14,
    "Potassium (K)": 2.30,
    "Sodium (Na)": 2.28,
    "Calcium (Ca)": 2.90,
    "Zinc (Zn)": 4.30,
    "Copper (Cu)": 4.70,
    "Aluminium (Al)": 4.28,
    "Silver (Ag)": 4.73
}

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def calculate_threshold_frequency(work_function):
    """Calculate threshold frequency in Hz."""
    return (work_function * E) / H


def calculate_photon_energy(frequency):
    """Calculate photon energy in eV."""
    return (H * frequency) / E


def calculate_kinetic_energy(frequency, work_function):
    """Calculate maximum kinetic energy in eV."""
    return max(calculate_photon_energy(frequency) - work_function, 0)


def calculate_stopping_potential(frequency, work_function):
    """Stopping potential in volts."""
    return calculate_kinetic_energy(frequency, work_function)


def calculate_wavelength(frequency):
    """Calculate wavelength in nanometres."""
    return (C / frequency) * 1e9


def calculate_photoelectric_current(intensity, emitted):
    """
    Relative photocurrent model.

    Intensity is proportional to incident photon flux.
    This is a normalized model, not an absolute current.
    """
    if not emitted:
        return 0.0

    return intensity


# ---------------------------------------------------------
# TITLE AND INTRODUCTION
# ---------------------------------------------------------

st.title("⚡ Photoelectric Effect Virtual Laboratory")

st.markdown(
    """
    Explore the photoelectric effect by changing the frequency
    and intensity of incident light and selecting different metal
    surfaces.

    Observe electron emission, calculate stopping potential,
    and experimentally determine Planck's constant.
    """
)

st.divider()

# ---------------------------------------------------------
# SIDEBAR - EXPERIMENTAL CONTROLS
# ---------------------------------------------------------

st.sidebar.header("🔬 Experimental Controls")

st.sidebar.subheader("1. Select Metal Surface")

selected_metal = st.sidebar.selectbox(
    "Choose the metal:",
    list(METALS.keys()),
    index=0
)

work_function = METALS[selected_metal]

st.sidebar.subheader("2. Light Source")

frequency = st.sidebar.slider(
    "Light Frequency (×10¹⁴ Hz)",
    min_value=2.0,
    max_value=15.0,
    value=8.0,
    step=0.1
) * 1e14

intensity = st.sidebar.slider(
    "Light Intensity (%)",
    min_value=0,
    max_value=100,
    value=70,
    step=1
)

st.sidebar.subheader("3. Experimental Information")

st.sidebar.info(
    """
    **Remember:**

    • Frequency determines photon energy.

    • Intensity determines the number of incident photons.

    • Work function determines the minimum energy
      required to release an electron.
    """
)

# ---------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------

threshold_frequency = calculate_threshold_frequency(work_function)

photon_energy = calculate_photon_energy(frequency)

kinetic_energy = calculate_kinetic_energy(
    frequency, work_function
)

stopping_potential = kinetic_energy

wavelength = calculate_wavelength(frequency)

emission_possible = (
    frequency >= threshold_frequency and intensity > 0
)

relative_current = calculate_photoelectric_current(
    intensity, emission_possible
)

# ---------------------------------------------------------
# EXPERIMENTAL RESULTS
# ---------------------------------------------------------

st.header("1. Experimental Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Photon Energy",
    f"{photon_energy:.3f} eV"
)

col2.metric(
    "Work Function",
    f"{work_function:.2f} eV"
)

col3.metric(
    "Maximum Kinetic Energy",
    f"{kinetic_energy:.3f} eV"
)

col4.metric(
    "Stopping Potential",
    f"{stopping_potential:.3f} V"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Threshold Frequency",
    f"{threshold_frequency / 1e14:.3f} × 10¹⁴ Hz"
)

col6.metric(
    "Incident Wavelength",
    f"{wavelength:.2f} nm"
)

col7.metric(
    "Relative Photocurrent",
    f"{relative_current:.1f}%"
)

col8.metric(
    "Selected Metal",
    selected_metal
)

st.divider()

# ---------------------------------------------------------
# ELECTRON EMISSION STATUS
# ---------------------------------------------------------

st.header("2. Electron Emission Observation")

if emission_possible:

    st.success(
        "ELECTRON EMISSION DETECTED! "
        "The incident photon energy is sufficient "
        "to overcome the metal's work function."
    )

    st.write(
        f"Maximum kinetic energy of emitted electrons: "
        f"**{kinetic_energy:.4f} eV**"
    )

elif intensity == 0:

    st.warning(
        "No incident light. Therefore, no photoelectrons "
        "are emitted."
    )

else:

    st.error(
        "NO ELECTRON EMISSION! The photon energy is "
        "less than the metal's work function."
    )

    st.write(
        f"Frequency must reach at least "
        f"**{threshold_frequency / 1e14:.3f} × 10¹⁴ Hz** "
        f"for electron emission."
    )

# ---------------------------------------------------------
# PHOTOELECTRIC EFFECT VISUALIZATION
# ---------------------------------------------------------

st.subheader("Interactive Photoelectric Cell")

fig, ax = plt.subplots(figsize=(11, 4.5))

ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")

# Vacuum tube
tube = Rectangle(
    (3.2, 0.7), 7.7, 4.7,
    linewidth=2,
    edgecolor="black",
    facecolor="#EAF3FA",
    alpha=0.65
)

ax.add_patch(tube)

# Metal cathode
cathode = Rectangle(
    (3.5, 1.2), 0.45, 3.7,
    facecolor="#777777",
    edgecolor="black"
)

ax.add_patch(cathode)

ax.text(
    3.7, 0.85, "Metal Cathode",
    ha="center", fontsize=9
)

# Anode
anode = Rectangle(
    (10.3, 1.2), 0.25, 3.7,
    facecolor="#D69E36",
    edgecolor="black"
)

ax.add_patch(anode)

ax.text(
    10.4, 0.85, "Anode",
    ha="center", fontsize=9
)

# Incoming light rays
for y in [2.1, 3.0, 3.9]:
    ax.add_patch(
        FancyArrowPatch(
            (0.5, y), (3.35, y),
            arrowstyle="->",
            mutation_scale=15,
            linewidth=2,
            color="orange"
        )
    )

ax.text(
    1.7, 4.65,
    "Incident Light",
    ha="center",
    fontsize=11,
    color="darkorange",
    fontweight="bold"
)

# Photon label
ax.text(
    1.7, 1.2,
    f"f = {frequency / 1e14:.2f} × 10¹⁴ Hz",
    ha="center",
    fontsize=9
)

# Electron visualization
if emission_possible:

    number_of_electrons = max(
        1, int(intensity / 10)
    )

    rng = np.random.default_rng(42)

    for i in range(number_of_electrons):

        y = rng.uniform(1.5, 4.6)

        x_end = rng.uniform(7.0, 9.7)

        electron = Circle(
            (4.15, y),
            radius=0.09,
            color="blue"
        )

        ax.add_patch(electron)

        ax.add_patch(
            FancyArrowPatch(
                (4.35, y),
                (x_end, y),
                arrowstyle="->",
                mutation_scale=10,
                linewidth=1.2,
                color="blue"
            )
        )

    ax.text(
        7.0, 5.65,
        "Emitted Photoelectrons →",
        color="blue",
        fontsize=12,
        ha="center",
        fontweight="bold"
    )

else:

    ax.text(
        7.0, 3.0,
        "No Photoelectron Emission",
        color="red",
        fontsize=13,
        ha="center",
        fontweight="bold"
    )

ax.set_title(
    "Schematic Representation of the Photoelectric Effect",
    fontsize=14,
    fontweight="bold",
    pad=15
)

st.pyplot(fig)
plt.close(fig)

st.caption(
    "Illustrative schematic: electron trajectories are not "
    "to scale. The relative number of arrows represents "
    "light intensity, not a measured electron count."
)

st.divider()

# ---------------------------------------------------------
# ENERGY LEVEL DIAGRAM
# ---------------------------------------------------------

st.header("3. Energy Level Analysis")

fig2, ax2 = plt.subplots(figsize=(9, 4))

ax2.set_xlim(0, 10)
ax2.set_ylim(-0.5, max(photon_energy, work_function) + 2)

# Fermi/reference energy
ax2.axhline(
    0, color="black", linewidth=2
)

ax2.text(
    0.3, 0.2,
    "Initial electron energy (reference)",
    fontsize=9
)

# Work function level
ax2.axhline(
    work_function,
    color="red",
    linestyle="--",
    linewidth=2
)

ax2.text(
    7.2, work_function + 0.15,
    f"Work Function = {work_function:.2f} eV",
    color="red",
    fontsize=10
)

# Photon energy
ax2.annotate(
    "",
    xy=(3, photon_energy),
    xytext=(3, 0),
    arrowprops=dict(
        arrowstyle="->",
        color="orange",
        linewidth=3
    )
)

ax2.text(
    3.2,
    photon_energy / 2,
    f"Photon Energy\n{photon_energy:.2f} eV",
    color="darkorange",
    fontsize=10
)

if emission_possible:

    ax2.annotate(
        "",
        xy=(5.5, photon_energy),
        xytext=(5.5, work_function),
        arrowprops=dict(
            arrowstyle="->",
            color="blue",
            linewidth=3
        )
    )

    ax2.text(
        5.8,
        (photon_energy + work_function) / 2,
        f"KE = {kinetic_energy:.2f} eV",
        color="blue",
        fontsize=10
    )

ax2.set_ylabel("Energy (eV)")
ax2.set_xticks([])
ax2.set_title("Energy Level Diagram")
ax2.grid(axis="y", alpha=0.3)

st.pyplot(fig2)
plt.close(fig2)

st.divider()

# ---------------------------------------------------------
# PLANCK'S CONSTANT EXPERIMENT
# ---------------------------------------------------------

st.header("4. Determination of Planck's Constant")

st.markdown(
    """
    In this experiment, the stopping potential is measured
    for different frequencies of incident light.

    Einstein's photoelectric equation is:

    **Vs = (h/e)f - (φ/e)**

    The slope of the graph is h/e.
    Therefore, Planck's constant can be determined by
    multiplying the slope by the electron charge.
    """
)

# Generate frequency values
frequencies = np.linspace(
    2e14,
    15e14,
    100
)

# Theoretical stopping potential
stopping_voltages = np.maximum(
    (H * frequencies / E) - work_function,
    0
)

# Only use frequencies above threshold
valid = frequencies > threshold_frequency

f_valid = frequencies[valid]
v_valid = stopping_voltages[valid]

fig3, ax3 = plt.subplots(figsize=(10, 5))

ax3.plot(
    frequencies / 1e14,
    stopping_voltages,
    color="gray",
    linestyle="--",
    label="Theoretical curve"
)

ax3.scatter(
    f_valid / 1e14,
    v_valid,
    color="blue",
    s=22,
    label="Photoelectric measurements"
)

# Linear regression
if len(f_valid) >= 2:

    result = linregress(
        f_valid,
        v_valid
    )

    slope = result.slope
    intercept = result.intercept

    calculated_h = slope * E

    fitted_values = slope * f_valid + intercept

    ax3.plot(
        f_valid / 1e14,
        fitted_values,
        color="red",
        linewidth=2,
        label="Linear regression"
    )

    # Current frequency marker
    if emission_possible:

        ax3.scatter(
            [frequency / 1e14],
            [stopping_potential],
            color="green",
            s=110,
            marker="*",
            label="Current operating point",
            zorder=5
        )

    st.success("Linear regression completed successfully.")

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Calculated Planck's Constant",
        f"{calculated_h:.4e} J·s"
    )

    r2.metric(
        "Accepted Value",
        f"{H:.4e} J·s"
    )

    percentage_error = (
        abs(calculated_h - H) / H
    ) * 100

    r3.metric(
        "Percentage Error",
        f"{percentage_error:.6f}%"
    )

    st.write(
        f"**Experimental slope:** {slope:.6e} V·s"
    )

    st.write(
        f"**Regression R²:** {result.rvalue**2:.8f}"
    )

else:

    st.warning(
        "Insufficient frequency range above the threshold "
        "to perform linear regression."
    )

ax3.set_xlabel("Frequency (×10¹⁴ Hz)", fontsize=11)
ax3.set_ylabel("Stopping Potential (V)", fontsize=11)

ax3.set_title(
    "Stopping Potential vs Frequency",
    fontsize=14,
    fontweight="bold"
)

ax3.grid(True, alpha=0.3)
ax3.legend()

st.pyplot(fig3)
plt.close(fig3)

st.divider()

# ---------------------------------------------------------
# EXPERIMENTAL DATA TABLE
# ---------------------------------------------------------

st.header("5. Experimental Data Table")

data = {
    "Frequency (×10¹⁴ Hz)": frequencies / 1e14,
    "Photon Energy (eV)": H * frequencies / E,
    "Stopping Potential (V)": stopping_voltages
}

import pandas as pd

df = pd.DataFrame(data)

df = df.round(4)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Experimental Data (CSV)",
    data=csv,
    file_name="photoelectric_effect_data.csv",
    mime="text/csv"
)

st.divider()

# ---------------------------------------------------------
# CONCLUSION
# ---------------------------------------------------------

st.header("6. Experimental Conclusion")

st.markdown(
    f"""
    1. The selected metal is **{selected_metal}**.

    2. Its work function is **{work_function:.2f} eV**.

    3. Its threshold frequency is
       **{threshold_frequency:.4e} Hz**.

    4. The incident light frequency is
       **{frequency:.4e} Hz**.

    5. Electron emission is
       **{"observed" if emission_possible else "not observed"}**.

    6. The maximum kinetic energy is
       **{kinetic_energy:.4f} eV**.

    7. The stopping potential is
       **{stopping_potential:.4f} V**.

    The experiment demonstrates that the frequency of
    incident light determines the maximum kinetic energy
    of emitted photoelectrons, whereas light intensity
    controls the photocurrent when emission is possible.
    """
)

st.info(
    "End of Virtual Laboratory Experiment | Photoelectric Effect"
)
