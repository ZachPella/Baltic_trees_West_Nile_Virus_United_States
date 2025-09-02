# Required imports
import baltic as bt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Color scheme as specified by your boss
UNMC_BLUE = '#002957'  # All nodes
UNMC_RED = '#AD122A'   # 29 specific UNMC samples

# Define your 29 specific UNMC samples to highlight
HIGHLIGHTED_SAMPLES = {
    'UNMC0008', 'UNMC0009', 'UNMC0014', 'UNMC0020', 'UNMC0185',
    'UNMC0270', 'UNMC0299', 'UNMC0261', 'UNMC0267', 'UNMC0015',
    'UNMC0011', 'UNMC0016', 'UNMC0017', 'UNMC0013', 'UNMC0730',
    'UNMC0567', 'UNMC0019', 'UNMC0209', 'UNMC0265', 'UNMC0728',
    'UNMC0010', 'UNMC0575', 'UNMC0538', 'UNMC0012', 'UNMC0707',
    'UNMC0282', 'UNMC0699', 'UNMC0678', 'UNMC0706'
}

print(f"🎯 Highlighting {len(HIGHLIGHTED_SAMPLES)} specific UNMC samples")

# Load your data
print("📁 Loading data...")
metadata = pd.read_csv('/content/updated_metadata.tsv', sep='\t')
tree = bt.loadNewick('/content/tree_NE_2025.nwk')
print(f"✅ Loaded {len(metadata)} metadata rows and {len(tree.Objects)} tree nodes")

# Let Baltic handle the tree layout - don't calculate divergence manually!
print("🌳 Setting up tree layout...")

# Get sample names from tree
tree_samples = set()
for node in tree.Objects:
    if hasattr(node, 'branchType') and node.branchType == 'leaf':
        if hasattr(node, 'name') and node.name:
            tree_samples.add(node.name)

# Check highlighted samples
highlighted_in_tree = HIGHLIGHTED_SAMPLES.intersection(tree_samples)
print(f"✅ Highlighted samples in tree: {len(highlighted_in_tree)} out of {len(HIGHLIGHTED_SAMPLES)}")

# Count sample types
unmc_in_tree = len([name for name in tree_samples if 'UNMC' in str(name)])
non_unmc_in_tree = len([name for name in tree_samples if 'UNMC' not in str(name)])
print(f"📋 UNMC samples in tree: {unmc_in_tree}")
print(f"📋 Non-UNMC samples in tree: {non_unmc_in_tree}")

# Create the figure
print("🎨 Creating visualization...")
fig, ax = plt.subplots(figsize=(20, 14), facecolor='white')

# Use Baltic's built-in coordinates for proper tree structure
# Baltic automatically calculates x and y coordinates for proper tree display

# Draw all branches using Baltic's coordinates
branch_count = 0
for node in tree.Objects:
    if hasattr(node, 'parent') and node.parent:
        # Use Baltic's x and y coordinates directly
        x = node.x
        y = node.y
        x_parent = node.parent.x
        y_parent = node.parent.y

        # Horizontal branch (from parent to node)
        ax.plot([x_parent, x], [y, y], color='#AAAAAA', linewidth=2, zorder=10, alpha=0.8)

        # Vertical connector for internal nodes (connect siblings)
        if hasattr(node.parent, 'children') and len(node.parent.children) > 1:
            sibling_ys = [child.y for child in node.parent.children if hasattr(child, 'y')]
            if len(sibling_ys) > 1:
                ax.plot([x_parent, x_parent], [min(sibling_ys), max(sibling_ys)],
                       color='#AAAAAA', linewidth=2, zorder=9, alpha=0.8)
        branch_count += 1

print(f"🌳 Drew {branch_count} branches")

# Plot sample points using Baltic's coordinates
highlighted_count = 0
unmc_count = 0
other_count = 0

for node in tree.Objects:
    if hasattr(node, 'branchType') and node.branchType == 'leaf':
        strain = getattr(node, 'name', None)
        if strain:
            if strain in HIGHLIGHTED_SAMPLES:
                # 29 highlighted samples: red with black edge
                ax.scatter(node.x, node.y, s=140, c=UNMC_RED,
                          zorder=20005, edgecolors='black', linewidth=2.5, alpha=1.0)
                highlighted_count += 1
            elif 'UNMC' in str(strain):
                # Other UNMC samples: blue
                ax.scatter(node.x, node.y, s=80, c=UNMC_BLUE,
                          zorder=20002, alpha=0.9, edgecolors='none')
                unmc_count += 1
            else:
                # Non-UNMC samples (reference sequences): blue
                ax.scatter(node.x, node.y, s=80, c=UNMC_BLUE,
                          zorder=20001, alpha=0.9, edgecolors='none')
                other_count += 1
        else:
            # No name - plot as blue
            ax.scatter(node.x, node.y, s=80, c=UNMC_BLUE,
                      zorder=20001, alpha=0.9, edgecolors='none')
            other_count += 1

# Set plot dimensions using Baltic's coordinate system
ax.set_ylim(-5, tree.ySpan + 5)

# For x-axis, let's use the actual tree span
# Baltic typically uses branch lengths for x-coordinates
x_coords = [node.x for node in tree.Objects if hasattr(node, 'x')]
if x_coords:
    x_min, x_max = min(x_coords), max(x_coords)
    x_range = x_max - x_min
    ax.set_xlim(x_min - 0.05 * x_range, x_max + 0.05 * x_range)

    print(f"📏 Tree x-range: {x_min:.6f} to {x_max:.6f}")
else:
    ax.set_xlim(0, 1)

# Style the plot
[ax.spines[loc].set_visible(False) for loc in ['left', 'right', 'top']]
ax.grid(axis='x', linestyle='-', color='grey', alpha=0.3, linewidth=0.8)
ax.tick_params(axis='y', size=0)
ax.tick_params(axis='x', labelsize=14)
ax.set_yticklabels([])

# The x-axis now represents cumulative branch lengths (nucleotide divergence)
ax.set_xlabel('Nucleotide Divergence from Root', fontsize=18, fontweight='bold')

plt.tight_layout()
plt.show()
