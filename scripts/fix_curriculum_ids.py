#!/usr/bin/env python3
"""
Script to fix curriculum file IDs to match module IDs.
Adds 'module_' prefix to all module IDs in curriculum files.
"""

import os
import json
import glob
import re


def load_json_file(file_path):
    """Load and parse JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None


def save_json_file(file_path, data):
    """Save data to JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving {file_path}: {e}")
        return False


def fix_module_ids_in_curriculum(curriculum_file):
    """Fix module IDs in a curriculum file by adding 'module_' prefix."""
    print(f"🔧 Fixing: {os.path.basename(curriculum_file)}")
    
    data = load_json_file(curriculum_file)
    if not data:
        return False
    
    changes_made = 0
    
    # Process each stage
    for stage in data.get('stages', []):
        for module in stage.get('modules', []):
            old_id = module.get('id', '')
            
            # Check if ID already has 'module_' prefix
            if old_id and not old_id.startswith('module_'):
                new_id = f"module_{old_id}"
                module['id'] = new_id
                changes_made += 1
                print(f"  ✓ {old_id} → {new_id}")
    
    if changes_made > 0:
        if save_json_file(curriculum_file, data):
            print(f"  💾 Saved {changes_made} changes")
            return True
        else:
            print(f"  ❌ Failed to save changes")
            return False
    else:
        print(f"  ⏭️  No changes needed")
        return True


def main():
    """Main function to fix all curriculum files."""
    print("🔧 Fixing curriculum file IDs to match module IDs...")
    print("=" * 60)
    
    curriculum_dir = "curriculum"
    
    if not os.path.exists(curriculum_dir):
        print(f"❌ Curriculum directory not found: {curriculum_dir}")
        return
    
    # Get all curriculum files
    curriculum_files = glob.glob(os.path.join(curriculum_dir, "curriculum_*.json"))
    
    if not curriculum_files:
        print(f"❌ No curriculum files found in {curriculum_dir}")
        return
    
    print(f"Found {len(curriculum_files)} curriculum files to process")
    print()
    
    success_count = 0
    total_count = 0
    
    for curriculum_file in curriculum_files:
        total_count += 1
        if fix_module_ids_in_curriculum(curriculum_file):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"✅ Fixed {success_count}/{total_count} curriculum files")
    
    if success_count == total_count:
        print("🎉 All curriculum files have been updated!")
        print("\nNow you can run the consistency check again to verify.")
    else:
        print("⚠️  Some files failed to update. Check the errors above.")


if __name__ == "__main__":
    main()
