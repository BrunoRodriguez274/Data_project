import pandas as pd
from faker import Faker
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from geopy.geocoders import Nominatim
import string
import time
import polars as pl

fake = Faker('es_MX')
rng = np.random.default_rng(seed=274)

def get_zipcodes(lat_, lon_):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="bruno")

    # Coordinates
    location = geolocator.reverse(f"{lat_}, {lon_}", addressdetails=True)

    # Extract ZIP code
    if location and 'postcode' in location.raw['address']:
        zipcode = location.raw['address']['postcode']
        print(zipcode)
    else:
        print("Zip code not found")
        return None
    
    return int(zipcode)

def eval_name(name_: str) -> bool:

    if " " not in name_:
        return True

    name1, name2 = name_.split()[0], name_.split()[-1]

    if (name1[-1] in ["s","o"] and name2[-1] == "a") or (name1[-1]=="a" and name2[-1] in ["s","o"]):
        
        return True
    
    else:
        return False
    
def create_name(gender_: bool) -> str:
    
    names = [fake.first_name_female, fake.first_name_male]

    conditions = True
    while conditions:
        temp = []
        for i in range(rng.choice([1,2])):
            temp.append(names[int(gender_)]())

        name = " ".join(temp)
        if len(name.split()) >= 3:
            continue

        conditions = eval_name(name)

    return name

def bounded_normal_integer(mean_, var_, l_bound_ = None, u_bound_ = None) -> int:

    value = int(rng.normal(mean_, var_))

    if l_bound_ is not None:
    
        value = max(value, l_bound_)

    if u_bound_ is not None:
    
        value = min(value, u_bound_)
    return value

def compute_centroid(points : list) -> float:

    A = 0
    Cx = 0
    Cy = 0

    points.append(points[0])
    for i in range(len(points)-1):

        x_i, y_i = points[i]
        x_ii, y_ii = points[i+1]
        
        print(x_i, y_i, "---->", x_ii, y_ii)

        A += ((x_i*y_ii)-(x_ii*y_i))
        Cx += (x_i+x_ii)*((x_i*y_ii)-(x_ii*y_i))
        Cy += (y_i+y_ii)*((x_i*y_ii)-(x_ii*y_i))
        
    A_tot = (1/2)*A
    Cx = (1/(6*A_tot))*Cx
    Cy = (1/(6*A_tot))*Cy

    return (Cx, Cy)

def create_customer(geography_metadata_, n_=1):

    # customer_x = []
    # customer_y = []
    # customers_data = []
    # for customer in range(n_):
    print("Creating customer")

    key = rng.choice(list(geography_metadata_.keys()))
    xc, yc = geography_metadata_[key]["centroids"]
    lat = [p["point"][0] for p in geography_metadata_["Marfil"]["points"]]
    lon = [p["point"][1] for p in geography_metadata_["Marfil"]["points"]]
    customer_x = rng.normal(xc, np.std(lat))
    customer_y = rng.normal(yc, np.std(lon))
    
    retries = 0
    while True:
        try:
            zipcode = get_zipcodes(customer_x, customer_y)
            time.sleep(3)
            break
        except:
            print("retry", retries)
            time.sleep(3)
            retries +=1
            if retries >3:
                zipcode= None
                break

    gender = rng.choice([True, False])
    birth_date = dt.datetime.date(rng.choice(pd.date_range("1950-01-01", "2019-01-01").to_list()))
    letters = [i for i in string.ascii_lowercase]

    data = {"id": None,
            "name" : create_name(gender),
        "last_name" : " ".join([fake.last_name(), fake.last_name()] ),
        "gender" : gender, 
        "birth_date" : dt.datetime(rng.choice([bounded_normal_integer(1990, 8, 1950), bounded_normal_integer(2005, 3, 1950)], p= [0.5,0.5], size=1)[0],\
                                    birth_date.month,\
                                        birth_date.day).date(),
        "lat" : customer_x,
        "lon" : customer_y,
        "zipcode" : zipcode,
        "email" : rng.choice(letters) + rng.integers(8,17)*"*"+ rng.choice(letters) +"@" + rng.choice(["gmail.com", "hotmail.com"]),
        "phone_number" : "(473)" + str(rng.integers(1000000,10000000)),
        "created_at" : dt.datetime.now(),
        "status" : "Active",
        "profile_type" : None,
        "updated_at" : dt.datetime.now()
        }
    
    #customers_data.append(tuple(data.values()))
    #customers_data.append(data)
    
    return data