import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# Đọc dữ liệu từ file CSV
data = pd.read_csv('DanCu.csv')

# Chuyển đổi dấu phẩy thành dấu chấm trong số liệu
data['Diện tích(km2)'] = data['Diện tích(km2)'].str.replace(',', '.').astype(float)
data['Mật độ dân số (Người/km2)'] = data['Mật độ dân số (Người/km2)'].str.replace(',', '.').astype(float)

# Chọn các cột cần thiết
features = data[['Năm', 'Diện tích(km2)', 'Tổng_số_cặp_kết_hôn', 'Tỷ_lệ_sinh']]
target = data['Mật độ dân số (Người/km2)']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Khởi tạo mô hình
model = LinearRegression(fit_intercept=True, n_jobs=15, positive=False)

# Huấn luyện mô hình
model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá mô hình
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Dự đoán mật độ dân số cho năm 2023
future_year = pd.DataFrame({'Năm': [2023], 'Diện tích(km2)': [3359.84], 'Tổng_số_cặp_kết_hôn': [45000], 'Tỷ_lệ_sinh': [2.1]})
future_density = model.predict(future_year)

print(f'Dự đoán mật độ dân số năm 2023: {future_density[0]} người/km2')