import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Constants
total_sectors = 48000000
reserved_sectors = 10000000

# Parse files from the memory folder
memory_folder = './memory'
used_sectors = set()
#Create location[] to store start and end points of each file, which used for plotting
location = []
for file_name in os.listdir(memory_folder):
    file_path = os.path.join(memory_folder, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            start_address = (content.split('FLASH_SECTORS_START_ADDRESS = ')[1].split('\n')[0])
            stop_address = (content.split('FLASH_SECTORS_STOP_ADDRESS = ')[1].split('\n')[0])
            #check if the start_adress and stop_adress are numbers, if not, dafault setting will be 0
            if start_address.isdigit():
                start_address = int(content.split('FLASH_SECTORS_START_ADDRESS = ')[1].split('\n')[0])
                stop_address = int(content.split('FLASH_SECTORS_STOP_ADDRESS = ')[1].split('\n')[0]) 
                used_sectors.update(range(start_address, stop_address + 1))
            else:
                start_address=0
                stop_address=0
            
            location.append(start_address)
            location.append(stop_address)

# Calculate memory usage
used_sectors = len(used_sectors)
free_memory = total_sectors - used_sectors - reserved_sectors
# Print calculations
print ("Total flash sectors used:", used_sectors, "sectors")
print ("Free flash sectors:", free_memory,"sectors")
used_percentage = ((used_sectors+reserved_sectors) / total_sectors) * 100
free_percentage = 100-used_percentage
print(f"Used Memory: {used_percentage:.2f}%")
print(f"Free Memory: {free_percentage:.2f}%")
#print("Location =",location)

# Plotting data
#create flash memery sectors
flash_memory = [{'status': 'reversed', 'start':0, 'end':reserved_sectors}]
for i in range(0,len(location),2):
    flash_memory.append({'status': 'used', 'start':location[i], 'end':location[i+1]})
# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 2))
# Set axis limits and labels
ax.set_xlim(0, total_sectors)
ax.set_ylim(0, 1)
ax.set_xticks([0,total_sectors])
# Hide y-axis ticks
ax.set_yticks([])  
# Add sectors as rectangles
for sector in flash_memory:
    status = sector['status']
    start = sector['start']
    end = sector ['end']
    color = 'green' if status == 'reversed' else 'red'
    rect = patches.Rectangle((start, 0), end-start, 1, facecolor=color, edgecolor='black')
    ax.add_patch(rect)
# Add legend
used_patch = patches.Patch(color='red', label='Used')
reversed_patch = patches.Patch(color='green', label='Reversed')
free_patch = patches.Patch(color='white', label='Free')
ax.legend(handles=[used_patch, reversed_patch, free_patch], loc='upper right')
# Set title
ax.set_title('Flash Memory Sectors')
# Display the plot
plt.show()