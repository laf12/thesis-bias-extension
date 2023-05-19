import matplotlib.pyplot as plt

def read_log_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        # Read the first line and split it into a list of entry names
        entry_names = file.readline().strip().split()
        
        # Read the remaining lines and process the data
        for line in file:
            # Split each line into individual data values
            values = line.strip().split()
            
            # Create a dictionary mapping each entry name to its corresponding value
            entry_data = dict(zip(entry_names, values))
            
            # Convert the numeric values to appropriate data types if needed
            for key in entry_data:
                if key != 'Frame':
                    entry_data[key] = float(entry_data[key])
            
            # Append the entry data to the list
            data.append(entry_data)
    
    return data

def plot_graph(data, data_loaded):
    frames = [entry['Frame'] for entry in data]
    values_A = [entry['A'] for entry in data]
    values_B = [entry['B'] for entry in data]
    values_C = [entry['C'] for entry in data]
    values_distance = [entry['distance'] for entry in data]

    # create a figure
    fig = plt.figure(figsize=(10, 10))
    # 2 subplots, one for the 3 areas and one for the clamp
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    # set the title of the figure
    fig.suptitle('Graphs for {}'.format(data_loaded['video']['output_name']))
    # set the title of the subplots
    ax1.set_title('Shear values for the 3 areas')
    ax2.set_title('Clamp distance')
    # set the x and y labels for the subplots
    ax1.set_xlabel('Frame number')
    ax1.set_ylabel('Shear value')
    ax2.set_xlabel('Frame number')
    ax2.set_ylabel('Distance')
    # set the x and y limits for the subplots
    ax1.set_xlim(0, len(data))
    ax1.set_ylim(0, max(values_A + values_B + values_C))
    ax2.set_xlim(0, len(data))
    ax2.set_ylim(0, max(values_distance) + 10)
    # plot the shear values for the 3 areas
    ax1.plot(values_A, label='Area A', color='red')
    ax1.plot(values_B, label='Area B', color='green')
    ax1.plot(values_C, label='Area C', color='blue')
    # plot the clamp distance
    ax2.plot(values_distance, label='distance', color='black')
    # add a legend to the subplots
    ax1.legend()
    ax2.legend()
    # save the figure
    fig.savefig('plots/{}.png'.format(data_loaded['video']['output_name'][:-4]))

