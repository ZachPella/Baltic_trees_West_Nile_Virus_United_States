# Baltic Phylogenetic Tree Visualization Pipeline

A comprehensive Python pipeline for creating publication-ready phylogenetic tree visualizations using the Baltic library. Designed for time-calibrated trees with metadata-driven sample highlighting and regional/temporal analysis.

## Overview

This pipeline processes Newick tree files and associated metadata to create customizable phylogenetic visualizations. Features include time-calibrated plotting, metadata-based sample highlighting, regional analysis, and publication-quality output formats.

## Key Features

- **Time-calibrated tree visualization** with decimal year conversion
- **Metadata-driven sample highlighting** by region, year, or custom categories
- **Flexible color schemes** for different sample groups
- **Publication-ready output** in multiple formats (PNG, PDF, SVG)
- **Statistical summaries** of tree composition and sample distribution
- **Interactive legend** generation based on metadata categories

## Requirements

### Python Dependencies
```bash
pip install baltic-lib pandas matplotlib numpy
```

### Required Libraries
- **baltic** - Phylogenetic tree manipulation and visualization
- **pandas** - Metadata handling and data processing
- **matplotlib** - Plotting and figure generation
- **numpy** - Numerical operations

### Input Files
1. **Newick tree file** (`.nwk`) - Time-calibrated phylogenetic tree
2. **Metadata file** (`.tsv` or `.csv`) - Sample information with columns:
   - `strain` - Sample identifiers matching tree tip names
   - `Region` - Geographic or categorical groupings
   - `date` - Collection dates (YYYY-MM-DD or YYYY-XX-XX format)
   - Additional columns as needed

## Installation (Google Colab)

1. **Install dependencies in Colab:**
```python
# Run this in a Colab cell
!pip install baltic-lib pandas matplotlib numpy
```

2. **Upload your files to Colab:**
```python
# Upload tree and metadata files
from google.colab import files
uploaded = files.upload()
# Select your .nwk and .tsv/.csv files
```

3. **Verify installation:**
```python
import baltic as bt
print('Baltic installed successfully')
```

## Installation (Local Environment)

1. **Install dependencies:**
```bash
pip install baltic-lib pandas matplotlib numpy
```

2. **Download the notebook:**
   - Copy the code from the repository
   - Or download individual script files

## Usage

### Google Colab Usage
```python
# In a Colab cell, copy and paste the visualization code
import baltic as bt
import pandas as pd
import matplotlib.pyplot as plt

# Load your uploaded files
tree = bt.loadNewick('tree_2025.nwk')  # Your uploaded tree file
metadata = pd.read_csv('updated_metadata.tsv', sep='\t')  # Your uploaded metadata

# Run the visualization code (see examples below)
```

### Jupyter Notebook Usage
```python
import baltic as bt
import pandas as pd
import matplotlib.pyplot as plt

# Load your local files
tree = bt.loadNewick('/path/to/your/tree.nwk')
metadata = pd.read_csv('/path/to/your/metadata.tsv', sep='\t')

# Run visualization
```

### Custom Analysis Template
```python
# Basic template for Colab/Jupyter
import baltic as bt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data
tree = bt.loadNewick('your_tree.nwv')
metadata = pd.read_csv('your_metadata.tsv', sep='\t')

# Your analysis code here...
```

## Configuration Options

### Tree Appearance
```python
tree_config = {
    'figure_size': (20, 10),
    'branch_color': '#CCCCCC',
    'branch_width': 2,
    'tip_size_highlighted': 100,
    'tip_size_normal': 30,
    'time_range': (1993, 2025)
}
```

### Color Schemes
```python
color_schemes = {
    'nebraska_regions': {
        'NE_Central': '#FCB614',  # Gold
        'NE_West': '#005E63',     # Teal  
        'NE_East': '#AD122A',     # Red
        'other': '#CCCCCC'        # Grey
    },
    'temporal': {
        '2023': '#FF0000',
        '2022': '#FF6666',
        'other': '#CCCCCC'
    }
}
```

### Filtering Options
```python
filters = {
    'regions': ['NE_Central', 'NE_West', 'NE_East'],
    'years': [2023],
    'date_range': ('2020-01-01', '2025-12-31'),
    'custom_field': 'field_name'
}
```

## Script Components

### Core Functions

#### 1. Date Processing
```python
def date_to_decimal_year(date_str):
    """Convert YYYY-MM-DD or YYYY-XX-XX to decimal year"""
    # Handles missing data and various date formats
    # Returns float for precise time positioning
```

