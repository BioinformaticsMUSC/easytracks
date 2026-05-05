#!/usr/bin/env python3
"""
Test script to verify Easy Tracks package installation and basic functionality
"""

def test_import():
    """Test that the package imports correctly"""
    try:
        from easy_tracks import EasyTracks
        from easy_tracks import convert_narrowpeak_to_bed
        print("✅ Package imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_initialization():
    """Test EasyTracks initialization"""
    try:
        from easy_tracks import EasyTracks
        et = EasyTracks()
        print("✅ EasyTracks initialization successful")
        print(f"✅ Default output directory: {et.config['output_dir']}")
        return True
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_string_representation():
    """Test string representation methods"""
    try:
        from easy_tracks import EasyTracks
        et = EasyTracks()
        str_repr = str(et)
        repr_repr = repr(et)
        print("✅ String representation successful")
        print(f"✅ Config display has {len(str_repr.split('\\n'))} lines")
        return True
    except Exception as e:
        print(f"❌ String representation error: {e}")
        return False

def test_utility_functions():
    """Test utility functions"""
    try:
        from easy_tracks import create_example_regions_file
        success = create_example_regions_file("test_regions.csv")
        if success:
            print("✅ Utility functions working")
            # Clean up
            import os
            if os.path.exists("test_regions.csv"):
                os.remove("test_regions.csv")
        return success
    except Exception as e:
        print(f"❌ Utility function error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Easy Tracks Package")
    print("=" * 40)
    
    tests = [
        test_import,
        test_initialization, 
        test_string_representation,
        test_utility_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        print(f"\\n🔍 Running {test_func.__name__}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_func.__name__} failed")
    
    print(f"\\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        return False

if __name__ == "__main__":
    main()