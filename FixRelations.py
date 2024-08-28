import pandas as pd

# Load the CSV file
csv_path = r"export (3).csv"
relations_df = pd.read_csv(csv_path)

# Dictionary to store relationships
graph = {}

# Function to build the tree from the CSV data
def build_graph(df):
    for _, row in df.iterrows():
        from_node = (row['fromTable'], row['fromColumn'])
        to_node = (row['toTable'], row['toColumn'])

        if from_node not in graph:
            graph[from_node] = {'DataType': row['DataType_fromColm'], 'Connections': []}
        if to_node not in graph:
            graph[to_node] = {'DataType': row['DataType_toColm'], 'Connections': []}

        # Add bidirectional relationships
        graph[from_node]['Connections'].append(to_node)
        graph[to_node]['Connections'].append(from_node)

# Function to propagate data types through the graph
def propagate_data_types(node, visited=None):
    if visited is None:
        visited = set()

    visited.add(node)
    node_data_type = graph[node]['DataType']

    for connected_node in graph[node]['Connections']:
        if connected_node not in visited:
            connected_node_data_type = graph[connected_node]['DataType']
            if connected_node_data_type != node_data_type:
                # Correct the data type
                graph[connected_node]['DataType'] = node_data_type
            propagate_data_types(connected_node, visited)

# Function to update the DataFrame with the corrected data types
def update_dataframe(df):
    for i, row in df.iterrows():
        from_node = (row['fromTable'], row['fromColumn'])
        to_node = (row['toTable'], row['toColumn'])

        df.at[i, 'DataType_fromColm'] = graph[from_node]['DataType']
        df.at[i, 'DataType_toColm'] = graph[to_node]['DataType']

# Build the tree graph from the CSV data
build_graph(relations_df)

# Propagate data types throughout the graph
# for node in graph:
#     if node not in visited:
#         propagate_data_types(node)
for node in graph:
    visited = set()  # Initialize visited set for each new node
    propagate_data_types(node, visited)

# Update the DataFrame with the corrected data types
update_dataframe(relations_df)

# Save the updated DataFrame to a new CSV file
output_csv_path = r"CorrectedRelations.csv"
relations_df.to_csv(output_csv_path, index=False)

print("Relationships corrected and saved to export_corrected.csv")