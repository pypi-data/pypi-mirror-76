import requests
import json
import pandas as pd
import datetime
from IPython.display import clear_output
import plotly.express as px

"""# Vista APIs (Raw)  
-- Lowest Level ( JSON API response, as is )

```
vista_search_api()
vista_listing_api()
vista_listing_other_details_api()
vista_price_calculator_api()
```
"""

def vista_search_api(search_type='city',location="lonavala,%20maharashtra",guests=2,adults=2,childs=0,page_no=1):

  url = "https://searchapi.vistarooms.com/api/search/getresults"

  param={
    }

  payload = {
      
      "city": location,
      "search_type": "city",
      "checkin": "",
      "checkout": "",
      "total_guests": guests,
      "adults": adults,
      "childs": childs,
      "page": page_no,
      "min_bedrooms": 1,
      "max_bedrooms": 30,
      "amenity": [],
      "facilities": [],
      "price_start": 1000,
      "price_end": 5000000,
      "sort_by_price": ""
        
    }
  headers = {}

  response = requests.post(url, params=param, headers=headers, data=payload)
  search_data = json.loads(response.text.encode('utf8'))

  return search_data

def vista_listing_api(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2),
                         guest=3,adult=3,child=0):
  
  url = "https://v3api.vistarooms.com/api/single-property"

  param={
          'slug': slug,
          'checkin': checkin,
          'checkout': checkout,
          'guest': guest,
          'adult': adult,
          'child': child    
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  property_deets = json.loads(response.text.encode('utf8'))
  return property_deets

def vista_listing_other_details_api(slug='the-boulevard-villa'):

  url = "https://v3api.vistarooms.com/api/single-property-detail"

  param={
          'slug': slug,
      }

  payload = {}
  headers = {
  }
  
  response = requests.get(url, params=param, headers=headers, data = payload)
  property_other_deets = json.loads(response.text.encode('utf8'))
  return property_other_deets

def vista_price_calculator_api(property_id='710', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0):

  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')


  url = "https://v3api.vistarooms.com/api/price-breakup"
  
  param={
      'property_id': property_id,
      'checkin': checkin,
      'checkout': checkout,
      'guest': guest,
      'adult': adult,
      'child': child,   
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  pricing_deets = json.loads(response.text.encode('utf8'))
  return pricing_deets

"""# Search locations (Vista) 
-- Medium Level ( DataFrames & JSON )


```
vista_search_locations()
vista_search_locations_json()
```
"""

def vista_search_locations_json(locations=["lonavala,%20maharashtra"],guests=2,get_all=False):

  # Empty list to append (extend) all the data
  properties = []

  if get_all:
    locations = vista_locations()

  # Outer loop - for each location
  for location in locations:

    page_no = 1

    # Inner Loop - for each page in location ( acc to the Vista Search API )
    while True:

      clear_output(wait=True)
      print(f"Page {page_no} for {location.split('%20')[0]} ")

      # Vista API call (search)
      search_data = vista_search_api(location=location,guests=guests,page_no=page_no)

      # Break when you reach the last page for a location
      if not search_data['data']['properties']:
        break
        
      properties.extend(search_data['data']['properties'])
      page_no += 1


  return properties

# Retruns a DATAFRAME for the above functions & **DROP DUPLICATES (always use this for analysis)
def vista_search_locations(locations=["lonavala,%20maharashtra"],guests=2,get_all=False):
  villas = vista_search_locations_json(locations=locations, guests=guests,get_all=get_all)
  villas = pd.DataFrame(villas)
  villas = villas.drop_duplicates('id')

  return villas

"""# Listing Details
-- Medium Level ( JSON data, refined )

```
vista_listing()
vista_price_calculator()
```
"""

# Returns a JSON with the listing details
def vista_listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2)):

  print("Fetching ",slug)
  # Vista API call (listing)
  property_deets = vista_listing_api(slug=slug,guests=guests,checkin=checkin, checkout=checkout)
  
  # Get lat and long (diff API call)
  lat_long = vista_listing_other_details_api(slug)['data']['location']

  # Get pricing for various durations
  weekday_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(1))
  weekend_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(5),checkout=next_weekday(5)+datetime.timedelta(1))
  entire_week_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(7))
  entire_month_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(30))

  # Add the extra fields in response (JSON)
  property_deets['data']['slug'] = slug
  property_deets['data']['lat'] = lat_long['latitude']
  property_deets['data']['long'] = lat_long['longitude']
  property_deets['data']['checkin_date'] = checkin
  property_deets['data']['checkout_date'] = checkout
  property_deets['data']['weekday_pricing'] = weekday_pricing
  property_deets['data']['weekend_pricing'] = weekend_pricing
  property_deets['data']['entire_week_pricing'] = entire_week_pricing
  property_deets['data']['entire_month_pricing'] = entire_month_pricing
  property_deets['data']['price_per_room'] = property_deets['data']['price']['amount_to_be_paid']/property_deets['data']['property_detail']['number_of_rooms']

  return property_deets['data']

