# Apply time setting to all nodes
for node in ll.Objects:
    set_node_times(node)

# Check how many nodes are using default values
nodes_using_2020 = 0
nodes_using_2010 = 0
total_leaf_nodes = 0
total_internal_nodes = 0
missing_names = []

for node in ll.Objects:
    if node.branchType == 'leaf':
        total_leaf_nodes += 1
        if node.absoluteTime == 2020:
            nodes_using_2020 += 1
            if hasattr(node, 'name'):
                missing_names.append(node.name)
            else:
                missing_names.append("NO_NAME")
    else:
        total_internal_nodes += 1
        if node.absoluteTime == 2010:
            nodes_using_2010 += 1

print(f"\n⚠️  DEFAULT TIME USAGE REPORT:")
print(f"Leaf nodes using default 2020: {nodes_using_2020} out of {total_leaf_nodes}")
print(f"Internal nodes using default 2010: {nodes_using_2010} out of {total_internal_nodes}")

if nodes_using_2020 > 0:
    print(f"\nSamples missing dates (using 2020 default):")
    for name in missing_names[:10]:  # Show first 10
        print(f"  - {name}")
    if len(missing_names) > 10:
        print(f"  ... and {len(missing_names) - 10} more")

if nodes_using_2010 > 0:
    print(f"\n⚠️  {nodes_using_2010} internal nodes couldn't calculate times from children!")

print(f"Total nodes# Set absoluteTime for all nodes based on tree structure")
def set_node_times(node):
    if node.branchType == 'leaf':
        if hasattr(node, 'name') and node.name:
            decimal_year = strain_to_decimal_year.get(node.name, None)
            if decimal_year is not None:
                node.absoluteTime = decimal_year
                node.time_source = 'metadata'
            else:
                node.absoluteTime = 2020
                node.time_source = 'default_2020'
        else:
            node.absoluteTime = 2020
            node.time_source = 'default_2020_no_name'
    else:
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                set_node_times(child)
            child_times = [child.absoluteTime for child in node.children if hasattr(child, 'absoluteTime')]
            if child_times:
                node.absoluteTime = min(child_times) - (node.length if hasattr(node, 'length') else 0.1)
                node.time_source = 'calculated'
            else:
                node.absoluteTime = 2010
                node.time_source = 'default_2010'
        else:
            node.absoluteTime = 2010
            node.time_source = 'default_2010_no_children'

# Apply time setting to all nodes
for node in ll.Objects:
    set_node_times(node)

# Analyze time source statistics
time_source_counts = {}
leaf_time_sources = {}
internal_time_sources = {}

for node in ll.Objects:
    source = getattr(node, 'time_source', 'unknown')
    time_source_counts[source] = time_source_counts.get(source, 0) + 1

    if node.branchType == 'leaf':
        leaf_time_sources[source] = leaf_time_sources.get(source, 0) + 1
    else:
        internal_time_sources[source] = internal_time_sources.get(source, 0) + 1

print("\n" + "="*50)
print("TIME ASSIGNMENT ANALYSIS")
print("="*50)

print(f"\nOverall time source breakdown:")
for source, count in sorted(time_source_counts.items()):
    percentage = (count / len(ll.Objects)) * 100
    print(f"  {source}: {count} nodes ({percentage:.1f}%)")

for node in ll.Objects:
    if hasattr(node, 'name') and node.name:
        strain = node.name
        broad_region = strain_to_broad_region.get(strain, 'Other')

        if not hasattr(node, 'traits'):
            node.traits = {}

        # Set color based on broad region
        node.traits['color'] = REGION_COLORS.get(broad_region, UNMC_COLORS['grey'])
        node.traits['broad_region'] = broad_region

        # Mark if this is a UNMC sample
        node.traits['is_unmc'] = strain in UNMC_SAMPLES

        node.traits['original_region'] = strain_to_region.get(strain, 'unknown')

# Set up the figure
fig, ax = plt.subplots(figsize=(20, 10), facecolor='w')

# Get tree dimensions and set up layout
import baltic as bt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import matplotlib as mpl

# UNMC Color Palette - Most distinct colors
UNMC_COLORS = {
    'green_2': '#A1B426',      # Bright Green
    'orange_1': '#F26721',     # Dark Orange (more distinct than orange_2)
    'blue_1': '#002957',       # Dark Blue (more distinct than blue_2)
    'green_1': '#656515',      # Dark Green (very distinct)
    'grey': '#CCCCCC'          # Light grey
}

# Define your UNMC samples to highlight
UNMC_SAMPLES = {
    'UNMC0008', 'UNMC0009', 'UNMC0014', 'UNMC0020', 'UNMC0185', 'UNMC0270',
    'UNMC0299', 'UNMC0261', 'UNMC0267', 'UNMC0015', 'UNMC0011', 'UNMC0016',
    'UNMC0017', 'UNMC0013', 'UNMC0730', 'UNMC0567', 'UNMC0019', 'UNMC0209',
    'UNMC0265', 'UNMC0728', 'UNMC0010', 'UNMC0575', 'UNMC0538', 'UNMC0012',
    'UNMC0707', 'UNMC0282', 'UNMC0699', 'UNMC0678', 'UNMC0706'
}

