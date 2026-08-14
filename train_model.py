import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


# Load dataset
data = pd.read_csv("house_data.csv")

# Features
features = [
    "location",
    "property_type",
    "area",
    "bedrooms",
    "bathrooms",
    "age",
    "parking",
    "furnishing",
    "pool",
    "gym",
    "lift",
    "security",
    "garden",
    "clubhouse"
]

X = data[features]
y = data["price"]


# Categorical features
categorical_features = [
    "location",
    "property_type",
    "furnishing"
]

# Numerical features
numerical_features = [
    "area",
    "bedrooms",
    "bathrooms",
    "age",
    "parking",
    "pool",
    "gym",
    "lift",
    "security",
    "garden",
    "clubhouse"
]


# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# Machine Learning model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


# Complete pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Train
print("Training AI model...")

pipeline.fit(X_train, y_train)


# Test
predictions = pipeline.predict(X_test)

r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print()
print("================================")
print("   LUXORA AI MODEL RESULTS")
print("================================")
print("R² Score:", round(r2, 4))
print("Mean Absolute Error:", round(mae, 2))
print("================================")


# Save model
with open("house_price_model.pkl", "wb") as file:
    pickle.dump(pipeline, file)

print()
print("AI model saved successfully!")
print("File: house_price_model.pkl")
