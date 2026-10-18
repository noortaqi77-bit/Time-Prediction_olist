"""
Olist - Delivery Time Prediction Demo App
-------------------------------------------
This app will be simulating a simple online checkout where the customer pickes the product, 
enters the delivery location and order date. The app will use the trained machine learning model to predict how many days the delivery will take. 

Disclaimer: this is not an actual checout page its only purpose is to show the time delivery estimator model

"""

import streamlit as st                      
from datetime import date, timedelta       
from geopy.distance import geodesic         # calculates the distance in km between two map points
import pandas as pd                         
import joblib                              


st.set_page_config(page_title="Olist Store", layout="wide")



#Streamlit re-runs this whole file every time the user clicks something.
#Loading the model is slow, so we wrap it in a function with @st.cache_resource.
#This tells Streamlit: "load it once, then remember it" instead of reloading on every click. 

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")


model = load_model()

# cities.csv: used for the State and City dropdowns, and to get the customer's location
cities = pd.read_csv("cities.csv")

#catalog.csv: the products. One row per category and seller --> because the same category can be sold by many different sellers. 

catalog = pd.read_csv("catalog.csv")


st.title("Olist Store")
st.subheader("1. Choose your product")

# Build the dropdown list from the catalog --> category names sorted A to Z.
categories = sorted(catalog["category_english"].unique())
choice = st.selectbox("Product category", categories)

# How many items the customer wants (between 1 and 10)
quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1)



st.subheader("2. Delivery details")
name = st.text_input("Full name")

# State dropdown --> taken from ceties.csv
state = st.selectbox("State", sorted(cities["customer_state"].unique()))

# to keep  only the cities that belong to the chosen state:
state_cities = cities[cities["customer_state"] == state]
city = st.selectbox("City", sorted(state_cities["city"].unique()))


# techincally this is not how it will be,  the main reason for this function is to show the model's functionallity
st.subheader("3. When would you like to order?")
# min_value=date.today() means the customer cannot pick a date in the past
order_date = st.date_input("Order date", value=date.today(), min_value=date.today())


st.subheader("4. Delivery estimate")

# The prediction only runs when this button is clicked. so the app would not lag every time the user changes something
if st.button("Check delivery estimate"):

    # Find where the customer is, then take the row of the chosen city and read its latitude and   longitude.
    city_row = state_cities[state_cities["city"] == city].iloc[0]
    cust_lat = city_row["cust_lat"]
    cust_lng = city_row["cust_lng"]

    # Find the nearest seller of this product because the seller's location matters
    sellers = catalog[catalog["category_english"] == choice]

    best_distance = None   # the shortest distance found so far
    best_seller = None     # the seller who has that shortest distance

    # a loop to check all sellers
    for i in range(len(sellers)):
        seller = sellers.iloc[i]

        # Distance in km between this seller and the customer
        d = geodesic((seller["sell_lat"], seller["sell_lng"]),
                     (cust_lat, cust_lng)).km

        # Keep this seller if it is the first one, or closer than the best so far
        if best_distance is None or d < best_distance:
            best_distance = d
            best_seller = seller

     
    #The model expects the SAME columns it was trained on, so we create a one-row table with exactly those columns.
    #Price, freight and weight are typical values for one item, so we multiply by the quantity.  
    row = pd.DataFrame([{
        "distance_km": best_distance,                                    # seller-to-customer distance
        "price": best_seller["price"] * quantity,                        # total price
        "freight": best_seller["freight"] * quantity,                    # total shipping cost
        "overal_weight_g": best_seller["overal_weight_g"] * quantity,    # total weight in grams
        "number_of_items": quantity,                                     # how many items
        "purchase_month": order_date.month,                              # month of the order
        "purchase_day": order_date.day,                                  # day of the month
        "product_category_name": best_seller["product_category_name"],    # original (Portuguese) name, as in training
        "customer_state": state,                                         # where the order is going
        "seller_state": best_seller["seller_state"],                     # where the order ships from
    }])

    # model.predict returns the predicted number of days.
    # We round it to a whole number and make sure it is at least 1 day.
    days = max(1, round(float(model.predict(row)[0])))

    #Streamlit forgets variables after every click.
    #st.session_state works like a notepad: it keeps these values
    #so they are still available when the customer clicks "Order Now" later.
    st.session_state["days"] = days
    st.session_state["eta"] = order_date + timedelta(days=days)  
    st.session_state["summary"] = f"{quantity} x {choice} to {city}, {state}"



# This block only appears after an estimate has been calculated
if "days" in st.session_state:

    # Read the saved values back from the memory
    days = st.session_state["days"]
    eta = st.session_state["eta"]
    summary = st.session_state["summary"]

    # Show the estimate BEFORE the customer orders, like a real store would
    st.info(f"Estimated delivery for {summary}: **{days} days** (around {eta})")

    
    st.subheader("5. Place your order")

    if st.button("Order Now"):
        # The customer must enter a name before ordering
        if name == "":
            st.warning("Please enter your name.")
        else:
            # Confirmation screen, showing the same estimate again
            st.success(f"Thank you, {name}! Your order ({summary}) is confirmed.")
            st.info(f"It will arrive in about **{days} days** (around {eta}).")