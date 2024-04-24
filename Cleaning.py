import pandas as pd
import re

def convert_par_nuit_to_number(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path)
    
    # Compile a regex pattern to extract the numeric value for "par nuit" prices
    pattern = re.compile(r'(\$\d+) \npar nuit')
    
    # Define a function to convert price text to numeric value
    def to_numeric(value):
        match = pattern.search(value)
        if match:
            # Convert the dollar amount from string to integer
            return int(match.group(1).replace('$', ''))
        return None  # Return None if "par nuit" is not found or for any non-matching cases

    # Apply the function to the 'Price' column
    data['Numeric Price'] = data['Price'].apply(to_numeric)
    
    # Optionally save the modified DataFrame back to CSV or return it
    # data.to_csv('/mnt/data/cleaned_airbnb_prices.csv', index=False)
    return data
    # Return or save the modified DataFrame
    return data
# Load all datasets
df_listings = pd.read_csv('airbnb_listings.csv')
df_beds = pd.read_csv('airbnb_listings_beds.csv')
df_links = pd.read_csv('airbnb_listings_links.csv')
df_names = pd.read_csv('airbnb_listings_names.csv')
df_ratings = pd.read_csv('airbnb_listings_ratings.csv')
df_prices = pd.read_csv('airbnb_prices.csv')

# Clean the prices
#df_prices['cleaned_price'] = df_prices['Price'].apply(clean_price)
df_prices=convert_par_nuit_to_number('airbnb_prices.csv')
# Combine all DataFrames
df_combined = pd.concat([df_listings, df_beds, df_links, df_names, df_ratings, df_prices], axis=1)

# Remove any duplicate columns
df_combined = df_combined.loc[:,~df_combined.columns.duplicated()]

# Save the combined DataFrame to an Excel file
df_combined.to_excel('combined_airbnb_listings.xlsx', index=False)
