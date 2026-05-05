from easy_tracks import EasyTracks

# Example 1: Display configuration
print("🔧 Loading EasyTracks configuration...")
config_path = "../configs/easy_tracks_config.yaml"  # Relative to examples directory
et = EasyTracks(config_path)
print(et)  # Shows formatted configuration

print("\n" + "="*50)
print("🎯 Generating tracks...")

# Example 2: Using quick_plot for simple string regions (recommended for string input)
et.quick_plot('chr1:3000000-4000000')

# Example 3: Using quick_plot with custom output
et = EasyTracks(config_path)
et.quick_plot('chr1:3000000-4000000', output='myplots/sample1')

# Example 4: Generate tracks with specific output prefix
regions = [('chr1', 3000000, 4000000, 'test_gene')]
bigwig_files = et.find_bigwig_files()
bed_files = et.find_bed_files()
gtf_files = et.find_gtf_files()
et.generate_tracks(regions, bigwig_files, bed_files=bed_files, gtf_files=gtf_files, output='results/experiment1')

# Show configuration anytime for debugging
print("\n🔍 Current configuration:")
et.show_config()