# Regional groupings (combining all NE_ regions into Midwest)
def get_broad_region(region):
    if pd.isna(region):
        return 'Other'

    region_str = str(region)

    # Group NE_ regions as Midwest (since they're Nebraska samples)
    if region_str.startswith('NE_'):
        return 'Midwest'
    elif region_str == 'Northeast':
        return 'Northeast'
    elif region_str == 'West':
        return 'West'
    elif region_str == 'Midwest':
        return 'Midwest'
    elif region_str == 'South':
        return 'South'
    else:
        return 'Other'

# Color assignments - More distinct colors to avoid green confusion
REGION_COLORS = {
    'Northeast': UNMC_COLORS['green_2'],    # 1524 samples - Bright Green
    'West': UNMC_COLORS['orange_1'],        # 1228 samples - Dark Orange
    'Midwest': UNMC_COLORS['blue_1'],       # 475 + 271 = 746 samples - Dark Blue
    'South': '#129DBF',                     # 371 samples - Light Blue (from Blue 2)
    'Other': UNMC_COLORS['grey']            # Any remaining - Grey
}

# Load your tree using baltic's loadNewick function
ll = bt.loadNewick('/content/tree_2025.nwk')

# Load your metadata
metadata = pd.read_csv('/content/updated_metadata.tsv', sep='\t')
print("Metadata shape:", metadata.shape)
print("Metadata columns:", metadata.columns.tolist())

# Add broad region groupings
metadata['broad_region'] = metadata['Region'].apply(get_broad_region)
print("\nBroad region distribution:")
print(metadata['broad_region'].value_counts())

# Check UNMC samples
unmc_metadata = metadata[metadata['strain'].isin(UNMC_SAMPLES)]
print(f"\nUNMC samples found in metadata: {len(unmc_metadata)}")
print("UNMC samples by broad region:")
print(unmc_metadata['broad_region'].value_counts())

# Create strain-to-metadata mappings
strain_to_region = dict(zip(metadata['strain'], metadata['Region']))
strain_to_broad_region = dict(zip(metadata['strain'], metadata['broad_region']))
strain_to_date = dict(zip(metadata['strain'], metadata['date']))

# Convert dates to decimal years for time axis
def extract_year(date_str):
    if pd.isna(date_str):
        return None
    import re
    year_match = re.search(r'^(\d{4})', str(date_str))
    if year_match:
        return int(year_match.group(1))
    return None

def date_to_decimal_year(date_str):
    if pd.isna(date_str):
        return None
    try:
        parts = str(date_str).split('-')
        if len(parts) >= 3:
            year = int(parts[0])
            month = int(parts[1]) if parts[1] != 'XX' else 6
            day = int(parts[2]) if parts[2] != 'XX' else 15

            from datetime import datetime
            date_obj = datetime(year, month, day)
            year_start = datetime(year, 1, 1)
            year_end = datetime(year + 1, 1, 1)
            year_fraction = (date_obj - year_start).total_seconds() / (year_end - year_start).total_seconds()
            return year + year_fraction
        else:
            return int(parts[0])
    except:
        return extract_year(date_str)

metadata['decimal_year'] = metadata['date'].apply(date_to_decimal_year)
strain_to_decimal_year = dict(zip(metadata['strain'], metadata['decimal_year']))

# Set absoluteTime for all nodes based on tree structure
def set_node_times(node):
    if node.branchType == 'leaf':
        if hasattr(node, 'name') and node.name:
            decimal_year = strain_to_decimal_year.get(node.name, None)
            if decimal_year is not None:
                node.absoluteTime = decimal_year
            else:
                node.absoluteTime = 2020
    else:
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                set_node_times(child)
            child_times = [child.absoluteTime for child in node.children if hasattr(child, 'absoluteTime')]
            if child_times:
                node.absoluteTime = min(child_times) - (node.length if hasattr(node, 'length') else 0.1)
            else:
                node.absoluteTime = 2010

# Apply time setting to all nodes
for node in ll.Objects:
    set_node_times(node)

# Draw ALL branches in grey (boss's preference - much cleaner!)
for node in ll.Objects:
    if hasattr(node, 'parent') and node.parent:
        x = node.absoluteTime
        y = node.y
        x_parent = node.parent.absoluteTime
        y_parent = node.parent.y

        # ALL branches are grey for simplicity
        branch_color = '#CCCCCC'

        # Draw horizontal branch
        ax.plot([x_parent, x], [y, y], color=branch_color, linewidth=1.5, zorder=10, alpha=0.7)

        # Draw vertical connector
        if hasattr(node.parent, 'children') and len(node.parent.children) > 1:
            sibling_ys = [child.y for child in node.parent.children]
            ax.plot([x_parent, x_parent], [min(sibling_ys), max(sibling_ys)],
                   color='#CCCCCC', linewidth=1.5, zorder=9, alpha=0.7)

