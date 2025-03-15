from narwhals import col
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# HELPER FUNCTIONS
def create_month_trends(df):
    month_order= ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    bymonth_trends = df.groupby(by="month").agg({
        "total_casual_users": "sum",
        "total_registered_users": "sum",
        "total_rental": "sum"
    }).reindex(month_order)

    return bymonth_trends

def create_season_trends(df):
    season_order = ["Springer", "Summer", "Fall", "Winter"]
    byseason_trends = df.groupby(by="season").agg({
        "total_casual_users": "sum",
        "total_registered_users": "sum",
        "total_rental": "sum"  
    }).round().reindex(season_order)

    return byseason_trends

def create_yearly_trends(df):
    byyear_trends = df.groupby(by="year").agg({
        "total_casual_users": "sum",
        "total_registered_users": "sum",
    }).reset_index()

    byyear_trends["year"] = pd.Categorical(byyear_trends["year"], ordered=True)

    return byyear_trends

def create_weekly_pattern(df):
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week_pattern = df.groupby(by="day").agg({
        "total_casual_users": "mean",
        "total_registered_users": "mean",
        "total_rental": "mean",
    }).round().astype(int).reindex(weekday_order)

    return week_pattern

def create_byday_type(df):
    df["day_type"] = df.apply(
        lambda row: "Holiday" if row["isHoliday"] == 1 else "Working Day" if row["isWorkingDay"] == 1 else "Weekend", axis=1
    )
    byday_trends = df.groupby("day_type")["total_rental"].sum().round().astype(int).reset_index()

    return byday_trends

def create_byweather_type(df):
    byweather_type = df.groupby(by="weather_desc").agg({
        "total_casual_users": "sum",
        "total_registered_users": "sum",
        "total_rental": "sum",
    }).round().reset_index()

    return byweather_type

# DISABLED FOR NOW BECAUSE IN THIS ANALYSIS I JUST WANT TO FOCUS ANALYZING THE TRENDS
# def create_hourly_pattern(df):
#     hour_pattern = df.groupby(by="hour_time").agg({
#         "total_casual_users": "mean",
#         "total_registered_users": "mean",
#         "total_rental": "mean",
#     }).round().astype(int).reset_index()

#     return hour_pattern

# LOAD DATA
def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=['date'])

day_df = load_data("submission\dashboard\cleaned_day.csv")
# hour_df = load_data("submission\dashboard\cleaned_hour.csv") -> DISABLE CAUSE IT HAS NO USE

# SIDEBAR
with st.sidebar:
    st.caption("Made by Stevan Lukas")
    # MAKING FILTER
    st.header("Filters Option")
    # Date filter
    start_date = st.sidebar.date_input("Start Date", day_df["date"].min())
    end_date = st.sidebar.date_input("End Date", day_df["date"].max())

# DISABLED AT THIS MOMENT BECAUSE IT AFFECT TO ALL CHART, BUT IT WORKS. JUST NEED TO DO SOME ADJUSTMENT FIRST
    # # Weather filter
    # weather_options = day_df["weather_desc"].unique()
    # selected_weather = st.sidebar.multiselect("Select Weather Condition", weather_options)

    # # Season filter
    # season_options = day_df["season"].unique()
    # selected_season = st.sidebar.multiselect("Select Season", season_options)

    # Applying filter
    filtered_df = day_df.copy()

    apply_filter = False

    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df["date"] >= pd.to_datetime(start_date)) & 
                                (filtered_df["date"] <= pd.to_datetime(end_date))]
        apply_filter = True

# DISABLED AT THIS MOMENT BECAUSE IT AFFECT TO ALL CHART, BUT IT WORKS. JUST NEED TO DO SOME ADJUSTMENT FIRST
    # if selected_weather:
    #     filtered_df = filtered_df[filtered_df["weather_desc"].isin(selected_weather)]
    #     apply_filter = True

    # if selected_season:
    #     filtered_df = filtered_df[filtered_df["season"].isin(selected_season)]
    #     apply_filter = True

    # If NO filters were applied, show full dataset instead of empty result
    if not apply_filter:
        filtered_df = day_df

    # BRIEF GUIDELINE
    st.title('I. Brief Guideline of Bike-sharing System')
    st.subheader('1. What is Bike-sharing System?')
    st.markdown(
        """
        Bike-sharing system is a program that provides a fleet of bikes for public use, allowing individuals to rent them for short-term transportation or recreation, often through membership or single-ride fees
        """)
    st.subheader('2. What is the benefit?')
    st.markdown(
        """
        - **Convenience**: Provides a quick and easy way to travel short distances. 
        - **Sustainability** : Reduces traffic congestion and promotes eco-friendly transportation. 
        - **Accessibility** : Makes cycling accessible to a wider range of people, regardless of ownership. 
        - **Health** : Encourages physical activity and promotes a healthier lifestyle.
        """)
    st.subheader('3. What are the types of Bike-sharing System?')
    st.markdown(
        """
        - **Station-based** : Bikes are docked at specific stations and users can pick up and return them at those locations. 
        - **Free-floating** : Bikes can be picked up and returned anywhere within the service area, without the need for designated stations. 
        """
    )
    st.subheader('4. Example of Bike-sharing system')
    st.markdown(
        """
        - **Capital Bikeshare** : Washington D.C. 
        - **Citi bike** : New York City
        - **next bike** : German
        """
    )
    st.title('II. The Seasons in Washington D.C.')
    st.markdown(
        """
        - Spring : March to May
        - Summer : June to August
        - Fall : September to November
        - Winter : December to February
        """
    )

