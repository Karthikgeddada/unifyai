import streamlit as st
import pandas as pd

st.set_page_config(page_title="UnifyAI - Universal Duplicate Detector", layout="wide")

st.title("🚀 UnifyAI - Universal CSV Duplicate Detection Engine")
st.write("Upload any CSV or Excel file. The system will automatically detect exact duplicate rows.")

# ---------------------------
# File Upload
# ---------------------------

uploaded_file = st.file_uploader(
    "📂 Upload Dataset (CSV or Excel)",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    # ---------------------------
    # Read File (Auto Detect)
    # ---------------------------

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    if df.empty:
        st.warning("Uploaded file is empty.")
        st.stop()

    # ---------------------------
    # Large Dataset Safety Fixes
    # ---------------------------

    # Remove auto index columns like Unnamed: 0
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Convert all columns to string
    df = df.astype(str)

    # Prevent memory crash
    if len(df) > 600000:
        st.warning("Dataset too large for Streamlit Cloud memory limits.")
        st.stop()

    # ---------------------------
    # Preview Uploaded Data
    # ---------------------------

    st.subheader("📄 Data Preview (First 100 Rows)")
    st.dataframe(df.head(100), use_container_width=True)

    # ---------------------------
    # Process Button
    # ---------------------------

    if st.button("⚡ Process Data"):

        with st.spinner("Processing dataset..."):

            # Normalize data
            df_normalized = df.apply(lambda x: x.str.strip())

            # Faster duplicate detection
            duplicates_df = df_normalized[df_normalized.duplicated()]
            unique_df = df_normalized.drop_duplicates()

        st.success("Processing Complete ✅")

        # Metrics
        col1, col2 = st.columns(2)
        col1.metric("Unique Rows", len(unique_df))
        col2.metric("Duplicate Rows", len(duplicates_df))

        # ---------------------------
        # Duplicate Records
        # ---------------------------

        if not duplicates_df.empty:
            st.subheader("⚠️ Duplicate Records")
            st.dataframe(duplicates_df, use_container_width=True)
        else:
            st.success("No duplicate records found 🎉")

        # ---------------------------
        # Unique Dataset
        # ---------------------------

        st.subheader("🧠 Unique Dataset")
        st.dataframe(unique_df, use_container_width=True)

        # ---------------------------
        # Download Buttons
        # ---------------------------

        st.subheader("⬇ Download Results")

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "Download Unique Dataset",
                unique_df.to_csv(index=False),
                file_name="unique_dataset.csv",
                mime="text/csv"
            )

        with col2:
            st.download_button(
                "Download Duplicate Dataset",
                duplicates_df.to_csv(index=False),
                file_name="duplicate_dataset.csv",
                mime="text/csv"
            )
