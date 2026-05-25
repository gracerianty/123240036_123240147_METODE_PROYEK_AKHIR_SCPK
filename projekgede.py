# IMPORT LIBRARY
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# PAGE CONFIG
st.set_page_config(
    page_title="Student Apartment DSS - WP Method",
    layout="wide"
)

# SIDEBAR
st.sidebar.title("Group Profile")

st.sidebar.write("""
Grace Rianty Butar Butar

(NIM: 123240036) 
                 
Raffi Abbad Vega Pratama

(NIM: 123240147) 
""")

st.sidebar.markdown("---")

st.sidebar.write("""
### Project Information
- Course: Decision Support System
- Method: Weighted Product (WP)
- Tools: Streamlit + Python
- Dataset: Apartment Dataset CSV
""")

# MAIN TITLE
st.title("🏢 Best Apartment Selection System for Students")
st.subheader("Weighted Product (WP) Method")

st.write("""
This system helps determine the best apartment based on several criteria such as price, year built, size, floor, and nearby facilities. The method used is the Weighted Product (WP) method.
""")


# LOAD DATASET
try:
    df = pd.read_csv("apartment.csv", sep=';')
except:
    st.error("File apartment.csv tidak ditemukan!")
    st.stop()

# Clean dataset
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


# REQUIRED COLUMNS
required_cols = [
    'SalePrice',
    'YearBuilt',
    'Size(sqf)',
    'Floor',
    'N_FacilitiesNearBy(Hospital)',
    'N_FacilitiesNearBy(Mall)',
    'N_FacilitiesNearBy(ETC)',
    'N_SchoolNearBy(University)',
    'N_FacilitiesInApt'
]

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Kolom berikut tidak ada di dataset: {missing}")
    st.stop()

# Convert numeric
df[required_cols] = df[required_cols].apply(pd.to_numeric, errors='coerce')
df = df.dropna().reset_index(drop=True)


# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dataset",
    "📈 Visualization",
    "📘 WP Theory",
    "🏆 WP Calculation",
])

# TAB 1 - DATASET
with tab1:

    st.subheader("📊 Dataset Apartemen")

    col1, col2 = st.columns(2)
    col1.metric("Total Data", len(df))
    col2.metric("Total Criteria", len(required_cols))

    st.dataframe(df)

# TAB 2 - VISUALIZATION
with tab2:

    st.subheader("📊 Data Visualization & Interpretation")

    # 1. PRICE DISTRIBUTION
    st.subheader("1️⃣ Apartment Price Distribution")

    fig, ax = plt.subplots()
    ax.hist(df['SalePrice'], bins=20)
    ax.set_title("Apartment Price Distribution")
    ax.set_xlabel("Price")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

    st.write("""
    📌 **Meaning:**
    This chart shows how apartment prices are distributed in the dataset.

    - Most data on the left → most apartments are affordable
    - Wide spread → high price variation
    - Useful to understand market price range for students
    """)

    # 2. SIZE vs PRICE
    st.subheader("2️⃣ Apartment Size vs Price")

    fig, ax = plt.subplots()
    ax.scatter(df['Size(sqf)'], df['SalePrice'])
    ax.set_title("Size vs Price Relationship")
    ax.set_xlabel("Size (sqf)")
    ax.set_ylabel("Price")

    st.pyplot(fig)

    st.write("""
    📌 **Meaning:**
    This chart shows the relationship between apartment size and price.

    - Upward trend → larger apartments are more expensive
    - Scattered points → weak relationship
    - Helps analyze whether size affects price significantly
    """)

    # 3. FACILITIES
    st.subheader("3️⃣ Average Nearby Facilities")

    facility_avg = {
        "Hospital": df['N_FacilitiesNearBy(Hospital)'].mean(),
        "Mall": df['N_FacilitiesNearBy(Mall)'].mean(),
        "University": df['N_SchoolNearBy(University)'].mean()
    }

    fig, ax = plt.subplots()
    ax.bar(facility_avg.keys(), facility_avg.values())
    ax.set_title("Average Nearby Facilities")
    ax.set_ylabel("Average Count")

    st.pyplot(fig)

    st.write("""
    📌 **Meaning:**
    This chart shows the availability of facilities around apartments.

    - Higher value → better accessibility
    - Important factor for student housing decisions
    - Helps evaluate location quality
    """)

    # 4. FLOOR DISTRIBUTION
    st.subheader("4️⃣ Apartment Floor Distribution")

    floor_counts = df['Floor'].value_counts().head(5)

    fig, ax = plt.subplots()
    ax.pie(floor_counts, labels=floor_counts.index, autopct='%1.1f%%')
    ax.set_title("Floor Distribution")

    st.pyplot(fig)

    st.write("""
    📌 **Meaning:**
    This chart shows the most common apartment floors in the dataset.

    - Large slice → most frequent floor level
    - Helps understand building structure patterns
    - Useful for analyzing availability trends
    """)

