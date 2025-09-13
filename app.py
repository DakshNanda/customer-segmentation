import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Title
st.title("Customer Segmentation App")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)

        # Define scoring functions
        def score_spend(spend):
            if pd.isna(spend) or spend == 0:
                return 0
            elif spend >= 50000:
                return 3
            elif spend >= 20001:
                return 2
            elif spend >= 1:
                return 1
            return 0

        def score_size(size):
            if pd.isna(size) or size == 0:
                return 0
            elif size > 100:
                return 3
            elif size >= 51:
                return 2
            elif size >= 1:
                return 1
            return 0

        def score_engagement(engagement):
            engagement = str(engagement).strip().lower()
            if engagement == "demo completed":
                return 3
            elif engagement in ["demo scheduled", "linkedin reply"]:
                return 2
            elif engagement in ["email opened", "cold call only"]:
                return 1
            elif engagement in ["cold email sent", "no response"]:
                return 0
            return 0

        # Apply scoring
        df['Spend Score'] = df['Avg. Monthly Spend (₹)'].apply(score_spend)
        df['Size Score'] = df['Company Size (Employees)'].apply(score_size)
        df['Engagement Score'] = df['Current Engagement'].apply(score_engagement)

        # Total score
        df['Total Score'] = df['Spend Score'] + df['Size Score'] + df['Engagement Score']

        # Segmentation
        def segment(score):
            if score >= 8:
                return "Act Immediately"
            elif score >= 5:
                return "Check for Prospects"
            else:
                return "To Be Developed"

        df['Segment'] = df['Total Score'].apply(segment)

        # Display segmented data
        st.subheader("Segmented Customer Data")
        st.dataframe(df)

        # Summary
        st.subheader("Segment Summary")
        summary = df['Segment'].value_counts().reset_index()
        summary.columns = ['Segment', 'Count']
        st.dataframe(summary)

        
        # Display company names by segment
        st.subheader("Companies by Segment")
        for segment_label in ['Act Immediately', 'Check for Prospects', 'To Be Developed']:
            st.markdown(f"**{segment_label} Companies:**")
            companies = df[df['Segment'] == segment_label]['Company Name'].dropna().tolist()
            if companies:
                for company in companies:
                    st.write(f"- {company}")
            else:
                st.write("No companies in this segment.")


        # Download CSV
        st.subheader("Download Segmented Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="segmented_customers.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")




