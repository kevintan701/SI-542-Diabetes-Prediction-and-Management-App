import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib

# Load the diabetes data from CSV on the current directory
data = pd.read_csv('diabetes_data.csv')

# Preview the first few rows
print(data.head())

# Remove non-numeric columns before processing
data = data.drop(columns=['user_id', 'date'])

# Check for missing values and fill them if necessary
data.fillna(data.mean(), inplace=True)

# Split features and target variable
X = data.drop(columns=['risk_score'])  # Ensure lowercase 'risk_score' matches the CSV column name
y = data['risk_score']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the scaler for later use
joblib.dump(scaler, 'scaler.pkl')

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize the XGBoost Regressor
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5)

# Train the model
xgb_model.fit(X_train, y_train)

# Make predictions
y_pred = xgb_model.predict(X_test)

# Calculate RMSE
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Plot feature importance
xgb.plot_importance(xgb_model, max_num_features=10)
plt.show()

# Save the model
joblib.dump(xgb_model, 'diabetes_risk_model.pkl')
