"""
Easy Tracks: User-friendly pyGenomeTracks generator
A Python package for creating publication-ready genome browser tracks with minimal configuration
"""

from .core import EasyTracks
from .utils import (
    convert_narrowpeak_to_bed,
    convert_narrowpeak_directory, 
    validate_bigwig_file,
    find_files_with_extensions,
    create_example_regions_file,
    get_package_config_path
)

__version__ = "1.0.0"
__author__ = "Easy Tracks Development Team"
__description__ = "User-friendly pyGenomeTracks generator for genomics data visualization"

# Main class and functions available at package level
__all__ = [
    'EasyTracks',
    'convert_narrowpeak_to_bed',
    'convert_narrowpeak_directory',
    'validate_bigwig_file', 
    'find_files_with_extensions',
    'create_example_regions_file',
    'get_package_config_path'
]

# Package metadata
SUPPORTED_FORMATS = {
    'bigwig': ['.bw', '.bigwig'],
    'bed': ['.bed', '.narrowPeak', '.broadPeak'], 
    'gtf': ['.gtf', '.gff', '.gff3']
}

DEPENDENCIES = [
    'pandas',
    'pyBigWig', 
    'PyYAML',
    'pyGenomeTracks'
]