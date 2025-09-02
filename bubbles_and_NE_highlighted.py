import baltic as bt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import matplotlib as mpl

# Load your tree using baltic's loadNewick function
ll = bt.loadNewick('/content/tree_2025.nwk')

# Load your metadata
metadata = pd.read_csv('/content/updated_metadata.tsv', sep='\t')
print("Metadata shape:", metadata.shape)
print("Metadata columns:", metadata.columns.tolist())
print("\nRegion value counts:")
print(metadata['Region'].value_counts())

# Filter for Nebraska regions and 2023 samples
ne_regions = ['NE_Central', 'NE_West', 'NE_East']
ne_metadata = metadata[metadata['Region'].isin(ne_regions)]

# Extract year from date column and filter for 2023
def extract_year(date_str):
    if pd.isna(date_str):
        return None
    # For YYYY-XX-XX format, just take the first 4 characters
    import re
    year_match = re.search(r'^(\d{4})', str(date_str))
    if year_match:
        return int(year_match.group(1))
    return None

metadata['year'] = metadata['date'].apply(extract_year)
ne_2023 = metadata[(metadata['Region'].isin(ne_regions)) & (metadata['year'] == 2023)]

print(f"\nFiltered to {len(ne_2023)} Nebraska 2023 samples")
if len(ne_2023) > 0:
    print("NE 2023 Region breakdown:")
    print(ne_2023['Region'].value_counts())

# Create strain-to-metadata mapping
strain_to_region = dict(zip(metadata['strain'], metadata['Region']))
strain_to_year = dict(zip(metadata['strain'], metadata['year']))
strain_to_date = dict(zip(metadata['strain'], metadata['date']))

# Create a mapping for Nebraska 2023 samples
ne_2023_strains = set(ne_2023['strain'])

# Convert dates to decimal years for time axis
def date_to_decimal_year(date_str):
    if pd.isna(date_str):
        return None
    try:
        # Parse YYYY-XX-XX format
        parts = str(date_str).split('-')
        if len(parts) >= 3:
            year = int(parts[0])
            month = int(parts[1]) if parts[1] != 'XX' else 6  # Default to mid-year if XX
            day = int(parts[2]) if parts[2] != 'XX' else 15    # Default to mid-month if XX

            # Convert to decimal year
            from datetime import datetime
            date_obj = datetime(year, month, day)
            year_start = datetime(year, 1, 1)
            year_end = datetime(year + 1, 1, 1)
            year_fraction = (date_obj - year_start).total_seconds() / (year_end - year_start).total_seconds()
            return year + year_fraction
        else:
            return int(parts[0])  # Just return year if only year provided
    except:
        return extract_year(date_str)  # Fallback to year extraction

# Add decimal years to metadata
metadata['decimal_year'] = metadata['date'].apply(date_to_decimal_year)
strain_to_decimal_year = dict(zip(metadata['strain'], metadata['decimal_year']))

# First, set absoluteTime for all nodes based on tree structure
# We'll use a recursive approach to set times from tips to root
def set_node_times(node):
    if node.branchType == 'leaf':
        # For tips, use the date from metadata
        if hasattr(node, 'name') and node.name:
            decimal_year = strain_to_decimal_year.get(node.name, None)
            if decimal_year is not None:
                node.absoluteTime = decimal_year
            else:
                node.absoluteTime = 2020  # Default
    else:
        # For internal nodes, set time based on children
        if hasattr(node, 'children') and node.children:
            # First, ensure all children have times set
            for child in node.children:
                set_node_times(child)
            # Set node time as the average of children times minus branch length
            child_times = [child.absoluteTime for child in node.children if hasattr(child, 'absoluteTime')]
            if child_times:
                node.absoluteTime = min(child_times) - (node.length if hasattr(node, 'length') else 0.1)
            else:
                node.absoluteTime = 2010  # Default for internal nodes

# Apply time setting to all nodes
for node in ll.Objects:
    set_node_times(node)

# Add traits to tree nodes for coloring
for node in ll.Objects:
    if hasattr(node, 'name') and node.name:
        strain = node.name
        region = strain_to_region.get(strain, 'other')
        year = strain_to_year.get(strain, None)

        # Create traits dictionary
        if not hasattr(node, 'traits'):
            node.traits = {}

        # Assign special highlighting for Nebraska 2023
        if strain in ne_2023_strains:
            if region == 'NE_Central':
                node.traits['highlight_color'] = '#FCB614'  # Yellow/Gold
                node.traits['is_ne_2023'] = True
                node.traits['ne_region'] = 'NE_Central'
            elif region == 'NE_West':
                node.traits['highlight_color'] = '#005E63'  # Teal
                node.traits['is_ne_2023'] = True
                node.traits['ne_region'] = 'NE_West'
            elif region == 'NE_East':
                node.traits['highlight_color'] = '#AD122A'  # Red
                node.traits['is_ne_2023'] = True
                node.traits['ne_region'] = 'NE_East'
            else:
                node.traits['highlight_color'] = '#CCCCCC'  # Light grey
                node.traits['is_ne_2023'] = False
                node.traits['ne_region'] = 'Other'
        else:
            # Muted colors for non-2023 samples
            node.traits['highlight_color'] = '#CCCCCC'  # Light grey
            node.traits['is_ne_2023'] = False
            node.traits['ne_region'] = 'Other'

        node.traits['region'] = region
        node.traits['year'] = year
    else:
        # For internal nodes without names
        if not hasattr(node, 'traits'):
            node.traits = {}
        node.traits['highlight_color'] = '#CCCCCC'
        node.traits['is_ne_2023'] = False
        node.traits['ne_region'] = 'Other'

