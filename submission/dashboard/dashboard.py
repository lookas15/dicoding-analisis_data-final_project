import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_data(file_path):
    return pd.read_csv(file_path)

day_clean_df = load_data("submission\dashboard\cleaned_day.csv")

day_clean_df["day_type"] = day_clean_df.apply(
    lambda row: "Holiday" if row["isHoliday"] == 1 else "Working Day" if row["isWorkingDay"] == 1 else "Weekend", axis=1
)

day_type_rentals = day_clean_df.groupby("day_type")["total_rental"].mean().round().astype(int).reset_index()
weather_rentals = day_clean_df.groupby("weather_desc")["total_rental"].mean().round().astype(int).reset_index()

st.header('📊Bike Sharing Dashboard 📊')

st.subheader("A. Bike Rentals by Day Type")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="day_type", y="total_rental", data=day_type_rentals, palette="magma", ax=ax)
ax.set_xlabel("Day Type")
ax.set_ylabel("Average Total Rentals")
ax.set_title("Total Bike Rentals: Holidays - Working Days - Weekends")
st.pyplot(fig)
st.markdown("Explanation: **More bike rentals on working days & weekends than holidays.**")

st.subheader("B. Bike Rentals by Weather Condition")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weather_desc", y="total_rental", data=weather_rentals, palette="PuBu", ax=ax)
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Total Rentals")
ax.set_title("Bike Rentals Across Different Weather Conditions")
plt.xticks(rotation=45)
st.pyplot(fig)
st.markdown("Explanation")
st.markdown("- **Clear weather leads to the highest number of rentals.**")
st.markdown("- **Rainy or snowy weather significantly reduces rentals.**")
