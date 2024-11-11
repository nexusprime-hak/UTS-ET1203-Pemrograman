import json

def parse_satellite_data_1():
    norad_n2yo = ""
    try:
        with open("./satellite_data.json", 'r') as f:
            data = json.load(f)

        print("Data loaded succesfully:", data)
        satellites = data.get("satellites")
        for satellite in satellites:
            satellite_name = satellite.get("name", "")
            satellite_id = satellite.get("sat_id", "")
            norad_n2yo += f"{satellite_id}|{satellite_name},"
        
        norad_n2yo = norad_n2yo[:-1]
        return norad_n2yo

    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error loading JSON: {error}")
        return None 

        