# Debug: Print some sample data to see what's happening
print("Debug info:")
sample_count = 0
for node in ll.Objects:
    if hasattr(node, 'branchType') and node.branchType == 'leaf' and sample_count < 5:
        strain = getattr(node, 'name', 'no_name')
        broad_region = strain_to_broad_region.get(strain, 'NOT_FOUND')
        color = REGION_COLORS.get(broad_region, 'NO_COLOR')
        print(f"  Sample {sample_count}: {strain} -> {broad_region} -> {color}")
        sample_count += 1

print(f"Total leaf nodes: {len([n for n in ll.Objects if n.branchType == 'leaf'])}")
print(f"Strain mapping examples: {list(strain_to_broad_region.items())[:5]}")
print(f"Region colors: {REGION_COLORS}")

# Plot tip points with explicit color debugging
for node in ll.Objects:
    if hasattr(node, 'branchType') and node.branchType == 'leaf':
        strain = getattr(node, 'name', None)
        if strain:
            broad_region = strain_to_broad_region.get(strain, 'Other')
            is_unmc = strain in UNMC_SAMPLES

            if is_unmc:
                # UNMC samples: larger nodes with black circles, special red color
                ax.scatter(node.absoluteTime, node.y, s=120, c='#AD122A',
                          zorder=20005, edgecolors='black', linewidth=2, alpha=1.0)
            else:
                # Regular samples: smaller nodes, colored by region
                color = REGION_COLORS.get(broad_region, UNMC_COLORS['grey'])
                ax.scatter(node.absoluteTime, node.y, s=40, c=color,
                          zorder=20001, alpha=0.8, edgecolors='none')
        else:
            # No name - plot as grey
            ax.scatter(node.absoluteTime, node.y, s=40, c=UNMC_COLORS['grey'],
                      zorder=20001, alpha=0.8, edgecolors='none')

# Customize the plot
ax.set_ylim(-10, ll.ySpan + 10)
ax.set_xlim(1993, 2025)
[ax.spines[loc].set_visible(False) for loc in ['left', 'right', 'top']]

ax.grid(axis='x', ls='-', color='grey', alpha=0.3)
ax.tick_params(axis='y', size=0)
ax.tick_params(axis='x', labelsize=16)
ax.set_yticklabels([])
ax.set_xlabel('Time (Years)', fontsize=18)
ax.set_title('Phylogenetic Tree - UNMC Samples Highlighted by US Region', fontsize=20, fontweight='bold', pad=20)

# Create custom legend - UNMC samples now red
legend_elements = [
    plt.scatter([], [], c=UNMC_COLORS['green_2'], s=80, label='Northeast', alpha=0.8),
    plt.scatter([], [], c=UNMC_COLORS['orange_1'], s=80, label='West', alpha=0.8),
    plt.scatter([], [], c=UNMC_COLORS['blue_1'], s=80, label='Midwest (incl. Nebraska)', alpha=0.8),
    plt.scatter([], [], c='#129DBF', s=80, label='South', alpha=0.8),
    plt.scatter([], [], c='#AD122A', s=150, edgecolors='black', linewidth=2, label='UNMC Samples'),
]

ax.legend(handles=legend_elements, loc='upper left', fontsize=14,
          title='Regional Distribution', title_fontsize=16, frameon=True,
          fancybox=True, shadow=True, bbox_to_anchor=(0.02, 0.98))

plt.tight_layout()
plt.show()

# Print statistics
print(f"\n=== TREE STATISTICS ===")
print(f"Total tips in tree: {len(list(filter(lambda k: k.branchType == 'leaf', ll.Objects)))}")
print(f"Total internal nodes: {len(list(filter(lambda k: k.branchType == 'node', ll.Objects)))}")

# Check which UNMC samples are in the tree
tree_tips = set([tip.name for tip in ll.Objects if hasattr(tip, 'branchType') and tip.branchType == 'leaf'])
unmc_in_tree = UNMC_SAMPLES.intersection(tree_tips)
print(f"\nUNMC samples in tree: {len(unmc_in_tree)} out of {len(UNMC_SAMPLES)}")

if len(unmc_in_tree) > 0:
    print("UNMC samples found:")
    for strain in sorted(unmc_in_tree):
        region = strain_to_region.get(strain, 'unknown')
        broad_region = strain_to_broad_region.get(strain, 'unknown')
        print(f"  {strain}: {region} -> {broad_region}")

# Count by broad region in tree
broad_region_counts_tree = {}
for node in ll.Objects:
    if hasattr(node, 'branchType') and node.branchType == 'leaf' and hasattr(node, 'traits'):
        broad_region = node.traits.get('broad_region', 'Other')
        broad_region_counts_tree[broad_region] = broad_region_counts_tree.get(broad_region, 0) + 1

print(f"\nSamples by broad region in tree:")
for region, count in sorted(broad_region_counts_tree.items(), key=lambda x: x[1], reverse=True):
    color = REGION_COLORS.get(region, '#CCCCCC')
    print(f"  {region}: {count} samples (color: {color})")

# Optional: Save the figure
# plt.savefig('phylogenetic_tree_unmc_regional.png', dpi=300, bbox_inches='tight')
