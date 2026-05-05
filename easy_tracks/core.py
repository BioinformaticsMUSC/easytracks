"""
Easy Tracks Core Module
Contains the main EasyTracks class for generating pyGenomeTracks visualizations
"""

import os
import pandas as pd
import pyBigWig
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import subprocess


class EasyTracks:
    """Simplified interface for generating pyGenomeTracks visualizations"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_default_config()
        if config_file:
            self._load_user_config(config_file)
            
    def _load_default_config(self) -> Dict:
        """Load default configuration with sensible defaults"""
        return {
            'bigwig_dir': 'bigwig_files',
            'bed_dir': 'bed',
            'gtf_dir': 'annotations',
            'gtf_file': None,
            'output_dir': 'track_plots',
            'bp_shift': 10000,
            'track_height': 2,
            'number_of_bins': 700,
            'default_colors': ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6'],
            'bed_colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
            'file_extensions': ['.bw', '.bigwig'],
            'bed_extensions': ['.bed', '.narrowPeak', '.broadPeak'],
            'gtf_extensions': ['.gtf', '.gff', '.gff3'],
            'summary_method': 'mean',
            'bed_height': 1.5,
            'gtf_height': 2
        }
    
    def _load_user_config(self, config_file: str):
        """Load user configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                user_config = yaml.safe_load(f)
            self.config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def __str__(self) -> str:
        """Human-readable string representation of EasyTracks configuration"""
        lines = ["EasyTracks Configuration:"]
        lines.append("=" * 30)
        
        # Directories section
        lines.append("\n📁 Directories:")
        lines.append(f"  BigWig files:     {self.config['bigwig_dir']}")
        lines.append(f"  BED/peak files:   {self.config['bed_dir']}")
        lines.append(f"  GTF directory:    {self.config['gtf_dir']}")
        if self.config.get('gtf_file'):
            lines.append(f"  GTF file:         {self.config['gtf_file']}")
        lines.append(f"  Output directory: {self.config['output_dir']}")
        
        # Plot settings section  
        lines.append("\n🎨 Plot Settings:")
        lines.append(f"  Region padding:   {self.config['bp_shift']:,} bp")
        lines.append(f"  BigWig height:    {self.config['track_height']} cm")
        lines.append(f"  BED height:       {self.config['bed_height']} cm")
        lines.append(f"  GTF height:       {self.config['gtf_height']} cm")
        lines.append(f"  Resolution:       {self.config['number_of_bins']} bins")
        lines.append(f"  Summary method:   {self.config['summary_method']}")
        
        # Colors section
        lines.append("\n🌈 Colors:")
        lines.append(f"  BigWig colors:    {', '.join(self.config['default_colors'])}")
        lines.append(f"  BED colors:       {', '.join(self.config['bed_colors'])}")
        
        # File extensions section
        lines.append("\n📄 File Extensions:")
        lines.append(f"  BigWig:           {', '.join(self.config['file_extensions'])}")
        lines.append(f"  BED/peaks:        {', '.join(self.config['bed_extensions'])}")
        lines.append(f"  GTF/annotations:  {', '.join(self.config['gtf_extensions'])}")
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """Technical string representation of EasyTracks object"""
        return f"EasyTracks(config_keys={list(self.config.keys())}, output_dir='{self.config['output_dir']}')"
    
    def show_config(self) -> None:
        """Display current configuration in a formatted way"""
        print(self)
    
    def find_bigwig_files(self, directory: str = None) -> List[str]:
        """Auto-discover BigWig files in directory"""
        if not directory:
            directory = self.config['bigwig_dir']
            
        if not os.path.exists(directory):
            print(f"❌ Directory {directory} not found!")
            return []
            
        bw_files = []
        for ext in self.config['file_extensions']:
            bw_files.extend(Path(directory).glob(f"*{ext}"))
            
        bw_files = [str(f) for f in sorted(bw_files)]
        
        if bw_files:
            print(f"✅ Found {len(bw_files)} BigWig files:")
            for f in bw_files:
                print(f"  - {os.path.basename(f)}")
        else:
            print(f"❌ No BigWig files found in {directory}")
            
        return bw_files
    
    def find_bed_files(self, directory: str = None) -> List[str]:
        """Auto-discover BED/peak files in directory"""
        if not directory:
            directory = self.config['bed_dir']
            
        if not os.path.exists(directory):
            print(f"⚠️ BED directory {directory} not found, skipping BED files")
            return []
            
        bed_files = []
        for ext in self.config['bed_extensions']:
            bed_files.extend(Path(directory).glob(f"*{ext}"))
            
        bed_files = [str(f) for f in sorted(bed_files)]
        
        if bed_files:
            print(f"✅ Found {len(bed_files)} BED/peak files:")
            for f in bed_files:
                print(f"  - {os.path.basename(f)}")
        
        return bed_files
    
    def find_gtf_files(self, directory: str = None, filename: str = None) -> List[str]:
        """Find GTF/GFF annotation files"""
        gtf_files = []
        
        # Use config file settings if no parameters provided
        if not filename and not directory:
            if self.config.get('gtf_file') and os.path.exists(self.config['gtf_file']):
                filename = self.config['gtf_file']
            else:
                directory = self.config.get('gtf_dir')
        
        if filename and os.path.exists(filename):
            gtf_files.append(filename)
        elif directory:
            if os.path.exists(directory):
                for ext in self.config['gtf_extensions']:
                    gtf_files.extend(Path(directory).glob(f"*{ext}"))
        
        gtf_files = [str(f) for f in sorted(gtf_files)]
        
        if gtf_files:
            print(f"✅ Found {len(gtf_files)} GTF/annotation files:")
            for f in gtf_files:
                print(f"  - {os.path.basename(f)}")
        
        return gtf_files

    def get_max_in_region(self, bigwig_files: List[str], chr_name: str, 
                         start: int, end: int) -> float:
        """Get maximum signal value across all BigWig files in region"""
        max_values = []
        
        for bw_file in bigwig_files:
            try:
                bw = pyBigWig.open(bw_file)
                values = bw.values(chr_name, start, end)
                if values:
                    max_val = max([v for v in values if v is not None])
                    max_values.append(max_val)
                bw.close()
            except Exception as e:
                print(f"⚠️ Warning: Could not read {bw_file}: {e}")
                
        return max(max_values) if max_values else 100.0
    
    def create_ini_file(self, bigwig_files: List[str], max_value: float, 
                       colors: List[str] = None, bed_files: List[str] = None,
                       gtf_files: List[str] = None, bed_colors: List[str] = None) -> str:
        """Create pyGenomeTracks INI configuration file"""
        
        if not colors:
            colors = (self.config['default_colors'] * 10)[:len(bigwig_files)]
        
        if bed_files and not bed_colors:
            bed_colors = (self.config['bed_colors'] * 10)[:len(bed_files)]
        
        ini_content = []
        
        # Add x-axis
        ini_content.extend([
            "[x-axis]",
            "fontsize = 12",
            "where = top",
            "",
            "[spacer]",
            "height = 0.3",
            ""
        ])
        
        # Add tracks for each BigWig file
        for i, bw_file in enumerate(bigwig_files):
            sample_name = Path(bw_file).stem
            color = colors[i] if i < len(colors) else self.config['default_colors'][0]
            
            ini_content.extend([
                f"[{sample_name}]",
                f"file = {os.path.abspath(bw_file)}",
                f"title = {sample_name}",
                f"height = {self.config['track_height']}",
                f"color = {color}",
                f"min_value = 0",
                f"max_value = {max_value:.1f}",
                f"number_of_bins = {self.config['number_of_bins']}",
                "nans_to_zeros = true",
                f"summary_method = {self.config['summary_method']}",
                "type = fill",
                ""
            ])
        
        # Add BED/peak files
        if bed_files:
            ini_content.extend([
                "[spacer]",
                "height = 0.2",
                ""
            ])
            
            for i, bed_file in enumerate(bed_files):
                bed_name = Path(bed_file).stem
                bed_color = bed_colors[i] if bed_colors and i < len(bed_colors) else self.config['bed_colors'][0]
                
                ini_content.extend([
                    f"[{bed_name}]",
                    f"file = {os.path.abspath(bed_file)}",
                    f"title = {bed_name}",
                    f"height = {self.config['bed_height']}",
                    f"color = {bed_color}",
                    "border_color = black",
                    "interval_height = 100",
                    "display = collapsed",
                    "labels = false",
                    ""
                ])
        
        # Add GTF/annotation files
        if gtf_files:
            ini_content.extend([
                "[spacer]",
                "height = 0.2",
                ""
            ])
            
            for gtf_file in gtf_files:
                gtf_name = Path(gtf_file).stem
                
                ini_content.extend([
                    f"[{gtf_name}]",
                    f"file = {os.path.abspath(gtf_file)}",
                    f"title = {gtf_name}",
                    f"height = {self.config['gtf_height']}",
                    "color = #1f77b4",
                    "border_color = black",
                    "display = stacked",
                    "labels = true",
                    "style = UCSC",
                    "gene_rows = 10",
                    ""
                ])
        
        return "\n".join(ini_content)
    
    def generate_tracks(self, regions: List[Union[Tuple[str, int, int], Tuple[str, int, int, str]]], 
                       bigwig_files: List[str], colors: List[str] = None,
                       bed_files: List[str] = None, bed_colors: List[str] = None,
                       gtf_files: List[str] = None, auto_scale: bool = True, 
                       output: str = None, keep_ini_file: bool = False) -> List[str]:
        """Generate track plots for specified regions
        
        Args:
            regions: List of region tuples. Each tuple can be:
                    - (chr_name, start, end) - gene_name will be auto-generated
                    - (chr_name, start, end, gene_name) - explicit gene name
            bigwig_files: List of BigWig file paths
            colors: Colors for BigWig tracks (optional)
            bed_files: BED/peak files to overlay (optional)
            bed_colors: Colors for BED tracks (optional)
            gtf_files: GTF annotation files (optional)
            auto_scale: Auto-scale Y-axis based on data
            output: Output directory or file prefix
            keep_ini_file: Keep INI configuration files after plotting (default: False)
            
        Returns:
            List of generated file paths
        """
        
        # Determine output directory and file prefix
        if output is None:
            output_dir = self.config['output_dir']
            file_prefix = ''
        elif output.endswith('/') or os.path.isdir(output):
            # output is a directory
            output_dir = output.rstrip('/')
            file_prefix = ''
        else:
            # output is a file prefix, extract directory and prefix
            output_dir = os.path.dirname(output) or '.'
            file_prefix = os.path.basename(output) + '_' if os.path.basename(output) else ''
        
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []
        
        for i, region in enumerate(regions):
            # Handle both 3-element and 4-element tuples
            if len(region) == 3:
                chr_name, start, end = region
                gene_name = f"{chr_name}_{start}_{end}"
                start = int(start)
                end = int(end)
            elif len(region) == 4:
                chr_name, start, end, gene_name = region
                start = int(start)
                end = int(end)
            else:
                print(f"⚠️ Warning: Skipping invalid region format: {region}")
                continue
                
            print(f"\n🎯 Processing {gene_name}: {chr_name}:{start}-{end}")
            
            # Calculate plot window with padding
            plot_start = max(0, start - self.config['bp_shift'])
            plot_end = end + self.config['bp_shift']
            
            # Get maximum value for scaling if auto_scale is enabled
            if auto_scale:
                print("  📊 Calculating optimal Y-axis scale...")
                max_value = self.get_max_in_region(bigwig_files, chr_name, start, end)
            else:
                max_value = 100.0  # Default fallback
                
            print(f"  📈 Max signal value: {max_value:.1f}")
            
            # Create INI file
            ini_content = self.create_ini_file(bigwig_files, max_value, colors, 
                                              bed_files, gtf_files, bed_colors)
            ini_file = os.path.join(output_dir, f"{file_prefix}tracks_{gene_name}.ini")
            
            with open(ini_file, 'w') as f:
                f.write(ini_content)
            
            # Generate output filename
            region_str = f"{chr_name}_{plot_start}_{plot_end}"
            output_file = os.path.join(output_dir, f"{file_prefix}tracks_{gene_name}_{region_str}.pdf")
            
            # Run pyGenomeTracks
            region_arg = f"{chr_name}:{plot_start}-{plot_end}"
            cmd = [
                "pyGenomeTracks",
                "--tracks", ini_file,
                "--region", region_arg,
                "-t", f"{gene_name}",
                "-o", output_file
            ]
            
            try:
                print(f"  🎨 Generating plot...")
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"  ✅ Created: {output_file}")
                    generated_files.append(output_file)
                    
                    # Clean up INI file if requested
                    if not keep_ini_file:
                        try:
                            os.remove(ini_file)
                            print(f"  🧹 Cleaned up: {os.path.basename(ini_file)}")
                        except Exception as e:
                            print(f"  ⚠️ Warning: Could not remove INI file {ini_file}: {e}")
                else:
                    print(f"  ❌ Error: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Failed to run pyGenomeTracks: {e}")
                
        return generated_files
    
    def quick_plot(self, regions_input: str, bigwig_dir: str = None, 
                   colors: str = None, bed_dir: str = None, bed_colors: str = None,
                   gtf_file: str = None, output: str = None, keep_ini_file: bool = False) -> List[str]:
        """Quick plot generation with minimal configuration"""
        
        # Find BigWig files
        bigwig_files = self.find_bigwig_files(bigwig_dir)
        if not bigwig_files:
            return []
        
        # Find BED files
        bed_files = self.find_bed_files(bed_dir) if bed_dir else []
        
        # Find GTF files - use config if no parameter provided
        if gtf_file:
            gtf_files = self.find_gtf_files(filename=gtf_file)
        else:
            gtf_files = self.find_gtf_files()  # Will use config settings
        
        # Parse colors
        color_list = None
        if colors:
            color_list = [c.strip() for c in colors.split(',')]
            
        bed_color_list = None
        if bed_colors:
            bed_color_list = [c.strip() for c in bed_colors.split(',')]
        
        # Parse regions
        regions = self._parse_regions_input(regions_input)
        if not regions:
            return []
            
        # Generate tracks
        return self.generate_tracks(regions, bigwig_files, color_list, 
                                   bed_files, bed_color_list, gtf_files, 
                                   output=output, keep_ini_file=keep_ini_file)
    
    def _parse_regions_input(self, regions_input: str) -> List[Union[Tuple[str, int, int], Tuple[str, int, int, str]]]:
        """Parse regions from various input formats"""
        regions = []
        
        if os.path.isfile(regions_input):
            # Load from file
            try:
                if regions_input.endswith('.csv'):
                    df = pd.read_csv(regions_input)
                elif regions_input.endswith('.tsv'):
                    df = pd.read_csv(regions_input, sep='\t')
                else:
                    df = pd.read_csv(regions_input, sep=None, engine='python')
                
                # Try common column names
                chr_col = self._find_column(df, ['chr', 'chrom', 'chromosome', 'seqnames'])
                start_col = self._find_column(df, ['start', 'pos', 'position'])
                end_col = self._find_column(df, ['end', 'stop'])
                gene_col = self._find_column(df, ['gene', 'symbol', 'name', 'id'])
                
                for _, row in df.iterrows():
                    chr_name = str(row[chr_col])
                    start = int(row[start_col])
                    end = int(row[end_col])
                    gene = str(row[gene_col]) if gene_col else f"region_{len(regions)+1}"
                    regions.append((chr_name, start, end, gene))
                    
            except Exception as e:
                print(f"❌ Error reading file {regions_input}: {e}")
                return []
        else:
            # Parse single region string
            try:
                # Format: chr1:1000000-2000000 or chr1:1000000-2000000:GENE
                if ':' in regions_input:
                    parts = regions_input.split(':')
                    chr_name = parts[0]
                    coords = parts[1]
                    
                    if '-' in coords:
                        start_str, end_str = coords.split('-')
                        start = int(start_str.replace(',', ''))
                        end = int(end_str.replace(',', ''))
                        
                        gene_name = parts[2] if len(parts) > 2 else f"{chr_name}_{start}_{end}"
                        regions.append((chr_name, start, end, gene_name))
                        
            except Exception as e:
                print(f"❌ Error parsing region {regions_input}: {e}")
                
        return regions
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """Find column by checking multiple possible names (case insensitive)"""
        df_cols_lower = [col.lower() for col in df.columns]
        for name in possible_names:
            if name.lower() in df_cols_lower:
                return df.columns[df_cols_lower.index(name.lower())]
        return None