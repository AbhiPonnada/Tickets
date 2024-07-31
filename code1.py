import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the dataset
file_path = '/content/copy of data 1yr (1) 1.xlsx'
data = pd.read_excel(file_path)

# Step 2: Preprocess the data
# Convert 'Created Time' to datetime
data['Created Time'] = pd.to_datetime(data['Created Time'])

# Extract the day of the week and hour from 'Created Time'
data['Day of Week'] = data['Created Time'].dt.day_name()
data['Hour'] = data['Created Time'].dt.hour

# Aggregate data to count tickets by day and hour
ticket_counts = data.groupby(['Day of Week', 'Hour']).size().reset_index(name='Ticket Count')

# Order the days of the week
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ticket_counts['Day of Week'] = pd.Categorical(ticket_counts['Day of Week'], categories=ordered_days, ordered=True)
ticket_counts = ticket_counts.sort_values(['Day of Week', 'Hour'])

# Step 3: Plot the bar graph
plt.figure(figsize=(14, 8)) 

# Create a bar graph for each day
for day in ordered_days:
    day_data = ticket_counts[ticket_counts['Day of Week'] == day]
    plt.bar(day_data['Hour'] + (ordered_days.index(day) * 0.1), day_data['Ticket Count'], width=0.1, label=day)

plt.xlabel('Hour of the Day')
plt.ylabel('Number of Tickets')
plt.title('Number of Tickets by Hour and Day of the Week')
plt.xticks(range(24))
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
