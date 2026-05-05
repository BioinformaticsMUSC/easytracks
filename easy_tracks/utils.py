"""
Easy Tracks Utility Functions
Contains helper functions for file conversion and processing
"""

import os
from pathlib import Path
from typing import List, Optional


def convert_narrowpeak_to_bed(narrowpeak_file: str, output_file: str = None, 
                             keep_score: bool = True, keep_strand: bool = True) -> bool:
    """
    Convert a narrowPeak file to BED format
    
    Args:
        narrowpeak_file: Path to input narrowPeak file
        output_file: Path to output BED file (optional)
        keep_score: Include score column in output
        keep_strand: Include strand column in output
    
    Returns:
        True if conversion successful, False otherwise
    """
    
    if not output_file:
        # Generate output filename
        output_file = str(Path(narrowpeak_file).with_suffix('.bed'))
    
    print(f"Converting {narrowpeak_file} -> {output_file}")
    
    converted_count = 0
    
    try:
        with open(narrowpeak_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                try:
                    fields = line.split('\t')
                    if len(fields) < 3:
                        print(f"Warning: Line {line_num} has fewer than 3 columns, skipping")
                        continue
                    
                    # Extract basic BED columns
                    chrom = fields[0]
                    start = fields[1] 
                    end = fields[2]
                    
                    # Build BED line
                    bed_fields = [chrom, start, end]
                    
                    # Add name if available
                    if len(fields) >= 4 and fields[3]:
                        bed_fields.append(fields[3])
                    else:
                        bed_fields.append(f"peak_{converted_count + 1}")
                    
                    # Add score if requested and available
                    if keep_score and len(fields) >= 5:
                        bed_fields.append(fields[4])
                    
                    # Add strand if requested and available
                    if keep_strand and len(fields) >= 6:
                        bed_fields.append(fields[5])
                    
                    outfile.write('\t'.join(bed_fields) + '\n')
                    converted_count += 1
                    
                except Exception as e:
                    print(f"Warning: Error processing line {line_num}: {e}")
                    continue
    
    except Exception as e:
        print(f"Error: Could not process {narrowpeak_file}: {e}")
        return False
    
    print(f"✅ Converted {converted_count} peaks")
    return True


def convert_narrowpeak_directory(input_dir: str, output_dir: str = None, 
                                pattern: str = "*.narrowPeak") -> bool:
    """
    Convert all narrowPeak files in a directory to BED format
    
    Args:
        input_dir: Directory containing narrowPeak files
        output_dir: Output directory for BED files
        pattern: File pattern to match
    
    Returns:
        True if all conversions successful, False otherwise
    """
    
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Directory {input_dir} not found!")
        return False
    
    # Find narrowPeak files
    narrowpeak_files = list(input_path.glob(pattern))
    if not narrowpeak_files:
        print(f"❌ No files matching {pattern} found in {input_dir}")
        return False
    
    print(f"🔍 Found {len(narrowpeak_files)} narrowPeak files")
    
    # Set up output directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    success_count = 0
    
    for narrowpeak_file in narrowpeak_files:
        output_file = output_path / f"{narrowpeak_file.stem}.bed"
        
        if convert_narrowpeak_to_bed(str(narrowpeak_file), str(output_file)):
            success_count += 1
    
    print(f"\n🎉 Successfully converted {success_count}/{len(narrowpeak_files)} files")
    return success_count == len(narrowpeak_files)


def validate_bigwig_file(filepath: str) -> bool:
    """
    Check if a file appears to be a valid BigWig file
    
    Args:
        filepath: Path to potential BigWig file
    
    Returns:
        True if file appears valid, False otherwise
    """
    try:
        import pyBigWig
        bw = pyBigWig.open(filepath)
        if bw is None:
            return False
        bw.close()
        return True
    except Exception:
        return False


def find_files_with_extensions(directory: str, extensions: List[str]) -> List[str]:
    """
    Find all files in directory with specified extensions
    
    Args:
        directory: Directory to search
        extensions: List of extensions to look for (e.g., ['.bw', '.bigwig'])
    
    Returns:
        List of file paths
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for ext in extensions:
        files.extend(Path(directory).glob(f"*{ext}"))
    
    return [str(f) for f in sorted(files)]


def create_example_regions_file(output_file: str = "example_regions.csv") -> bool:
    """
    Create an example regions CSV file for testing
    
    Args:
        output_file: Path to output CSV file
    
    Returns:
        True if file created successfully
    """
    try:
        with open(output_file, 'w') as f:
            f.write("chr,start,end,gene\n")
            f.write("chr1,1000000,1100000,Example1\n")
            f.write("chr2,2000000,2100000,Example2\n")
            f.write("chr3,3000000,3100000,Example3\n")
        
        print(f"✅ Created example regions file: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating example file: {e}")
        return False


def get_package_config_path(config_name: str = "easy_tracks_config.yaml") -> Optional[str]:
    """
    Get path to package configuration file
    
    Args:
        config_name: Name of configuration file
    
    Returns:
        Path to config file if found, None otherwise
    """
    # Check current directory first
    if os.path.exists(config_name):
        return config_name
    
    # Check package configs directory
    package_dir = Path(__file__).parent.parent
    config_path = package_dir / "configs" / config_name
    
    if config_path.exists():
        return str(config_path)
    
    return None