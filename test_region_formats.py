#!/usr/bin/env python3
"""
Test script to demonstrate flexible region tuple handling
"""

def test_region_formats():
    """Test that both 3 and 4 element region tuples work"""
    
    print("🧪 Testing flexible region tuple formats...")
    
    # Test different region formats
    regions_3_element = [
        ('chr1', 1000000, 1100000),  # No gene name
        ('chr2', 2000000, 2100000),  # No gene name
    ]
    
    regions_4_element = [
        ('chr1', 1000000, 1100000, 'MYC'),      # With gene name
        ('chr2', 2000000, 2100000, 'BRAF'),     # With gene name
    ]
    
    mixed_regions = [
        ('chr1', 1000000, 1100000),              # 3-element
        ('chr2', 2000000, 2100000, 'BRAF'),     # 4-element
        ('chr3', 3000000, 3100000),              # 3-element
    ]
    
    invalid_regions = [
        ('chr1', 1000000),                       # Too few elements
        ('chr2', 2000000, 2100000, 'GENE', 'extra'),  # Too many elements
    ]
    
    def process_regions(regions, test_name):
        print(f"\n📋 {test_name}:")
        for i, region in enumerate(regions):
            try:
                # Handle both 3-element and 4-element tuples
                if len(region) == 3:
                    chr_name, start, end = region
                    gene_name = f"{chr_name}_{start}_{end}"
                    print(f"  ✅ Region {i+1}: {chr_name}:{start}-{end} → {gene_name}")
                elif len(region) == 4:
                    chr_name, start, end, gene_name = region
                    print(f"  ✅ Region {i+1}: {chr_name}:{start}-{end} → {gene_name}")
                else:
                    print(f"  ❌ Region {i+1}: Invalid format {region}")
                    continue
            except Exception as e:
                print(f"  ❌ Region {i+1}: Error processing {region}: {e}")
    
    # Test all formats
    process_regions(regions_3_element, "3-element tuples (auto-generated names)")
    process_regions(regions_4_element, "4-element tuples (explicit names)")
    process_regions(mixed_regions, "Mixed 3 and 4-element tuples")
    process_regions(invalid_regions, "Invalid region formats")
    
    print("\n✅ Region format flexibility test completed!")
    print("\nℹ️  Usage examples:")
    print("   # 3-element tuples (gene names auto-generated)")
    print("   regions = [('chr1', 1000000, 1100000), ('chr2', 2000000, 2100000)]")
    print()
    print("   # 4-element tuples (explicit gene names)")  
    print("   regions = [('chr1', 1000000, 1100000, 'MYC'), ('chr2', 2000000, 2100000, 'BRAF')]")
    print()
    print("   # Mixed formats work too!")
    print("   regions = [('chr1', 1000000, 1100000), ('chr2', 2000000, 2100000, 'BRAF')]")

if __name__ == "__main__":
    test_region_formats()