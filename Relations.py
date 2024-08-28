import json
import pandas as pd

# File paths
json_file_path = r"Original.cim"
output_csv_path = r"Tabular_Relationships.csv"

# Function to extract connection details
def extract_connections(json_data):
    connections = []
    model = json_data.get('model', {})
    relationships = model.get('relationships', [])
    
    for relationship in relationships:
        connection = {
            'fromTable': relationship.get('fromTable', ''),
            'fromColumn': relationship.get('fromColumn', ''),
            'toTable': relationship.get('toTable', ''),
            'toColumn': relationship.get('toColumn', '')
        }
        connections.append(connection)
    
    return connections

# Load the JSON data from the BIM file
with open(json_file_path, 'r', encoding='utf-8') as file:
    bim_data = json.load(file)

# Extract connection details
connections = extract_connections(bim_data)

# Save the connection details to a CSV file
df = pd.DataFrame(connections)
df.to_csv(output_csv_path, index=False)

print("Connections data saved to CSV successfully!")