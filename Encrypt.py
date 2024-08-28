import json
import re
import pandas as pd

# Define the file path
file_path = r"Encrypted.bim"
csv_path = r"changes.csv"

# Initialize a list to store changes
changes_log = []

def remove_spaces(name):
    """Remove spaces from the name and return the updated name."""
    return re.sub(r"[ ().+{}]+", '', name)

def log_change(instance_level, field_name, before, after, table_name=None, data_type=None):
    """Log changes to the changes_log list."""
    change_entry = {
        'Instance Level': instance_level,
        'Field Name': field_name,
        'Before': before,
        'After': after,
        'Table Name': table_name if field_name == 'name' and instance_level.endswith('columns[list]') else None,
        'Data Type': data_type if field_name == 'name' and instance_level.endswith('columns[list]') else None
    }
    changes_log.append(change_entry)

def update_json(json_data, instance_level='Root', table_name=None):
    """Recursively update the JSON data."""
    if isinstance(json_data, dict):
        if instance_level.endswith('.measures[list]'):
            return

        if 'name' in json_data and instance_level.endswith('tables[list]'):
            table_name = json_data['name']

        if 'name' in json_data and 'columns' in json_data:
            before = json_data['name']
            after = remove_spaces(before)
            data_type = json_data.get('dataType')
            # if before != after:
            log_change(instance_level, 'name', before, after, table_name, data_type)
            json_data['name'] = after
        
        if 'name' in json_data and 'sourceColumn' in json_data:
            before = json_data['name']
            source_column = json_data.get('sourceColumn')
            after = remove_spaces(source_column)
            data_type = json_data.get('dataType')
            # if before != after:
            log_change(instance_level, 'name', before, after, table_name, data_type)
            json_data['name'] = after
        
        # Recursively update any nested dictionaries or lists
        for key, value in json_data.items():
            if isinstance(value, (dict, list)):
                update_json(value, instance_level=f"{instance_level}.{key}", table_name=table_name)
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, (dict, list)):
                update_json(item, instance_level=f"{instance_level}[list]", table_name=table_name)

def save_changes_to_csv():
    """Save the changes log to an CSV file."""
    df = pd.DataFrame(changes_log)
    df.to_csv(csv_path, index=False)

def main():
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        bim_data = json.load(file)
 
    # Update the JSON data
    update_json(bim_data)
 
    # Save the updated JSON data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(bim_data, file, indent=2)
    
    # Save the changes log to an Excel file
    save_changes_to_csv()
    
    print("File updated and changes logged successfully!")

if __name__ == "__main__":
    main()