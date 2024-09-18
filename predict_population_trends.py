import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv('DanCu.csv')

# change data type
data['Diện tích(km2)'] = data['Diện tích(km2)'].str.replace(',', '.').astype(float)
data['Mật độ dân số (Người/km2)'] = data['Mật độ dân số (Người/km2)'].str.replace(',', '.').astype(float)

features = data[['Năm', 'Diện tích(km2)', 'Tổng_số_cặp_kết_hôn', 'Tỷ_lệ_sinh']]
target = data['Mật độ dân số (Người/km2)']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

model = LinearRegression(fit_intercept=True, n_jobs=15, positive=False)

# train model
model.fit(X_train, y_train)

# test model
y_pred = model.predict(X_test)

# evaluate model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# test predict
future_year = pd.DataFrame({'Năm': [2023], 'Diện tích(km2)': [3359.84], 'Tổng_số_cặp_kết_hôn': [45000], 'Tỷ_lệ_sinh': [2.1]})
future_density = model.predict(future_year)

print(f'Dự đoán mật độ dân số năm 2023: {future_density[0]} người/km2')