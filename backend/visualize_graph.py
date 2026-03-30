import json
import matplotlib.pyplot as plt

def visualize_structural_graph():
    print("Plotting geometry graph...")
    
    try:
        with open("structural_graph.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: structural_graph.json not found. Run test_module2.py first.")
        return

    # Extract nodes into a dictionary for quick coordinate lookup
    nodes = {node['id']: (node['x'], node['y']) for node in data['nodes']}
    
    plt.figure(figsize=(10, 8))
    plt.title("Module 2 Output: Structural Graph (Nodes & Edges)")

    # Plot Edges (Walls)
    for edge in data['edges']:
        source = nodes.get(edge['source'])
        target = nodes.get(edge['target'])
        
        if source and target:
            # Color code: Red for load-bearing, Blue for partition
            wall_type = data['wall_types'].get(edge['wall_id'], 'partition')
            color = 'red' if wall_type == 'load-bearing' else 'blue'
            linewidth = 3 if wall_type == 'load-bearing' else 1.5
            
            plt.plot([source[0], target[0]], [source[1], target[1]], 
                     color=color, linewidth=linewidth, zorder=1)

    # Plot Nodes (Junctions/Corners)
    for node_id, (x, y) in nodes.items():
        plt.scatter(x, y, color='green', s=50, zorder=2)
        
    # Formatting
    plt.gca().invert_yaxis() # Invert Y axis to match image coordinates
    plt.axis('equal') # Keep proportions accurate
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Custom Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', lw=3, label='Load-Bearing Wall'),
        Line2D([0], [0], color='blue', lw=1.5, label='Partition Wall'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='Junction Node')
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    print("Close the plot window to exit.")
    plt.show()

if __name__ == "__main__":
    visualize_structural_graph()