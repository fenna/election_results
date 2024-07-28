""" 
python script that uses percentage SP voters per postcode to visualize voting% 
it is important that the file contains two columns
postcode | number representing the postcode of the voting point (stembureau) and the percentage SP voters 
for instance the file 'Veendam.csv' about EP 2024 voting

	postcode	number
	9645 EN	    5.681818
	9641 LK	    4.741980
	9648 AA	    4.619388
	9631 TN	    4.424779
	9641 AW	    4.423868
	9641 AD	    4.145078
	9641 PJ	    3.906977
	9648 CV	    3.816794
	9644 VL	    3.543307
	9645 AR	    2.688172

The file is read in the load_data function 
in line df = pd.read_csv(f'{gemeente}.csv', sep=';', decimal=',')
please adjust this line if you have a different file format
"""

import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import folium

__author__ = 'F.Feenstra'

class ElectionResults:
    """
    A class to represent election results based on postcode.

    Attributes:
        postcode (str): The postcode for the location.
        number (float): The election result (percentage SP voters) associated with the postcode.
    """
    
    def __init__(self, postcode, number):
        """
        Initializes the ElectionResults object with postcode and number.

        Args:
            postcode (str): The postcode for the location.
            number (float): The election result (percentage SP voters) associated with the postcode
        """
        self.postcode = postcode
        self.number = number
        self._location = None

    @property
    def location(self):
        """
        Retrieves the geographic location (latitude and longitude) for the postcode.

        Returns:
            Location: A geopy Location object containing the latitude and longitude.
        
        Raises:
            ValueError: If the postcode is invalid.
        """
        if self._location is None:
            geolocator = Nominatim(user_agent="dutch_postcode_locator")
            self._location = geolocator.geocode(f"{self.postcode}, Netherlands")
            if self._location is None:
                raise ValueError("Invalid postcode")
        return self._location

    @property
    def latitude(self):
        """
        Retrieves the latitude for the postcode.

        Returns:
            float: The latitude of the location.
        """
        return self.location.latitude

    @property
    def longitude(self):
        """
        Retrieves the longitude for the postcode.

        Returns:
            float: The longitude of the location.
        """
        return self.location.longitude
    

def get_latitude(postcode, number):
    """
    Gets the latitude for a given postcode and number.

    Args:
        postcode (str): The postcode for the location.
        number (float): The election result number associated with the postcode.

    Returns:
        float: The latitude of the location, or None if the postcode is invalid.
    """
    try:
        result = ElectionResults(postcode, number)
        return result.latitude
    except:
        return None

def get_longitude(postcode, number):
    """
    Gets the longitude for a given postcode and number.

    Args:
        postcode (str): The postcode for the location.
        number (float): The election result number associated with the postcode.

    Returns:
        float: The longitude of the location, or None if the postcode is invalid.
    """
    try:
        result = ElectionResults(postcode, number)
        return result.longitude
    except:
        return None


def load_data(district):
    """
    Loads data from a CSV file for a given district and adds latitude and longitude.

    Args:
        district (str): The name of the district (used as the filename).

    Returns:
        DataFrame: A pandas DataFrame with the loaded data and added latitude and longitude columns.
    """
    # Load the dataframe
    df = pd.read_csv(f'{district}.csv', sep=';', decimal=',')
    # Add latitude and longitude columns
    df['latitude'] = df.apply(lambda row: get_latitude(row['postcode'], row['number']), axis=1)
    df['longitude'] = df.apply(lambda row: get_longitude(row['postcode'], row['number']), axis=1)
    return df


def create_map(df, district):
    """
    Creates a Folium map with circle markers for the given DataFrame and saves it as an HTML file.

    Args:
        df (DataFrame): The pandas DataFrame containing postcode, number, latitude, and longitude.
        district (str): The name of the district (used as the filename).
    """
    # Initialize the Folium map centered around the average coordinates
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)
    # Add circle markers to the map
    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['number'] * 2,  # Adjust the radius as needed
            popup=f"Postcode: {row['postcode']}\nSP-stem: {row['number']:.1f}%",
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)
    # Save map to HTML
    m.save(f"{district}.html")


if __name__ == '__main__':
    # Change this to the desired district
    district = 'Veendam'
    df = load_data(district)
    create_map(df)
