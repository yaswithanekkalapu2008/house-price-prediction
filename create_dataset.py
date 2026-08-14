import pandas as pd
import random

random.seed(42)

locations = {
    "Hyderabad": 4500,
    "Bangalore": 6000,
    "Chennai": 4000,
    "Mumbai": 10000,
    "Delhi": 7500,
    "Pune": 5000
}

property_types = {
    "Apartment": 1.0,
    "Independent House": 1.15,
    "Villa": 1.35
}

furnishing_types = {
    "Unfurnished": 0.90,
    "Semi Furnished": 1.00,
    "Fully Furnished": 1.12,
    "Luxury": 1.25
}

rows = []

for i in range(1000):

    location = random.choice(list(locations.keys()))
    property_type = random.choice(list(property_types.keys()))
    furnishing = random.choice(list(furnishing_types.keys()))

    area = random.randint(600, 4000)

    bedrooms = random.randint(1, 5)

    bathrooms = random.randint(1, 4)

    age = random.randint(0, 25)

    parking = random.randint(0, 3)

    pool = random.randint(0, 1)
    gym = random.randint(0, 1)
    lift = random.randint(0, 1)
    security = random.randint(0, 1)
    garden = random.randint(0, 1)
    clubhouse = random.randint(0, 1)

    base_price = locations[location] * area

    price = (
        base_price
        * property_types[property_type]
        * furnishing_types[furnishing]
    )

    price += bedrooms * 300000
    price += bathrooms * 200000
    price += parking * 150000

    price += pool * 500000
    price += gym * 250000
    price += lift * 150000
    price += security * 100000
    price += garden * 200000
    price += clubhouse * 250000

    price -= age * 50000

    # Small random variation
    price *= random.uniform(0.90, 1.10)

    rows.append([
        location,
        property_type,
        area,
        bedrooms,
        bathrooms,
        age,
        parking,
        furnishing,
        pool,
        gym,
        lift,
        security,
        garden,
        clubhouse,
        round(price)
    ])


columns = [
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
    "clubhouse",
    "price"
]

data = pd.DataFrame(rows, columns=columns)

data.to_csv("house_data.csv", index=False)

print("Dataset created successfully!")
print("Total houses:", len(data))
print("File saved as house_data.csv")
