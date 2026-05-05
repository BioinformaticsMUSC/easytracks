#!/usr/bin/env python3
"""
Easy Tracks Command Line Interface
"""

import argparse
import os
from .core import EasyTracks


def main():
    """Main command line interface for Easy Tracks"""
    parser = argparse.ArgumentParser(
        description='Easy Tracks: User-friendly pyGenomeTracks generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Plot single region
  easy-tracks --region "chr1:1000000-2000000:MYC"
  
  # Plot with BED peaks and GTF annotations
  easy-tracks --region regions.csv --bed_dir bed --gtf_file annotation.gtf
  
  # Plot from CSV file with custom colors  
  easy-tracks --region regions.csv --colors "red,blue,green" --bed_colors "orange,purple"
  
  # Plot with custom output directory
  easy-tracks --region regions.csv --output "my_plots/"
  
  # Plot with file prefix
  easy-tracks --region regions.csv --output "results/sample1"
  
  # Use custom BigWig directory with peaks
  easy-tracks --region regions.csv --bigwig_dir /path/to/bigwigs --bed_dir /path/to/peaks
  
  # Interactive mode (prompts for input)
  easy-tracks --interactive
        """
    )
    
    parser.add_argument('--region', '-r', 
                       help='Region(s) to plot: file path or "chr:start-end:gene"')
    parser.add_argument('--bigwig_dir', '-b', 
                       help='Directory containing BigWig files (default: bigwig_files)')
    parser.add_argument('--bed_dir', 
                       help='Directory containing BED/peak files (default: bed)')
    parser.add_argument('--gtf_file', '-g',
                       help='GTF/GFF annotation file to include')
    parser.add_argument('--colors', '-c',
                       help='Comma-separated colors for tracks (e.g., "red,blue,green")')
    parser.add_argument('--bed_colors',
                       help='Comma-separated colors for BED tracks')
    parser.add_argument('--output', '-o',
                       help='Output directory or file prefix (default: from config)')
    parser.add_argument('--config', 
                       help='YAML configuration file')
    parser.add_argument('--keep-ini', action='store_true',
                       help='Keep INI configuration files after plotting (default: remove them)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode with prompts')
    
    args = parser.parse_args()
    
    # Initialize EasyTracks
    easy_tracks = EasyTracks(args.config)
    
    if args.interactive or not args.region:
        # Interactive mode
        print("🎨 Easy Tracks - Interactive Mode")
        print("=" * 40)
        
        # Get BigWig directory
        bw_dir = input(f"BigWig directory [{easy_tracks.config['bigwig_dir']}]: ").strip()
        if not bw_dir:
            bw_dir = easy_tracks.config['bigwig_dir']
            
        # Get region
        print("\nRegion format examples:")
        print("  chr1:1000000-2000000:MYC")
        print("  path/to/regions.csv")
        region_input = input("\nRegion(s) to plot: ").strip()
        
        # Get BED files (optional)
        bed_dir = input(f"\nBED/peaks directory [optional, default: {easy_tracks.config['bed_dir']}]: ").strip()
        if not bed_dir:
            bed_dir = easy_tracks.config['bed_dir'] if os.path.exists(easy_tracks.config['bed_dir']) else None
            
        # Get GTF file (optional)
        gtf_file = input("\nGTF/annotation file path [optional]: ").strip()
        if not gtf_file:
            gtf_file = None
        
        # Get colors (optional)
        colors = input("\nBigWig colors (comma-separated, optional): ").strip()
        if not colors:
            colors = None
            
        bed_colors = input("\nBED colors (comma-separated, optional): ").strip()
        if not bed_colors:
            bed_colors = None
            
        # Get output (optional)
        output = input(f"\nOutput directory or prefix [optional, default: {easy_tracks.config['output_dir']}]: ").strip()
        if not output:
            output = None
        
        # Ask about keeping INI files
        keep_ini_input = input("\nKeep INI configuration files? [y/N]: ").strip().lower()
        keep_ini = keep_ini_input.startswith('y')
            
        # Generate tracks
        files = easy_tracks.quick_plot(region_input, bw_dir, colors, bed_dir, bed_colors, 
                                      gtf_file, output, keep_ini_file=keep_ini)
        
    else:
        # Command line mode
        files = easy_tracks.quick_plot(args.region, args.bigwig_dir, args.colors, 
                                      args.bed_dir, args.bed_colors, args.gtf_file, 
                                      args.output, keep_ini_file=args.keep_ini)
    
    # Summary
    if files:
        print(f"\n🎉 Successfully generated {len(files)} track plots!")
        print("Generated files:")
        for f in files:
            print(f"  📊 {f}")
    else:
        print("\n❌ No tracks were generated. Please check your inputs.")


if __name__ == "__main__":
    main()