from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained AI model
with open("house_price_model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    location = request.form["location"]
    property_type = request.form["property_type"]

    area = float(request.form["area"])
    bedrooms = int(request.form["bedrooms"])
    bathrooms = int(request.form["bathrooms"])
    age = float(request.form["age"])
    parking = int(request.form["parking"])

    furnishing = request.form["furnishing"]

    # Amenities
    pool = 1 if request.form.get("pool") else 0
    gym = 1 if request.form.get("gym") else 0
    lift = 1 if request.form.get("lift") else 0
    security = 1 if request.form.get("security") else 0
    garden = 1 if request.form.get("garden") else 0
    clubhouse = 1 if request.form.get("clubhouse") else 0

    # Create property data
    house = pd.DataFrame([{
        "location": location,
        "property_type": property_type,
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age": age,
        "parking": parking,
        "furnishing": furnishing,
        "pool": pool,
        "gym": gym,
        "lift": lift,
        "security": security,
        "garden": garden,
        "clubhouse": clubhouse
    }])

    # AI prediction
    prediction = model.predict(house)[0]
    prediction = max(0, prediction)

    # Price per square foot
    price_per_sqft = prediction / area

    # Estimated range
    lower_price = prediction * 0.93
    upper_price = prediction * 1.07

    # Explanation
    reasons = []

    if area >= 2000:
        reasons.append(
            f"The large property area of {area:,.0f} sq.ft contributes positively to the estimated value."
        )
    elif area < 1000:
        reasons.append(
            f"The smaller property area of {area:,.0f} sq.ft keeps the estimated value relatively lower."
        )
    else:
        reasons.append(
            f"The property has a moderate area of {area:,.0f} sq.ft, which contributes to its overall valuation."
        )

    if bedrooms >= 4:
        reasons.append(
            f"The {bedrooms}-bedroom configuration increases the property's value because it offers more living space."
        )
    elif bedrooms <= 2:
        reasons.append(
            f"The {bedrooms}-bedroom configuration represents a smaller property configuration."
        )

    if bathrooms >= 3:
        reasons.append(
            f"Having {bathrooms} bathrooms adds value by providing greater convenience."
        )

    if property_type == "Villa":
        reasons.append(
            "The villa category generally commands a premium because of its larger space and exclusive property type."
        )
    elif property_type == "Independent House":
        reasons.append(
            "An independent house can receive a premium because it offers greater privacy."
        )
    else:
        reasons.append(
            "The apartment category is valued based on its size, configuration and location."
        )

    if furnishing == "Luxury":
        reasons.append(
            "Luxury furnishing contributes positively to the estimated property value."
        )
    elif furnishing == "Fully Furnished":
        reasons.append(
            "Full furnishing adds value because the property is ready for occupancy."
        )
    elif furnishing == "Semi Furnished":
        reasons.append(
            "Semi-furnished features provide additional value compared with an unfurnished property."
        )

    amenity_count = pool + gym + lift + security + garden + clubhouse

    if amenity_count >= 4:
        reasons.append(
            "The selected premium amenities significantly enhance the property's overall appeal."
        )
    elif amenity_count > 0:
        reasons.append(
            "The selected amenities provide additional value and convenience."
        )

    if age <= 5:
        reasons.append(
            "The relatively young property age supports a stronger valuation."
        )
    elif age >= 15:
        reasons.append(
            "The property's age has a downward effect compared with newer properties."
        )

    reasons.append(
        f"Location is an important factor, and the AI model considers {location} when estimating the property value."
    )

    return render_template(
        "result.html",
        price=f"₹{prediction:,.0f}",
        price_per_sqft=f"₹{price_per_sqft:,.0f}",
        lower=f"₹{lower_price:,.0f}",
        upper=f"₹{upper_price:,.0f}",
        location=location,
        property_type=property_type,
        area=area,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        reasons=reasons
    )


if __name__ == "__main__":
    app.run(debug=True)
    
