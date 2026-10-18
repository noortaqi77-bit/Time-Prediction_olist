# Time-Prediction_olist


### problem statement:

Olist’s  delivery estimates are conservative, which may discourage customers from completing their purchases, potentially leading to lost sales.

**Our objective** is to predict delivery time in days using historical order data, including product characteristics, order value, freight costs, and seller–customer locations, to support more accurate delivery estimates and reduce potential cart abandonment.


### **Data** :  
Brazilian E-Commerce Public Dataset by Olist  
(Tables used: orders, customers, order_items, products, sellers, geolocation.)

link=(https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### Date cleaning & preprocessing :

- Data Integration: Combined order, customer, product, seller, and location information into one using Olist’s dataset.

- Data Transformation: Organised the data so each row represented one order and calculated delivery time in days.

- Missing Values: Filled in missing information using imputation methods.

- Data Encoding & Scaling: Converted categorical information into a format the models could understand and scaled numerical features to support model training.


## Files :
Data_Cleaning

.gitignore

Data_Cleaning.zip

How_Far_Off_Is_the_Delivery_Estimate.png

README.md

all_models_comparison2.png

app.py

catalog.csv

cities.csv

states.csv

requirements.txt


##### streamlit App link :(https://time-predictionolist-7sbassgpvyey8uymvhx3am.streamlit.app/](https://the-data-solutions.streamlit.app/)