# Calculates the price for a duration (if unavailable, will automatically look for the next available dates) % Recursive function
def vista_price_calculator(property_id, checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0, depth=0):

  date_diff = (checkout-checkin).days

  # Set the exit condition for the recursion depth ( to avoid an endless recursion / slowing down the scripts )
  if date_diff < 7:
    depth_lim = 15
    next_hop = 7
  elif date_diff >= 7 and date_diff < 29:
    depth_lim = 7
    next_hop = 7
  else:
    depth_lim = 5
    next_hop = date_diff
    
  if depth==depth_lim:
    return f"Villa Probably Inactive, checked till {checkin}"
  
  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')

  # Vista API call (Calculation)
  pricing = vista_price_calculator_api(property_id=property_id, checkin=checkin, checkout=checkout, guest=guest, adult=adult, child=child)

  if 'error' in pricing.keys():

    # Recursion condition (Call self with next dates in case the dates are not available)
    if pricing['error'] == 'Booking Not Available for these dates':

      next_checkin = checkin + datetime.timedelta(next_hop)
      next_chekout = checkout + datetime.timedelta(next_hop)

      next_pricing = vista_price_calculator(property_id,checkin=next_checkin ,checkout=next_chekout,depth=depth+1)
      return next_pricing

    # For other errors (Like invalid listing ID)
    else:
      return pricing['error']
      
    return next_pricing
  else:
    return pricing['data']['price']

"""# Get ALL details about a list of all homes (Vista)
-- Medium\High Level ( DataFrames )

```
vista_master_dataframe(slugs)
added_villas_dataframe(old_slugs, new_slugs)
removed_villas_dataframe(old_slugs, new_slugs)
```
"""

# Use a list of slugs to generate a master DATAFRAME , this contains literally everything, ideal for any analysis on Vista
def vista_master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira'])):
  
  total_slugs = len(slugs)
  temp_progress_counter = 0
  villas_deets = []   

  for slug in slugs:
    villa_deets = vista_listing(slug=slug)
    villas_deets.append(villa_deets)
    villas_df = pd.DataFrame(villas_deets)

    temp_progress_counter += 1
    clear_output(wait=True)
    print("Done ",int((temp_progress_counter/total_slugs)*100),"%")

  prop_detail_df = pd.DataFrame(list(villas_df['property_detail']))
  agent_details_df =  pd.DataFrame(list(villas_df['agent_details']))
  price_df =  pd.DataFrame(list(villas_df['price']))

  literally_all_deets = pd.concat([prop_detail_df,villas_df,price_df,agent_details_df], axis=1)

  literally_all_deets = literally_all_deets.drop(['property_detail','mini_gallery', 'base_url',
       'agent_details', 'house_rule_pdf', 'mini_gallery_text',
       'seo','number_extra_guest', 'additionalcost',
       'days', 'min_occupancy', 'max_occupancy', 'amount_to_be_paid','total_guest',
       'extra_adult', 'extra_child', 'extra_adult_cost', 'extra_child_cost',
       'per_person','price','checkin_date','checkout_date','total_price','agent_short_words'], axis = 1)
  
  literally_all_deets['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in literally_all_deets['amenities']]
  literally_all_deets['weekday_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekday_pricing']]
  literally_all_deets['weekend_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekend_pricing']]
  literally_all_deets['entire_week_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_week_pricing']]
  literally_all_deets['entire_month_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_month_pricing']]
  
  return literally_all_deets

def added_villas_dataframe(old_slugs,new_slugs):
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  added_villas = []

  if added_slugs:
    added_villas = vista_master_dataframe(added_slugs) 

  return added_villas