# TAB 3 - WP THEORY
with tab3:

    st.subheader("📘 Weighted Product Method")

    st.write("""
    Weighted Product (WP) adalah metode SPK yang menggunakan perkalian antar kriteria,
    di mana setiap nilai dipangkatkan dengan bobotnya.
    """)

    st.subheader("Rumus Vector S")
    st.latex(r"S_i = \prod_{j=1}^{n} x_{ij}^{w_j}")

    st.subheader("Rumus Vector V")
    st.latex(r"V_i = \frac{S_i}{\sum S_i}")

    st.subheader("Jenis Kriteria (Cost & Benefit)")

    criteria_info = pd.DataFrame({
        "Criteria": [
            "SalePrice",
            "YearBuilt",
            "Size(sqf)",
            "Floor",
            "Hospital",
            "Mall",
            "ETC",
            "University",
            "Facilities"
        ],
        "Type": [
            "Cost",
            "Benefit",
            "Benefit",
            "Benefit",
            "Benefit",
            "Benefit",
            "Benefit",
            "Benefit",
            "Benefit"
        ],
        "Explanation": [
            "Higher price is worse",
            "Newer building is better",
            "Larger size is better",
            "Higher floor is better",
            "Closer to hospital is better",
            "Closer to mall is better",
            "More additional facilities is better",
            "Closer to university is better",
            "More in-apartment facilities is better"
        ]
    })

    st.dataframe(criteria_info)

# TAB 4 - WP CALCULATION
with tab4:

    st.subheader("⚖️ Input Bobot Kriteria")

    col1, col2, col3 = st.columns(3)

    with col1:
        w_price = st.slider("Price (Cost)", 1, 10, 5)
        w_year = st.slider("Year Built", 1, 10, 5)
        w_size = st.slider("Size", 1, 10, 5)

    with col2:
        w_floor = st.slider("Floor", 1, 10, 5)
        w_hospital = st.slider("Hospital", 1, 10, 5)
        w_mall = st.slider("Mall", 1, 10, 5)

    with col3:
        w_etc = st.slider("ETC", 1, 10, 5)
        w_univ = st.slider("University", 1, 10, 5)
        w_apt = st.slider("Facilities", 1, 10, 5)

    # CALC BUTTON
    if st.button("🚀 Calculate WP"):

        data = df.copy()
        alternatif = data.index

        # MATRIX DATA
        matrix = data[required_cols].to_numpy(dtype=float)

        # BOBOT AWAL
        bobot_awal = np.array([
            w_price, w_year, w_size,
            w_floor, w_hospital, w_mall,
            w_etc, w_univ, w_apt
        ], dtype=float)

        # Normalisasi bobot
        norm_bobot = bobot_awal / np.sum(bobot_awal)

        # COST handling (SalePrice = index 0)
        norm_bobot[0] = -norm_bobot[0]

        # TAMPILKAN BOBOT
        st.subheader("📌 Normalisasi Bobot")
        st.write(pd.DataFrame({
            "Criteria": required_cols,
            "Weight": norm_bobot,
            "Type": ["Cost"] + ["Benefit"] * 8
        }))

        # VECTOR S (WP STEP 1)
        matrix = np.where(matrix <= 0, 0.0001, matrix)

        S = []

        for i in range(len(matrix)):
            s_val = 1
            for j in range(len(required_cols)):
                s_val *= matrix[i][j] ** norm_bobot[j]
            S.append(s_val)

        # VECTOR V (WP STEP 2)
        S = np.array(S)
        V = S / np.sum(S)

        # RESULT TABLE
        result = pd.DataFrame({
            "Vector_S": S,
            "Vector_V": V
        }, index=alternatif)

        result["Ranking"] = result["Vector_V"].rank(
            ascending=False,
            method="dense"
        ).astype(int)

        result = result.sort_values("Vector_V", ascending=False)

        # attach
        data["Vector_S"] = S
        data["Vector_V"] = V
        data["Ranking"] = result["Ranking"].values

        # OUTPUT
        st.success("✅ WP Calculation Completed")

        st.subheader("🏅 Top 10 Apartemen")

        st.dataframe(
            data.sort_values("Vector_V", ascending=False).head(10)
        )

        # BEST RESULT
        best = result.index[0]

        st.subheader("🏢 Best Apartment")
        st.write(f"Alternatif terbaik adalah: **{best}**")