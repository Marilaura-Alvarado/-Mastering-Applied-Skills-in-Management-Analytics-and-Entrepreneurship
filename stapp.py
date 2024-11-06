
import os
import json
import time
import requests
import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st

st.header('ISS over Earth', divider='rainbow')

st.write('ISS crew:')
api_url_crew = 'http://api.open-notify.org/astros.json'
response_crew = requests.get(api_url_crew)
crew_data = response_crew.json()
iss_crew = [person['name'] for person in crew_data['people'] if person['craft'] == 'ISS']
crew_df = pd.DataFrame(iss_crew, columns=['Crew Member'])

st.table(crew_df)

st.divider()

st.write('Demo of ISS coordinates over the time on a map:')

api_url_loc = 'http://api.open-notify.org/iss-now.json'
n_points = 10
positions = []
for p in range(n_points):
    response = requests.get(api_url_loc)
    d = response.json()
    uts = d['timestamp']
    d['timestamp'] = datetime.utcfromtimestamp(uts).strftime('%Y-%m-%d %H:%M:%S')
    positions.append(d)
    time.sleep(1)
coords = [
    (float(x['iss_position']['latitude']), float(x['iss_position']['longitude']))
    for x in positions
]
map_data = pd.DataFrame(
    coords,
    columns=['lat', 'lon']
)
st.map(map_data)