def removed_villas_dataframe(old_slugs,new_slugs):
  removed_slugs = list(set(old_slugs).difference(set(new_slugs)))
  removed_villas =[]

  if removed_slugs:
    removed_villas = vista_master_dataframe(removed_slugs) 
  
  return removed_villas

"""# Graphs / Charts / Visuals
-- High Level ( Plotly Charts )  ( with parameters )
"""

def vista_map_all(mapbox_token='pk.eyJ1Ijoic2FyYW5ncHVyYW5kYXJlIiwiYSI6ImNrZG0wOTR2MzEzb20zM3M4cmVseDY5eGkifQ.RaYpNXAMapqZJITtOClHlA',json_download_link='https://www.dropbox.com/s/nouzn710ho9v4xc/vista_master.json?dl=1'):
  
  vista_data = pd.read_json(json_download_link)

  px.set_mapbox_access_token(mapbox_token)

  fig = px.scatter_mapbox(vista_data, lat="lat", lon="long",  color="number_of_rooms",hover_name="vista_name", size="price_per_room", hover_data=['property_type'],
                    color_continuous_scale='Bluered_r', size_max=20, zoom=6,height=500)
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  
  fig.show()

def ss_map_all(mapbox_token='pk.eyJ1Ijoic2FyYW5ncHVyYW5kYXJlIiwiYSI6ImNrZG0wOTR2MzEzb20zM3M4cmVseDY5eGkifQ.RaYpNXAMapqZJITtOClHlA'):
  
  ss_data = ss_latest()
  fig = px.scatter_mapbox(ss_data, lat="latitude", lon="longitude", hover_name="name", hover_data=["base_price", "priority"],
                          color_discrete_sequence=["#FBA919"], zoom=5, height=500)
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  fig.show()

def ss_vs_vista(mapbox_token='pk.eyJ1Ijoic2FyYW5ncHVyYW5kYXJlIiwiYSI6ImNrZG0wOTR2MzEzb20zM3M4cmVseDY5eGkifQ.RaYpNXAMapqZJITtOClHlA',vista_json_download_link='https://www.dropbox.com/s/nouzn710ho9v4xc/vista_master.json?dl=1'):
  
  px.set_mapbox_access_token(mapbox_token)
  
  vista_data = pd.read_json(vista_json_download_link)
  ss_data = ss_latest()

  vista_data['brand'] = "Vista"
  ss_data['brand'] = "SaffronStays"

  vista_trimmed = vista_data[['vista_name','villa_price','lat','long','brand']] 
  ss_trimmed = ss_data[['name','base_price','latitude','longitude','brand']]

  vista_trimmed.columns=['name','base_price','latitude','longitude','brand']
  ss_vista_villas = vista_trimmed.append(ss_trimmed,ignore_index=True)

  fig = px.scatter_mapbox(ss_vista_villas, lat="latitude", lon="longitude", hover_name="name", color="brand", hover_data=["base_price"],
                          color_discrete_sequence=["red","blue"], zoom=5, height=500,opacity=0.8,)
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  fig.show()

def vista_states_stacked_bar(mapbox_token='pk.eyJ1Ijoic2FyYW5ncHVyYW5kYXJlIiwiYSI6ImNrZG0wOTR2MzEzb20zM3M4cmVseDY5eGkifQ.RaYpNXAMapqZJITtOClHlA',vista_json_download_link='https://www.dropbox.com/s/nouzn710ho9v4xc/vista_master.json?dl=1'):

  vista_data = pd.read_json(vista_json_download_link)

  city_state_data = pd.DataFrame(vista_data.groupby(['state','city']).sum())
  city_state_data['state'] = [i[0] for i in city_state_data.index]
  city_state_data['city'] = [i[1] for i in city_state_data.index]

  fig = px.bar(city_state_data, x="state", y="number_of_rooms", color="city")
  fig.update_layout(margin={"t":10,"l":0,"b":0})
  fig.show()

"""# Helper Functions


```
next_weekday()
PROXY FOR SEARCH API
```
"""

def next_weekday(weekday=0, d=datetime.date.today()):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

# default - next monday

from bs4 import BeautifulSoup
from random import choice

def get_proxy():
  url = 'https://www.sslproxies.org/'
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html5lib')
  return {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}

def proxy_request(request_type, url, **kwargs):
  while 1:
    try:
      proxy = get_proxy()
      r = requests.request(request_type, url, proxy=proxies, timeout=5, **kwargs)
      break 
      return r
    except:
      pass

