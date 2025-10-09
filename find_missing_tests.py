#!/usr/bin/env python3
"""
Script to find all source files without corresponding test files.
"""
import os
from pathlib import Path

def find_missing_tests():
    """Find all source files that don't have corresponding test files."""
    base_dir = Path(__file__).parent
    source_dirs = [
        'asyncio_functions',
        'bioinformatics_functions',
        'compression_functions',
        'data_types',
        'data_validation',
        'datetime_functions',
        'decorators',
        'env_config_functions',
        'file_functions',
        'http_functions',
        'iterable_functions',
        'json_functions',
        'linux_functions',
        'logger_functions',
        'mathematical_functions',
        'multiprocessing_functions',
        'network_functions',
        'print_functions',
        'security_functions',
        'ssh_functions',
        'strings_utility',
    ]
    
    missing_tests = []
    
    for source_dir in source_dirs:
        source_path = base_dir / source_dir
        if not source_path.exists():
            continue
            
        # Find all Python files (not __init__.py)
        for py_file in source_path.rglob('*.py'):
            if py_file.name == '__init__.py':
                continue
            
            # Calculate relative path from source_dir
            rel_path = py_file.relative_to(source_path)
            
            # Construct expected test file path
            test_file_name = f"test_{py_file.stem}.py"
            test_path = base_dir / 'pytest' / 'unit' / source_dir / rel_path.parent / test_file_name
            
            if not test_path.exists():
                missing_tests.append({
                    'source': str(py_file.relative_to(base_dir)),
                    'expected_test': str(test_path.relative_to(base_dir))
                })
    
    return missing_tests

if __name__ == '__main__':
    missing = find_missing_tests()
    
    if missing:
        print(f"Found {len(missing)} source files without tests:\n")
        for item in sorted(missing, key=lambda x: x['source']):
            print(f"Source: {item['source']}")
            print(f"  Expected test: {item['expected_test']}\n")
    else:
        print("All source files have corresponding test files!")
