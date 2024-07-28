# Election results % SP voters visualization

## installation
To use this project, you need to have Python installed along with the following libraries:

- pandas
- geopy
- folium
  
You can install the required libraries using the commandline
```{bash}
bash install_geo_env.sh
```

## usage
Prepare a CSV file named <district>.csv (for example Veendam.csv) with the following columns:

- postcode: The postcode for the location.
- number: The SP voter % per postcode

Modify the district variable in the main section of the script to match the name of your CSV file (without the .csv extension).
```{python}
if __name__ == '__main__':
    # Change this to the desired district
    district = 'Veendam'
    df = load_data(district)
    create_map(df)
```

Run the script to generate an HTML file with the map. 
After running the script with `district = 'Veendam'`, it will generate an HTML file `Veendam.html` with an interactive map showing the election results.

## viewing the map
To view the generated map, open the html file in a web browser. 
The map will display circle markers for each postcode with the election result numbers. Click on the circle to view the information.