#### 2. Tree Time Calibration
```python
def set_node_times(node, metadata_dict):
    """Set absoluteTime for all nodes based on tip dates"""
    # Recursive function for internal node timing
    # Ensures proper temporal axis scaling
```

#### 3. Metadata Integration
```python
def add_traits_to_tree(tree, metadata):
    """Add metadata as node traits for visualization"""
    # Maps sample metadata to tree tips
    # Creates trait dictionaries for coloring/filtering
```

#### 4. Visualization Engine
```python
def create_tree_plot(tree, metadata, config):
    """Generate publication-ready tree visualization"""
    # Main plotting function with full customization
    # Handles legends, axes, and output formatting
```

## Example Workflows

### Workflow 1: Regional Analysis
```python
# Highlight samples from specific regions
regions_of_interest = ['NE_Central', 'NE_West', 'NE_East']
filtered_metadata = metadata[metadata['Region'].isin(regions_of_interest)]

# Create visualization
create_regional_tree_plot(
    tree='phylogeny.nwk',
    metadata=filtered_metadata,
    highlight_regions=regions_of_interest,
    output='regional_analysis.png'
)
```

### Workflow 2: Temporal Analysis
```python
# Focus on specific time period
temporal_filter = {
    'start_year': 2020,
    'end_year': 2025,
    'highlight_year': 2023
}

create_temporal_tree_plot(
    tree='phylogeny.nwk',
    metadata='metadata.tsv',
    temporal_config=temporal_filter,
    output='temporal_analysis.png'
)
```

### Workflow 3: Custom Categories
```python
# Use any metadata column for grouping
custom_groups = {
    'field': 'sample_type',
    'groups': ['clinical', 'environmental', 'reference'],
    'colors': ['#FF0000', '#00FF00', '#0000FF']
}

create_custom_tree_plot(
    tree='phylogeny.nwk',
    metadata='metadata.tsv',
    grouping=custom_groups,
    output='custom_analysis.png'
)
```

## Output Files

### Visualization Outputs
- **`tree_plot.png`** - High-resolution raster image (300 DPI)
- **`tree_plot.pdf`** - Vector format for publications
- **`tree_plot.svg`** - Scalable vector for web/editing

### Analysis Outputs
- **`tree_statistics.txt`** - Tree composition summary
- **`sample_distribution.csv`** - Metadata breakdown by categories
- **`filtered_samples.txt`** - List of samples meeting filter criteria

### Log Files
- **`processing.log`** - Detailed processing information
- **`warnings.log`** - Data quality and formatting warnings

## Customization Guide

### Adding New Color Schemes
```python
# Define in config/color_schemes.py
new_scheme = {
    'category1': '#COLOR1',
    'category2': '#COLOR2',
    'default': '#CCCCCC'
}
```

### Custom Filtering Functions
```python
def custom_filter(metadata, criteria):
    """Create custom filtering logic"""
    # Implement your specific filtering needs
    # Return filtered dataframe
    pass
```

### Plot Layout Modifications
```python
# Adjust figure dimensions and layout
fig_config = {
    'width': 24,
    'height': 12,
    'dpi': 300,
    'layout': 'tight'
}
```

## Quality Control

### Data Validation
- **Tree-metadata matching**: Verifies all tree tips have metadata
- **Date format checking**: Validates and converts date formats
- **Missing data handling**: Reports and manages missing values
- **Duplicate detection**: Identifies duplicate sample names

### Visual Quality Checks
- **Tip positioning**: Ensures proper temporal alignment
- **Color contrast**: Validates color scheme accessibility
- **Legend completeness**: Verifies all categories are represented
- **Scale appropriateness**: Checks axis ranges and scaling

## Troubleshooting

### Common Issues

1. **Tree tips not matching metadata**:
```python
# Check sample name mismatches
tree_tips = set([tip.name for tip in tree.Objects if tip.branchType == 'leaf'])
metadata_samples = set(metadata['strain'])
missing_metadata = tree_tips - metadata_samples
print(f"Tips missing metadata: {missing_metadata}")
```

2. **Date parsing errors**:
```python
# Validate date formats
problematic_dates = metadata[metadata['date'].apply(date_to_decimal_year).isna()]
print("Problematic dates:", problematic_dates['date'].unique())
```

