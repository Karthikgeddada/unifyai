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
    # 🔥 Large Dataset Safety Fixes
    # ---------------------------

    # Remove auto index columns like Unnamed: 0
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Convert all columns to string to avoid Arrow type errors
    df = df.astype(str)

    # Guard against extremely large datasets (Streamlit Cloud limit protection)
    if len(df) > 600000:
        st.warning("Dataset too large for Streamlit Cloud memory limits.")
        st.stop()

    # ---------------------------
    # Preview (Safe Rendering)
    # ---------------------------

    st.subheader("📄 Data Preview (First 100 Rows)")
    st.dataframe(df.head(100), width="stretch")

    # ---------------------------
    # Process Button
    # ---------------------------

    if st.button("⚡ Process Data"):

        df_normalized = df.apply(lambda x: x.str.strip())

        seen = set()
        duplicates = []
        unique_rows = []

        progress = st.progress(0)

        for i, (_, row) in enumerate(df_normalized.iterrows()):

            row_tuple = tuple(row)

            if row_tuple in seen:
                duplicates.append(row.to_dict())
            else:
                seen.add(row_tuple)
                unique_rows.append(row.to_dict())

            progress.progress((i + 1) / len(df_normalized))

        progress.empty()

        st.success("Processing Complete ✅")

        col1, col2 = st.columns(2)
        col1.metric("Unique Rows", len(unique_rows))
        col2.metric("Duplicate Rows", len(duplicates))

        # ---------------------------
        # Show Duplicates (Safe Preview)
        # ---------------------------

        if duplicates:
            st.subheader("⚠️ Duplicate Records (Preview First 100)")
            st.dataframe(pd.DataFrame(duplicates).head(100), width="stretch")
        else:
            st.success("No duplicate records found 🎉")

        # ---------------------------
        # Show Unique Data (Safe Preview)
        # ---------------------------

        st.subheader("🧠 Unique Dataset (Preview First 100)")
        st.dataframe(pd.DataFrame(unique_rows).head(100), width="stretch")