# CALLING HELPER FUNCTIONS
monthly_trends = create_month_trends(filtered_df)
season_trends = create_season_trends(filtered_df)
yearly_trends = create_yearly_trends(filtered_df)
weekly_pattern = create_weekly_pattern(filtered_df)
byday_type = create_byday_type(filtered_df)
byweather_day = create_byweather_type(filtered_df)
# hourly_pattern = create_hourly_pattern(hour_df)


# MAKING DASHBOARD
st.title('🚲BIKE-SHARING SYSTEM DASHBOARD📊')

# A. Bike Rentals by Day Type
#calculating percentage
total_rentals_sum = byday_type["total_rental"].sum()
byday_type["percentage"] = ((byday_type["total_rental"] / total_rentals_sum) * 100).round(2)

# Make a bar plot
st.subheader("A. Bike Rentals by Day Type")
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#ff9999", "#66b3ff", "#99ff99"]

ax = sns.barplot(x="day_type", y="total_rental", data=byday_type, palette="magma")
ax.set_xlabel("Day Type")
ax.set_ylabel("Total Rentals")
ax.set_title("Total Bike Rentals: Holidays - Working Days - Weekends")
# ubah dari plt ke fig, ax + tambahin persen diatas bar
for container, percentage in zip(ax.containers, byday_type["percentage"]):
    ax.bar_label(container, labels=[f"{percentage}%" for _ in container], fontsize=10, color='black')
st.pyplot(fig)

# B. Bike Rentals by Weather Type
#calculating percentage
weather_total_rentals = byweather_day["total_rental"].sum()
byweather_day["percentage"] = ((byweather_day["total_rental"] / weather_total_rentals)*100).round(2)

# Make a bar plot
st.subheader("B. Bike Rentals by Weather Condition")
fig, ax = plt.subplots(figsize=(10, 5))
ax = sns.barplot(data=byweather_day, x="weather_desc", y="total_rental", palette="PuBu", ci= None)
ax.set_xlabel("Weather Situation")
ax.set_ylabel("Total Rentals")
ax.set_title("Total Bike Rentals: Holidays - Working Days - Weekends")
# ubah dari plt ke fig, ax + tambahin persen diatas bar
for container, percentage in zip(ax.containers, byweather_day["percentage"]):
    ax.bar_label(container, labels=[f"{percentage}%" for _ in container], fontsize=10, color='black')
plt.xticks(rotation=30)
st.pyplot(fig)

# C. Bike Rentals Performance by Month and Season
st.subheader("C. Bike Rentals Performance by")
tab1, tab2 = st.tabs(["Month", "Season"])
with tab1:
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=monthly_trends, x="month", y="total_rental", palette="Blues", ax=ax1)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Rentals")
    # ax1.set_title("Monthly Bike Rental Trends")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with tab2:
    colors = ["#a6d75b", "#ffb400", "#e14b31", "#63bff0"]
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=season_trends, x="season" , y="total_rental", palette= colors, ax=ax2)
    ax2.set_ylabel("Total Rentals")
    ax2.set_xlabel("Season")
    # ax2.set_title("Rental Trends per Season", loc="center", fontsize=15)
    ax2.tick_params(axis ='y', labelsize=12)
    st.pyplot(fig2)

# D. WEEKLY PATTERN
st.subheader("D. Weekly Pattern")
plt.figure(figsize=(10, 5))
sns.lineplot(
    data= weekly_pattern, x= "day", y= "total_rental", 
    palette="bright",
)
plt.title("Weekly Patterns", loc="center", fontsize=15)
plt.xlabel("Day of The Week")
plt.ylabel("Total Users")
st.pyplot(plt)

# CASUAL vs REGISTERED USERS TOTAL
st.subheader("E. Casual vs. Registered Users")
yearly_melted = yearly_trends.melt(
    id_vars="year",
    value_vars=["total_casual_users", "total_registered_users"],
    var_name="User Type", 
    value_name="Total Users"
    )

yearly_melted["User Type"] = yearly_melted["User Type"].replace({
    "total_casual_users": "Casual Users",
    "total_registered_users": "Registered Users"
})

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(10, 5))

# Make a bar plot
sns.barplot(
    data=yearly_melted,
    x="year",
    y="Total Users",
    hue="User Type",
    palette=["#27aeef", "#00bfa0"],
    ax=ax 
)
# Add bar label
for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", fontsize=10, color="black", padding=3)

ax.set_xlabel("Year")
ax.set_ylabel("Total Users")
ax.set_title("Casual vs. Registered Users per Year", fontsize=15)

st.pyplot(fig)

