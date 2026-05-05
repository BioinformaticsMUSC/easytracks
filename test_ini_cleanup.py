#!/usr/bin/env python3
"""
Test the new keep_ini_file functionality
"""

from easy_tracks import EasyTracks
import os

def test_ini_cleanup():
    """Test that INI files are cleaned up when keep_ini_file=False"""
    
    print("🧪 Testing INI file cleanup functionality...")
    
    # Initialize EasyTracks
    config_file = "easy_tracks_config.yaml"
    if not os.path.exists(config_file):
        print(f"⚠️  Config file {config_file} not found, using defaults")
        et = EasyTracks()
    else:
        et = EasyTracks(config_file)
    
    # Test regions
    test_regions = [('chr1', 1000000, 1100000)]  # Single test region
    
    print("\n📋 Test 1: Default behavior (keep_ini_file=False)")
    print("="*50)
    
    bigwig_files = et.find_bigwig_files()
    if not bigwig_files:
        print("❌ No BigWig files found!")
        return False
    
    # Test default behavior (should clean up INI files)
    output_dir = "test_output_default"
    files = et.generate_tracks(
        test_regions, 
        bigwig_files, 
        output=output_dir
        # keep_ini_file defaults to False
    )
    
    if files:
        print(f"✅ Generated {len(files)} plot(s)")
        
        # Check if INI files exist
        ini_files = [f for f in os.listdir(output_dir) if f.endswith('.ini')]
        if ini_files:
            print(f"❌ Found {len(ini_files)} INI files - they should have been cleaned up!")
            for ini_file in ini_files:
                print(f"   - {ini_file}")
        else:
            print("✅ No INI files found - cleanup worked correctly!")
    
    print("\n📋 Test 2: Keep INI files (keep_ini_file=True)")
    print("="*50)
    
    # Test keeping INI files
    output_dir2 = "test_output_keep_ini"
    files2 = et.generate_tracks(
        test_regions, 
        bigwig_files, 
        output=output_dir2,
        keep_ini_file=True
    )
    
    if files2:
        print(f"✅ Generated {len(files2)} plot(s)")
        
        # Check if INI files exist
        ini_files2 = [f for f in os.listdir(output_dir2) if f.endswith('.ini')]
        if ini_files2:
            print(f"✅ Found {len(ini_files2)} INI files - kept as requested!")
            for ini_file in ini_files2:
                print(f"   - {ini_file}")
        else:
            print("❌ No INI files found - they should have been kept!")
    
    print("\n🎉 INI file cleanup tests completed!")
    print("\nℹ️  Usage examples:")
    print("   # Default behavior - cleans up INI files")
    print("   et.generate_tracks(regions, bigwig_files)")
    print("   et.quick_plot('chr1:1000000-2000000')")
    print()
    print("   # Keep INI files for debugging")
    print("   et.generate_tracks(regions, bigwig_files, keep_ini_file=True)")
    print("   et.quick_plot('chr1:1000000-2000000', keep_ini_file=True)")
    print()
    print("   # CLI usage")
    print("   easy-tracks --region 'chr1:1000000-2000000'  # default cleanup")
    print("   easy-tracks --region 'chr1:1000000-2000000' --keep-ini  # keep files")

if __name__ == "__main__":
    test_ini_cleanup()