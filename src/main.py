import pandas as pd
import matplotlib.pyplot as plt
from logConfigure import configure_logger
import os
from dotenv import load_dotenv
import requests
import json

app_logger = configure_logger("api_app_logger")

def get_env_vars() -> dict:
    try :
        load_dotenv("config/vars.env")
        api_call_parms = {
        'appid': os.getenv("API_KEY"),
        'url' : os.getenv("URL1"),
        'zip' : os.getenv("ZIP_CODE"),
        'units' : os.getenv("UNITS"),
        'q': os.getenv("Q"),
        }
        app_logger.info("API CALL PARAMETERS Retrived from ENV.")
    except Exception as exp:
        app_logger.error(f"An Error occured: {exp}")
    return api_call_parms

def get_api_data(api_call_parms: dict) -> pd.DataFrame:
    '''
    This function call Weather API to collect the weaher forcat every 3 hours for 5 days

    Parameters: 
        api_call_parms: dict
    Exceptions:
        Exception object

    Retuen: 
        data_df: data frame object.
    '''
    app_logger.info("Fitching Weather API data..")

    url = api_call_parms['url']
    payload={
        'zip':api_call_parms['zip'],
        'units': api_call_parms['units'],
        'appid': api_call_parms['appid'],
    }
    data_list = []
    data_dict = {}
    try:
        forcast_call_response = requests.get(url,payload) 
        forcast_row_data =forcast_call_response.json()
        write_data_to_file(forcast_row_data)
        data_list = forcast_row_data['list']
        for item in data_list:
            data_dict[item['dt_txt']] = {
                'TEMP': item['main']['temp'],
                'Weather_Status':item['weather'][0]['main'],
            }

    except Exception as exp:
        app_logger.error(f"Error processing Weather API call: ->{exp}")

    data_df = pd.DataFrame.from_dict(data_dict, orient='index')
    data_df.index = pd.to_datetime(data_df.index)

    return data_df

def write_data_to_file(forcast_row_data:dict) -> None:
    '''
    This function write the weather forcast data to a json file
    
    parameters:
        forcast_row_data (Dict): weather data forcast every 3 hours for 5 days. 
    Exception:
        FileNotFoundError , FileExistsError, Exception

    Return: 
        None.
    '''
    try:
        with open("forcast_data.json",'w') as jfile:
            json.dump(forcast_row_data, jfile, indent=4)
            app_logger.info("forcast data saved to: forcast_data.json")
    except (FileNotFoundError , FileExistsError, Exception) as exp:
        app_logger.error(f"Error writing data to json file: {exp}")

def plot_save_dataf(weather_data_df: pd.DataFrame) -> None:
    '''
    This function plot the weather data using matplotlib.

    Parameters:
        weather_data_df (Dict): weather data forcast every 3 hours for 5 days.  
    Exceptions:

    Return: None.

    '''
    try:
        # Plot the temperature over time 
        # (use the index as the x-axis)
        plt.figure(figsize=(10,6))
        plt.plot(weather_data_df.index, weather_data_df['TEMP'],marker='o', color='g', label='Temp (F)')

        plt.title('Tempreture in 5 days')
        plt.xlabel('Date')
        plt.ylabel('Temp (F) ')
        
        # Display grid and legend
        plt.grid(True)
        plt.legend()

        plt.xticks(rotation=45) # Rotate the x-axis labels for better readability
        plt.tight_layout() # Adjust the layout to avoid overlap
        plt.savefig("Forcast_plot_figure.png")
        plt.show()
    except Exception as exp:
        app_logger.error(f"Plotting Error occured: {exp}")


def main():

    env_vars=get_env_vars()
    weather_data_df= get_api_data(env_vars)
    #print(weather_data_df)
    plot_save_dataf(weather_data_df)

if __name__ == "__main__":
    main()