3. **Memory issues with large trees**:
```bash
# Increase available memory
export MPLBACKEND=Agg  # Use non-interactive backend
python visualize_phylogeny.py --tree large_tree.nwk --low-memory-mode
```

4. **Color scheme conflicts**:
```python
# Check for sufficient colors
unique_categories = metadata['Region'].nunique()
available_colors = len(color_scheme)
if unique_categories > available_colors:
    print("Warning: More categories than available colors")
```

## Advanced Features

### Batch Processing
```python
# Process multiple trees with same metadata
trees = ['tree1.nwk', 'tree2.nwk', 'tree3.nwk']
for tree_file in trees:
    process_tree(tree_file, 'metadata.tsv')
```

### Interactive Features
```python
# Add click events for sample information
def on_tip_click(event, tip_name):
    sample_info = metadata[metadata['strain'] == tip_name]
    print(sample_info)
```

### Animation Support
```python
# Create time-lapse animations
create_animated_tree(
    tree='phylogeny.nwk',
    metadata='metadata.tsv',
    time_steps=range(2000, 2025),
    output='tree_animation.gif'
)
```

## Citation

If you use this pipeline, please cite:
- **Baltic**: Dudas, G. & Rambaut, A. BALTIC: phylogenetic tree plotting and manipulation. J. Open Source Softw. 3, 1111 (2018).
- **Matplotlib**: Hunter, J. D. Matplotlib: A 2D graphics environment. Comput. Sci. Eng. 9, 90-95 (2007).

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-visualization`)
3. Commit your changes (`git commit -am 'Add new visualization type'`)
4. Push to the branch (`git push origin feature/new-visualization`)
5. Create a Pull Request

## Contact

- **Author**: Zach Pella
- **Institution**: Fauver Lab
- **Issues**: Use GitHub issues for bug reports and feature requests

---

## Repository Structure
```
baltic-phylo-pipeline/
├── README.md
├── LICENSE
├── requirements.txt
├── notebooks/
│   ├── phylogenetic_visualization.ipynb  # Main Colab notebook
│   ├── regional_analysis_example.ipynb
│   └── temporal_analysis_example.ipynb
├── scripts/
│   ├── visualize_phylogeny.py           # Standalone Python script
│   ├── tree_utils.py                    # Helper functions
│   └── color_schemes.py                 # Color scheme definitions
├── examples/
│   ├── example_tree.nwk                 # Sample tree file
│   ├── example_metadata.tsv             # Sample metadata
│   └── basic_usage_examples.py
└── docs/
    ├── colab_tutorial.md
    ├── customization_guide.md
    └── troubleshooting.md
```

## Example Data
The repository includes example datasets:
- **`example_tree.nwk`** - Sample phylogenetic tree
- **`example_metadata.tsv`** - Corresponding metadata file
- **`tutorial_data/`** - Complete tutorial dataset
<img width="1990" height="989" alt="download" src="https://github.com/user-attachments/assets/9e3f5bba-5773-4133-94db-56fce7e75f57<img width="1990" height="989" alt="download" src="https://github.com/user-attachments/assets/40e14ac7-a67c-4c93-9b2c-75ea156d09f3" />
" />
<img width="1990" height="989" alt="download" src="https://github.com/user-attachments/assets/00367c1c-3f31-4906-916e-9159d846738f" />
<img width="1990" height="989" alt="download" src="https://github.com/user-attachments/assets/1c123757-61af-416d-81b6-5db1d8004c50" />
<img width="1490" height="989" alt="download" src="https://github.com/user-attachments/assets/e9e893a5-0056-474e-9b05-7f949acbacc0" />
<img width="1990" height="1389" alt="download" src="https://github.com/user-attachments/assets/2206a789-b4d1-457f-8c98-1cf28ad93fac" />
<img width="1990" height="989" alt="download" src="https://github.com/user-attachments/assets/8292d05e-b155-497a-be74-79dbe268017c" />
<img width="1990" height="989" alt="download" src="https://github.com/user-attachments/assets/378afadc-c42f-42a4-a6c7-ec807bba054a" />
<img width="1990" height="1189" alt="download" src="https://github.com/user-attachments/assets/7fef648b-2ffe-4e71-87d7-5c9ae010e5bb" />
<img width="2790" height="789" alt="download" src="https://github.com/user-attachments/assets/37c78cc6-d115-433e-8fb4-2075ddab9b62" />
<img width="1589" height="789" alt="download" src="https://github.com/user-attachments/assets/da5c2982-21df-41b9-8367-b5906ed8a822" />
