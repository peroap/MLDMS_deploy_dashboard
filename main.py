import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download data
URL = "https://raw.githubusercontent.com/marcopeix/streamlit-population-canada/master/data/quarterly_canada_population.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(URL, index_col=0, dtype={'Quarter': str, 
                                          'Canada': np.int32,
                                         'Newfoundland and Labrador': np.int32,
                                          'Prince Edward Island': np.int32,
                                          'Nova Scotia': np.int32,
                                          'New Brunswick': np.int32,
                                          'Quebec': np.int32,
                                          'Ontario': np.int32,
                                          'Manitoba': np.int32,
                                          'Saskatchewan': np.int32,
                                          'Alberta': np.int32,
                                          'British Columbia': np.int32,
                                          'Yukon': np.int32,
                                          'Northwest Territories': np.int32,
                                          'Nunavut': np.int32})
    return df

@st.cache_data
def reformat_dates_to_float(date_as_string: str) -> float:
    date_quarter_str, date_year = date_as_string.split(" ")
    date_quarter = 0.25 * (int(date_quarter_str[-1]) - 1)
    formatted_date = int(date_year)+date_quarter
    return formatted_date


if __name__=="__main__":
    
    df = load_data()

    # Title
    st.title("Population of Canada")

    # Source of data
    st.markdown(f"Source of data can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1710000901)")

    # Expander containing data
    with st.expander(label="See full data table", expanded=False):
        st.dataframe(df)

    # Form to filter
    with st.form("filter_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Choose a starting date")
            start_quarter = st.selectbox(
                label="Quarter",
                options=["Q1", "Q2", "Q3", "Q4"],
                index=2,
                key="start_quarter_select"
            )
            start_year = st.slider(
                label="Year", 
                min_value=1991, 
                max_value=2023,
                step=1,
                value=1991,
                key="start_year_select")

        with col2:
            st.write("Choose an end date")
            end_quarter = st.selectbox(
                label="Quarter",
                options=["Q1", "Q2", "Q3", "Q4"],
                index=0,
                key="end_quarter_select"
            )
            end_year = st.slider(label="Year",
                                min_value=1991,
                                max_value=2023,
                                step=1,
                                value=2023,
                                key="end_year_select")

        with col3:
            st.write("Choose a location")
            location = st.selectbox(label="Choose a location",
                                    options=df.columns,
                                    index=0)
        
        submit_button = st.form_submit_button("Analyze", type="primary")

    start_date = f"{start_quarter} {start_year}"
    end_date = f"{end_quarter} {end_year}"

    # check if start_date < end_date
    if reformat_dates_to_float(start_date) >= reformat_dates_to_float(end_date):
        st.error("Please make sure your end date is later than the start date")    
    else:
        # Results in tabs
        tab1, tab2 = st.tabs(["Population change", "Compare"])

        with tab1:
            st.subheader(f"Population change from {start_quarter} {start_year} to {end_quarter} {end_year}")
            tab1_col1, tab1_col2 = st.columns(2)
            
            with tab1_col1:
                try:
                    # Start date metric
                    population_start = int(df[f"{location}"][f"{start_date}"])
                    metric_start = st.metric(f"{start_quarter} {start_year}", population_start)
                    # End date metric
                    population_end = int(df[f"{location}"][f"{end_date}"])
                    metric_end = st.metric(f"{end_quarter} {end_year}", population_end, delta= f"{round(100*(population_end-population_start)/population_start, 2)}%")
                except KeyError:
                    st.error(f"Please note that the data starts on {df.index[0]} an ends on {df.index[-1]}. Select a timespan that is present in the data.")

            with tab1_col2:
                try:
                    x_values = df[f"{location}"][f"{start_date}":f"{end_date}"].index
                    y_values = df[f"{location}"][f"{start_date}":f"{end_date}"]

                    fig, ax = plt.subplots()
                    plt.plot(x_values, y_values)
                    ax.set_xlabel("Time")
                    ax.set_ylabel("Population")
                    ax.set_xticks([f"{start_date}", f"{end_date}"])
                    st.pyplot(fig)
                except:
                    None

        with tab2:
            st.subheader("Compare locations to eachother")        
            selected_locations_compare = st.multiselect(label="Choose locations to be compared", options=df.columns, default=["Canada", "Quebec"])
            
            if len(selected_locations_compare)>0:
                fig, ax = plt.subplots()
                for location_i in selected_locations_compare:
                    x_values_i = df[f"{location_i}"][f"{start_date}":f"{end_date}"].index
                    y_values_i = df[f"{location_i}"][f"{start_date}":f"{end_date}"]
                    ax.plot(x_values_i, y_values_i)
                ax.set_xlabel("Time")
                ax.set_ylabel("Population")
                ax.set_xticks([f"{start_date}", f"{end_date}"])
                st.pyplot(fig)