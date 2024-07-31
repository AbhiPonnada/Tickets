import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load the dataset (assuming it contains ticket data)
data = pd.read_csv('/content/customer_support_tickets.csv')

# Step 2: Preprocess the data
# Focus on relevant columns
relevant_columns = ['Ticket Type', 'Date of Purchase']
data = data[relevant_columns]

# Convert 'Date of Purchase' to datetime and extract Month and Year
data['Date of Purchase'] = pd.to_datetime(data['Date of Purchase'])
data['Month'] = data['Date of Purchase'].dt.month
data['Year'] = data['Date of Purchase'].dt.year

# Aggregate data to count tickets by type, year, and month
ticket_counts = data.groupby(['Ticket Type', 'Year', 'Month']).size().reset_index(name='Ticket Count')

# Step 3: Prepare data for training
X = ticket_counts[['Year', 'Month', 'Ticket Type']]
y = ticket_counts['Ticket Count']

# Encode categorical variables (Ticket Type)
X = pd.get_dummies(X, columns=['Ticket Type'], drop_first=True)

# Step 4: Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train a Random Forest regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Predict future ticket volumes for the next 12 months
# Determine the next 12 months starting from the current month
current_year = pd.Timestamp.now().year
current_month = pd.Timestamp.now().month
future_months = [(current_month + i - 1) % 12 + 1 for i in range(1, 13)]  # Get next 12 months
future_years = [current_year + (current_month + i - 1) // 12 for i in range(1, 13)]  # Adjust year accordingly

# Create future data DataFrame
future_data = pd.DataFrame({
    'Year': future_years,
    'Month': future_months,
})

# Add columns for each ticket type based on X.columns
for col in X.columns[2:]:
    future_data[col] = 0  # Initialize with zeros to match dummy variable format

# Ensure 'Ticket Type' column is categorical and consistent with training data
for col in X.columns[2:]:
    if col not in future_data.columns:
        future_data[col] = 0

# Ensure columns are in the same order as X
future_data = future_data[X.columns]

# Predict ticket counts for future scenarios
predicted_counts = []
for ticket_type in X.columns[2:]:
    future_data_ticket_type = future_data.copy()
    future_data_ticket_type[ticket_type] = 1  # Set the current ticket type to 1
    predicted_counts_ticket_type = model.predict(future_data_ticket_type)
    predicted_counts.append(predicted_counts_ticket_type)

predicted_counts = np.array(predicted_counts).T  # Transpose to get (num_months, num_ticket_types)

# Step 7: Visualize predicted ticket volumes for each ticket type in each month
plt.figure(figsize=(16, 10))

# Plotting bar chart for each ticket type in each month
bar_width = 0.2
index = range(len(future_data))

for i, ticket_type in enumerate(X.columns[2:]):  # Iterate over each ticket type
    plt.bar([x + i * bar_width for x in index], predicted_counts[:, i], width=bar_width, label=ticket_type)

plt.xlabel('Month')
plt.ylabel('Predicted Ticket Count')
plt.title('Predicted Volume of Tickets by Type for Next 12 Months')
plt.xticks(index, [f"{future_data['Month'][i]}-{future_data['Year'][i]}" for i in range(len(future_data))], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
