# GTF File Configuration Guide

The Easy Tracks system now supports automatic inclusion of GTF/GFF annotation files in your track plots. This allows you to visualize gene annotations alongside your BigWig signals and BED peak files.

## Configuration Options

You can specify GTF files in your `easy_tracks_config.yaml` file in two ways:

### Option 1: Specific GTF File
```yaml
gtf_file: "/path/to/your/annotations.gtf"
```

This will use a single, specific GTF file for all plots.

### Option 2: GTF Directory
```yaml
gtf_dir: "/path/to/annotations/directory"
gtf_file: null  # Set to null to use directory search
```

This will automatically find all GTF/GFF files in the specified directory.

## Usage Examples

### Using Config File
```python
from easy_tracks import EasyTracks

# Initialize with config file containing GTF settings
et = EasyTracks('easy_tracks_config.yaml')

# GTF files will be automatically included from config
regions = [('chr1', 100000, 200000, 'test_region')]
bigwig_files = et.find_bigwig_files()
bed_files = et.find_bed_files()
gtf_files = et.find_gtf_files()  # Uses config settings

et.generate_tracks(regions, bigwig_files, bed_files=bed_files, gtf_files=gtf_files)
```

### Manual GTF Specification
```python
# Override config with specific GTF file
gtf_files = et.find_gtf_files(filename="/path/to/specific.gtf")

# Or search specific directory
gtf_files = et.find_gtf_files(directory="/path/to/gtf/dir")
```

## Supported File Formats

- `.gtf` - Gene Transfer Format
- `.gff` - General Feature Format  
- `.gff3` - GFF version 3

## Visual Settings

You can customize GTF track appearance in the config:

```yaml
gtf_height: 3           # Height of GTF tracks (cm)
```

## Complete Example Config

```yaml
# Directories
bigwig_dir: "bigwig_files"
bed_dir: "bed_converted" 
gtf_file: "annotations/gencode.v43.annotation.gtf"
output_dir: "track_plots"

# Plot settings
gtf_height: 3
# ... other settings
```

## Quick Plot with GTF

```python
# GTF files automatically included from config
et = EasyTracks('config.yaml')
et.quick_plot('chr1:100000-200000')
```

The GTF annotations will appear as gene models below your BigWig signals and BED peak tracks, providing genomic context for your data.