# Easy Tracks

**User-friendly pyGenomeTracks generator for genomics data visualization**

Easy Tracks simplifies the process of creating publication-ready genome browser tracks from BigWig, BED, and GTF files. Built as a wrapper around the powerful [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks) library, it provides an intuitive interface for generating beautiful genome browser plots.

## Features

🎨 **Simple Interface**: Generate complex track plots with minimal configuration  
📁 **Auto-discovery**: Automatically find BigWig, BED, and GTF files  
🎯 **Flexible Input**: Support for single regions or CSV/TSV files  
🌈 **Customizable**: Easy color schemes and plot settings  
🔧 **YAML Configuration**: Store and reuse settings  
📊 **Multiple Formats**: Support for BigWig, BED, narrowPeak, GTF files  
💻 **Command Line & Python API**: Use via CLI or import as Python package  

## Installation

### From Source
```bash
git clone <repository-url>
cd easy_tracks_package
pip install -e .
```

### Dependencies
- Python ≥ 3.8
- pandas ≥ 1.3.0
- pyBigWig ≥ 0.3.0
- PyYAML ≥ 5.4.0
- pyGenomeTracks ≥ 3.7

## Quick Start

### Command Line Usage
```bash
# Plot a single region
easy-tracks --region "chr1:1000000-2000000:MYC"

# Plot with BED peaks and GTF annotations
easy-tracks --region regions.csv --bed_dir peaks/ --gtf_file genes.gtf

# Interactive mode
easy-tracks --interactive
```

### Python API
```python
from easy_tracks import EasyTracks

# Initialize with configuration
et = EasyTracks('config.yaml')

# Quick plot
et.quick_plot('chr1:1000000-2000000:MYC')

# Advanced usage
regions = [('chr1', 1000000, 2000000, 'MYC')]
bigwig_files = et.find_bigwig_files('bigwig_dir/')
bed_files = et.find_bed_files('peaks_dir/')
gtf_files = et.find_gtf_files('annotations_dir/')

et.generate_tracks(regions, bigwig_files, 
                   bed_files=bed_files, 
                   gtf_files=gtf_files,
                   output='results/')
```

## Configuration

Create a YAML configuration file to customize settings:

```yaml
# Directories
bigwig_dir: "bigwig_files"
bed_dir: "peaks" 
gtf_file: "annotations/genes.gtf"
output_dir: "track_plots"

# Plot settings
bp_shift: 10000        # Region padding
track_height: 2.5      # BigWig track height (cm)
bed_height: 1.5        # BED track height (cm)
gtf_height: 3          # GTF track height (cm)

# Colors
default_colors:
  - "#3498DB"  # Blue
  - "#E74C3C"  # Red
  - "#2ECC71"  # Green

bed_colors:
  - "#FF6B6B"  # Light red
  - "#4ECDC4"  # Light teal
```

## Input Formats

### Regions
- **String**: `"chr1:1000000-2000000:GeneName"`
- **CSV/TSV**: Files with chr, start, end, gene columns

### Supported File Types
- **BigWig**: `.bw`, `.bigwig`
- **BED/Peaks**: `.bed`, `.narrowPeak`, `.broadPeak`
- **Annotations**: `.gtf`, `.gff`, `.gff3`

## Examples

### Basic Usage
```python
from easy_tracks import EasyTracks

# Display current configuration
et = EasyTracks('config.yaml')
print(et)  # Shows formatted configuration

# Generate tracks
et.quick_plot('chr1:1000000-2000000')
```

### Advanced Customization
```python
# Custom colors and output
et.quick_plot('regions.csv', 
              colors='red,blue,green',
              bed_colors='orange,purple',
              output='custom_plots/')

# Multiple regions from file
et.quick_plot('my_regions.csv', 
              bigwig_dir='my_bigwigs/',
              bed_dir='my_peaks/',
              gtf_file='my_annotations.gtf')
```

### Utility Functions
```python
from easy_tracks import convert_narrowpeak_to_bed

# Convert narrowPeak to BED format
convert_narrowpeak_to_bed('peaks.narrowPeak', 'peaks.bed')
```

## Command Line Examples

```bash
# Plot from CSV with custom settings
easy-tracks --region genes.csv \\
           --bigwig_dir data/bigwigs/ \\
           --bed_dir data/peaks/ \\
           --gtf_file annotations/genes.gtf \\
           --output results/

# Custom colors
easy-tracks --region "chr1:1000000-2000000" \\
           --colors "red,blue,green" \\
           --bed_colors "orange,purple"

# Using configuration file
easy-tracks --config my_config.yaml --region regions.csv
```

## Package Structure

```
easy_tracks_package/
├── easy_tracks/
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Main EasyTracks class
│   ├── cli.py               # Command line interface
│   └── utils.py             # Utility functions
├── configs/
│   ├── easy_tracks_config.yaml
│   └── easy_tracks_config_example.yaml
├── examples/
│   ├── make_tracks.py
│   └── example_regions.csv
├── docs/
│   ├── CONFIG_DISPLAY_GUIDE.md
│   └── GTF_CONFIG_GUIDE.md
├── setup.py
├── requirements.txt
└── README.md
```

## Output

Easy Tracks generates:
- **PDF plots**: High-quality genome browser visualizations
- **INI files**: pyGenomeTracks configuration files for reproducibility
- **Organized output**: Structured file naming and directories

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Support

- 📖 Documentation: See `docs/` directory
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions