import json
import pandas as pd

# File paths
log_file_path = r"export (3).csv"
bim_file_path = r"Encrypted.bim"
output_bim_file_path = r"Decryted.bim"
source_bim_file_path = r"Original.bim"

# Function to read the Excel log file
def read_changes_log(log_file_path):
    df = pd.read_csv(log_file_path)
    return df

# Function to update table names
def update_table_names(json_data, changes):
    tables = json_data.get('model', {}).get('tables', [])
    for index, row in changes.iterrows():
        if pd.isna(row['Table Name']) or row['Table Name'].strip() == "":
            before_value = row['Before']
            after_value = row['After']
            for table in tables:
                if table.get('name') == after_value:
                    table['name'] = before_value

# Function to update column names within corresponding tables
def update_column_names(json_data, changes):
    tables = json_data.get('model', {}).get('tables', [])
    for index, row in changes.iterrows():
        if not pd.isna(row['Table Name']) and row['Table Name'].strip() != "":
            table_name = row['Table Name'].strip()
            field_name = row['Field Name']
            before_value = row['Before']
            after_value = row['After']
            data_type = row.get('Data Type')  # Extract the data type from the row

            for table in tables:
                if table.get('name') == table_name:
                    columns = table.get('columns', [])
                    for column in columns:
                        if column.get('name') == after_value:
                            column['name'] = before_value
                            if data_type and 'dataType' in column:
                                column['dataType'] = data_type  # Update the data type if provided

# Function to copy hierarchies from the source BIM to the target BIM
def copy_hierarchies(source_bim, target_bim):
    source_tables = {table['name']: table for table in source_bim['model']['tables']}
    target_tables = {table['name']: table for table in target_bim['model']['tables']}

    for table_name, source_table in source_tables.items():
        if table_name in target_tables:
            target_table = target_tables[table_name]
            if 'hierarchies' in source_table:
                if 'hierarchies' not in target_table:
                    target_table['hierarchies'] = []
                # Copy all hierarchies from source to target
                target_table['hierarchies'].extend(source_table['hierarchies'])

    return target_bim

# Function to load a BIM file
def load_bim_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to save a BIM file
def save_bim_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def main():
    # Load the changes log
    changes_log = read_changes_log(log_file_path)
    
    # Load the JSON data from the BIM file
    bim_data = load_bim_file(bim_file_path)
    
    # Apply the changes to the JSON data
    update_table_names(bim_data, changes_log)
    update_column_names(bim_data, changes_log)
    
    # Load the source BIM file for copying hierarchies
    source_bim = load_bim_file(source_bim_file_path)
    
    # Copy hierarchies from the source BIM to the updated BIM data
    bim_data = copy_hierarchies(source_bim, bim_data)
    
    # Save the updated JSON data back to a new BIM file
    save_bim_file(output_bim_file_path, bim_data)
    
    print("File updated successfully!")

if __name__ == "__main__":
    main()