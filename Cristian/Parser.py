import json

def parse_json(file_path):  
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    files_dict = data["files"]
    first_file_key = next(iter(files_dict))
    file_data = files_dict[first_file_key]
    
    RelevantData = {}
    for key, value in file_data.items():
        print(f"Key: {key}")
        if isinstance(value, list):
            filtered_list = [item for item in value if isinstance(item, dict) and "line" in item]
            if filtered_list:  # Only store if it has matching items
                RelevantData[key] = filtered_list
        
        elif isinstance(value, dict):
            filtered_dict = {k: v for k, v in value.items() if "line" in k}
            if filtered_dict:  # Only store if it has matching keys
                RelevantData[key] = filtered_dict

    
    functionData = RelevantData.get("functions")
    functionFirst = functionData[0]
    print(functionFirst)
    for index, element in enumerate(functionFirst):
        print(f"Index: {index}, Element: {element}")

file_path = "C:/Users/nyros/GreenAI/GreenAI_Scrapwork/Cristian/profile.json"
parse_json(file_path)

    