# Set up the figure - compressed height
fig, ax = plt.subplots(figsize=(20, 10), facecolor='w')

# Define x attribute function
x_attr = lambda k: k.absoluteTime

# Define color function for branches - color tip branches only
def branch_color_func(k):
    if k.is_leaf() and k.traits.get('is_ne_2023', False):
        return k.traits['highlight_color']
    else:
        return '#CCCCCC'  # All other branches grey

# Define color function for tips
tip_color_func = lambda k: k.traits['highlight_color'] if (k.is_leaf() and k.traits.get('is_ne_2023', False)) else '#BBBBBB'

# Compress the tree vertically BEFORE plotting
y_compression_factor = 0.6
ll.drawTree()  # Set up coordinates first
for node in ll.Objects:
    if hasattr(node, 'y'):
        node.y = node.y * y_compression_factor
ll.ySpan = ll.ySpan * y_compression_factor

# Use Baltic's plotTree method with branch coloring
ll.plotTree(ax, x_attr=x_attr, colour=branch_color_func, width=2)

# Use Baltic's plotPoints method for tip coloring
ll.plotPoints(ax, x_attr=x_attr, size=lambda k: 100 if k.traits.get('is_ne_2023', False) else 30,
              colour=tip_color_func, zorder=100)

# Customize the plot
ax.set_ylim(-10, ll.ySpan + 10)
ax.set_xlim(1993, 2025)
[ax.spines[loc].set_visible(False) for loc in ['left', 'right', 'top']]

ax.grid(axis='x', ls='-', color='grey', alpha=0.3)
ax.tick_params(axis='y', size=0)
ax.tick_params(axis='x', labelsize=16)
ax.set_yticklabels([])
ax.set_xlabel('Time (Years)', fontsize=18)
ax.set_title('Phylogenetic Tree - Nebraska 2023 Samples Highlighted', fontsize=20, fontweight='bold', pad=20)

# Create custom legend in top left
from matplotlib.patches import Patch
legend_elements = [
    plt.scatter([], [], c='#FCB614', s=150, edgecolors='black', linewidth=1, label='NE_Central (2023)'),
    plt.scatter([], [], c='#005E63', s=150, edgecolors='black', linewidth=1, label='NE_West (2023)'),
    plt.scatter([], [], c='#AD122A', s=150, edgecolors='black', linewidth=1, label='NE_East (2023)'),
    plt.scatter([], [], c='#BBBBBB', s=75, edgecolors='black', linewidth=0.5, label='Other samples'),
]

ax.legend(handles=legend_elements, loc='upper left', fontsize=16,
          title='Sample Types', title_fontsize=18, frameon=True, fancybox=True, shadow=True,
          bbox_to_anchor=(0.02, 0.98))

plt.tight_layout()
plt.show()

# Print statistics
print(f"\nTree Statistics:")
print(f"Total tips in tree: {len(list(filter(lambda k: k.branchType == 'leaf', ll.Objects)))}")
print(f"Total internal nodes: {len(list(filter(lambda k: k.branchType == 'node', ll.Objects)))}")

# Check which Nebraska 2023 samples are in the tree
tree_tips = set([tip.name for tip in ll.Objects if hasattr(tip, 'branchType') and tip.branchType == 'leaf'])
ne_2023_in_tree = ne_2023_strains.intersection(tree_tips)
print(f"\nNebraska 2023 samples in tree: {len(ne_2023_in_tree)}")
if len(ne_2023_in_tree) > 0:
    print("Sample names:", list(ne_2023_in_tree)[:10], "..." if len(ne_2023_in_tree) > 10 else "")

# Count by region in tree
ne_2023_regions_in_tree = {}
for strain in ne_2023_in_tree:
    region = strain_to_region.get(strain, 'unknown')
    ne_2023_regions_in_tree[region] = ne_2023_regions_in_tree.get(region, 0) + 1

print(f"Nebraska 2023 samples by region in tree:")
for region, count in ne_2023_regions_in_tree.items():
    print(f"  {region}: {count}")

# Optional: Save the figure
# plt.savefig('phylogenetic_tree_nebraska_2023_highlighted.png', dpi=300, bbox_inches='tight')
