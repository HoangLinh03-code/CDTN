import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

file_path = 'SanPhamMeVaBe.csv'
data = pd.read_csv(file_path)

# rename columns
data_cleaned = data.rename(columns={'Product Name': 'ProductName', 'Product Price': 'ProductPrice', 'Catergory': 'Category'})

# split data (80% train, 20% test)
X = data_cleaned[['ProductName', 'ProductPrice']]
y = data_cleaned['Category']

X_train, X_test, y_train, y_test = train_test_split(X['ProductName'], y, test_size=0.2, random_state=42)

# create pipeline
model = make_pipeline(TfidfVectorizer(), RandomForestClassifier(n_estimators=100, random_state=42))

# train model
model.fit(X_train, y_train)

# test model
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))
