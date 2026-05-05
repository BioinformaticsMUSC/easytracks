# EasyTracks Configuration Display

The EasyTracks class now includes string representation methods to easily view and debug your configuration settings.

## Methods Added

### `__str__()` - Formatted Display
Returns a beautifully formatted, human-readable display of all configuration parameters:

```python
from easy_tracks import EasyTracks

et = EasyTracks('config.yaml')
print(et)
```

Output:
```
EasyTracks Configuration:
==============================

📁 Directories:
  BigWig files:     bigwig_files
  BED/peak files:   bed
  GTF directory:    annotations
  Output directory: track_plots

🎨 Plot Settings:
  Region padding:   10,000 bp
  BigWig height:    2 cm
  BED height:       1.5 cm
  GTF height:       2 cm
  Resolution:       700 bins
  Summary method:   mean

🌈 Colors:
  BigWig colors:    #3498DB, #E74C3C, #2ECC71, #F39C12, #9B59B6
  BED colors:       #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7

📄 File Extensions:
  BigWig:           .bw, .bigwig
  BED/peaks:        .bed, .narrowPeak, .broadPeak
  GTF/annotations:  .gtf, .gff, .gff3
```

### `__repr__()` - Technical Display
Returns a concise technical representation:

```python
print(repr(et))
```

Output:
```
EasyTracks(config_keys=['bigwig_dir', 'bed_dir', ...], output_dir='track_plots')
```

### `show_config()` - Convenience Method
Displays the formatted configuration (same as `print(et)`):

```python
et.show_config()
```

## Usage Examples

### Debug Configuration Loading
```python
et = EasyTracks('my_config.yaml')
print("Loaded configuration:")
et.show_config()
```

### Compare Configurations
```python
default_et = EasyTracks()
config_et = EasyTracks('custom_config.yaml')

print("Default configuration:")
print(default_et)

print("\nCustom configuration:")  
print(config_et)
```

### Verify Settings Before Running
```python
et = EasyTracks('config.yaml')
print("Current settings:")
et.show_config()

# Proceed with plotting
et.quick_plot('chr1:1000000-2000000')
```

This feature is especially useful for:
- ✅ Debugging configuration issues
- ✅ Verifying loaded settings
- ✅ Documenting analysis parameters
- ✅ Comparing different configurations