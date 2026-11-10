
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Technology Learning Analytics",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Technology Learning Trend Analytics")
st.write("Analysis of technology articles from freeCodeCamp.")

# Upload dataset
uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Check required columns
    required = [
        "Article Title",
        "Description",
        "Published Date",
        "Article URL",
        "Provider",
        "Category"
    ]

    if not all(col in df.columns for col in required):
        st.error("Uploaded CSV does not contain all required columns.")

    else:

        # Convert dates
        df["Published Date"] = pd.to_datetime(
            df["Published Date"],
            errors="coerce",
            utc=True
        )

        # Summary metrics
        total_articles = len(df)
        total_categories = df["Category"].nunique()

        category_count = df["Category"].value_counts()

        most_popular = (
            category_count.idxmax()
            if not category_count.empty
            else "N/A"
        )

        st.subheader("📊 Overall Statistics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Articles", total_articles)
        col2.metric("Technology Categories", total_categories)
        col3.metric("Most Popular Technology", most_popular)

        st.divider()

        # Category filter
        st.subheader("🔎 Filter Articles")

        categories = sorted(df["Category"].dropna().unique())

        selected_category = st.selectbox(
            "Select Technology Category",
            ["All"] + categories
        )

        if selected_category != "All":
            filtered_df = df[
                df["Category"] == selected_category
            ]
        else:
            filtered_df = df.copy()

        # Bar chart
        st.subheader("Technology Category Analysis")

        category_count = filtered_df["Category"].value_counts()

        fig1 = px.bar(
            x=category_count.index,
            y=category_count.values,
            labels={
                "x": "Technology",
                "y": "Number of Articles"
            },
            title="Articles by Technology Category",
            text=category_count.values
        )

        st.plotly_chart(fig1, use_container_width=True)

        # Pie chart
        st.subheader("Technology Distribution")

        fig2 = px.pie(
            names=category_count.index,
            values=category_count.values,
            title="Technology Topic Distribution",
            hole=0.4
        )

        st.plotly_chart(fig2, use_container_width=True)

        # Monthly trends
        st.subheader("Monthly Publishing Trends")

        date_df = filtered_df.dropna(
            subset=["Published Date"]
        ).copy()

        if not date_df.empty:

            date_df["Month"] = (
                date_df["Published Date"].dt.to_period("M").astype(str)
            )

            monthly_count = (
                date_df.groupby("Month")
                .size()
                .reset_index(name="Articles")
            )

            fig3 = px.line(
                monthly_count,
                x="Month",
                y="Articles",
                markers=True,
                title="Monthly Article Publishing Trends"
            )

            st.plotly_chart(fig3, use_container_width=True)

        else:
            st.info("No valid publication dates available.")

        # Article search
        st.subheader("📖 Article Details")

        search = st.text_input("Search articles by title")

        if search:
            filtered_df = filtered_df[
                filtered_df["Article Title"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

        # Download CSV
        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Filtered Dataset",
            data=csv,
            file_name="technology_learning_trends.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload the CSV file generated from Google Colab.")