def vista_search_api_proxy(search_type='city',location="lonavala,%20maharashtra",guests=2,adults=2,childs=0,page_no=1):

  url = "https://searchapi.vistarooms.com/api/search/getresults"

  param={
    }

  proxies = get_proxy()

  proxies = {
      "https": "103.216.82.52:6666"
  }

  payload = {
        
        "city": location,
        "search_type": "city",
        "checkin": "",
        "checkout": "",
        "total_guests": guests,
        "adults": adults,
        "childs": childs,
        "page": 1,
        "min_bedrooms": 1,
        "max_bedrooms": 30,
        "amenity": [],
        "facilities": [],
        "price_start": 1000,
        "price_end": 5000000,
        "sort_by_price": ""
          
      }

  payload = "{\n    \"city\": \"lonavala, maharashtra\",\n    \"search_type\": \"city\",\n    \"checkin\": \"\",\n    \"checkout\": \"\",\n    \"total_guests\": 1,\n    \"adults\": 1,\n    \"childs\": 0,\n    \"page\": 1,\n    \"min_bedrooms\": 1,\n    \"max_bedrooms\": 30,\n    \"amenity\": [],\n    \"facilities\": [],\n    \"price_start\": 1000,\n    \"price_end\": 5000000,\n    \"sort_by_price\": \"\"\n}"
  
  headers = {
      'authority': 'searchapi.vistarooms.com',
      'pragma': 'no-cache',
      'cache-control': 'no-cache',
      'accept': 'application/json, text/plain, */*',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
      'content-type': 'application/json',
      'origin': 'https://www.vistarooms.com',
      'sec-fetch-site': 'same-site',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://www.vistarooms.com/maharashtra/villas-in-lonavala',
      'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'Cookie': '__cfduid=d6e43e667320a570f3748afb4cee79f6b1596831185; laravel_session=Yvb89jaR2AGpblmNqYaNmuNNbhMay5j8btAzlZr1'
    }

  response = requests.post(url, params=param, headers=headers, data=payload, proxies=proxies)
  search_data = response.text.encode('utf8')

  return search_data

"""# Get Saved Data ( DataFrames on the cloud )
Use these to avoid the fetching time (Updated every week)
"""

def ss_latest():
  url = "https://www.saffronstays.com/items_catalogue.php"

  response = requests.get(url)
  response_data = response.text.encode('utf8')

  csv_endpoint = str(response_data).split('`')[1]
  csv_download_url = "https://www.saffronstays.com/"+csv_endpoint

  ss_data = pd.read_csv(csv_download_url)

  return ss_data


def vista_latest():
  vista_data = pd.read_csv('https://www.dropbox.com/s/9ep1ibv01mwo2ch/vista_all_details_8_aug.csv?dl=1')
  vista_data = vista_data.drop(columns='Unnamed: 0')
  return vista_data


def vista_locations():
  locations = ["lonavala, maharashtra","goa, goa","alibaug, maharashtra","nainital, uttarakhand","chail, himanchal-pradesh","manali, himachal-pradesh","shimla, himanchal%20pradesh","ooty, tamil%20nadu","coorg, karnataka","dehradun, uttarakhand","jaipur, rajasthan","udaipur, rajasthan","mahabaleshwar, maharashtra","nashik, maharashtra"]
  return locations

"""# Heavy Functions 
Only execute weekly


```
vista_get_entire_dataframe()
```
"""

# Only use this once a month - this script takes 1 hour to run
def vista_get_entire_dataframe():
  vista_search_data = vista_search_df(get_all=True)
  slugs = vista_search_data['slug']
  vista_final_dataframe = vista_master_dataframe(slugs)
  return vista_final_dataframe

"""# TEST"""

def final_test():
  ss_latest()
  vista_latest()
  vista_locations()
  vista_search_locations_json(locations=["nainital, uttarakhand"],guests=2,get_all=False)
  vista_search_locations(locations=["nainital, uttarakhand"],guests=2,get_all=False)
  vista_listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2))
  vista_listing_other_details_api(slug='the-boulevard-villa')
  vista_price_calculator(property_id='310', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0)
  next_weekday(weekday=0, d=datetime.date.today())
  vista_master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira']))
  vista_map_all()
  ss_map_all()
  ss_vs_vista()

  return "All Good :)"

final_test()

"""# End"""