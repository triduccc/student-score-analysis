import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import io
from PIL import Image

#Title for the page
st.title("Student score analysis")

#File uploaded by user
uploaded_file = st.file_uploader("Upload an Excel file (must have a \"Grade\" column)", type=["xlsx"])

def calculate_average(scores):
    return sum(scores) / len(scores)

def percentage_distribution(scores):
    bins = {"90-100": 0, "80-89": 0, "70-79": 0, "60-69": 0, "<60": 0,}
    for score in scores:
        if score >= 90:
            bins["90-100"] += 1
        elif score >= 80:
            bins["80-89"] += 1
        elif score >= 70:
            bins["70-79"] += 1
        elif score >= 60:
            bins["60-69"] += 1
        else:
            bins["<60"] += 1
    return bins     

if uploaded_file:
    # Read the file and delete the Nan value in the grade
    df = pd.read_excel(uploaded_file)
    scores = df["Grade"].dropna().astype(float).tolist()  

    if scores:
        # Display some infomation
        st.write("Total number of students:", len(scores))
        st.write("Average grade:", round(calculate_average(scores), 2))

        # Distribute grade
        dist = percentage_distribution(scores)
        labels = list(dist.keys())
        values = list(dist.values())

        # Draw the pie chart
        fig, ax = plt.subplots(figsize=(3,3))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        plt.tight_layout(pad=0.1)

        # Save the chart as an image for high resolution
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        buf.seek(0)
        st.markdown("Grade distribution chart")
        img = Image.open(buf)

        # Make 3 cols, with the middle one wider
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img, width=300)
            st.markdown("Grade distribution chart")
            





