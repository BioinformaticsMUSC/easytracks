# Easy Tracks Package Installation Guide

This guide helps you install and test the Easy Tracks package.

## Installation Steps

### 1. Navigate to Package Directory
```bash
cd /Users/bryanwgranger/biocm/projects/kozo_mar26/easy_tracks_package
```

### 2. Install in Development Mode
```bash
pip install -e .
```

This installs the package in "editable" mode, so changes to the code are immediately available.

### 3. Test the Installation
```bash
python test_package.py
```

### 4. Test Command Line Interface
```bash
easy-tracks --help
```

### 5. Test with Example
```bash
cd examples
python make_tracks.py
```

## Package Structure

```
easy_tracks_package/
├── easy_tracks/              # Main package
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Main EasyTracks class
│   ├── cli.py               # Command line interface
│   └── utils.py             # Utility functions
├── configs/                 # Configuration files
│   ├── easy_tracks_config.yaml
│   └── easy_tracks_config_example.yaml
├── examples/                # Example scripts
│   ├── make_tracks.py
│   └── example_regions.csv
├── docs/                    # Documentation
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
├── README.md               # Main documentation
└── test_package.py         # Test script
```

## Usage Examples

### Python API
```python
from easy_tracks import EasyTracks

# Initialize
et = EasyTracks('configs/easy_tracks_config.yaml')

# Display configuration
print(et)

# Quick plot
et.quick_plot('chr1:1000000-2000000:MYC')
```

### Command Line
```bash
# Single region
easy-tracks --region "chr1:1000000-2000000:MYC"

# With config file
easy-tracks --config configs/easy_tracks_config.yaml --region regions.csv

# Interactive mode
easy-tracks --interactive
```

### Utility Functions
```python
from easy_tracks import convert_narrowpeak_to_bed

# Convert narrowPeak to BED
convert_narrowpeak_to_bed('peaks.narrowPeak', 'peaks.bed')
```

## Development

### Installing for Development
```bash
pip install -e ".[dev]"
```

### Running Tests
```bash
python test_package.py
```

### Building Distribution
```bash
python setup.py sdist bdist_wheel
```

## Troubleshooting

1. **Import Errors**: Make sure all dependencies are installed
2. **Command not found**: Reinstall with `pip install -e .`
3. **Config file errors**: Check YAML syntax and file paths
4. **Missing pyGenomeTracks**: Install with `pip install pyGenomeTracks`

## Next Steps

1. Test with your own data
2. Customize configuration files
3. Create your own examples
4. Share the package with collaborators