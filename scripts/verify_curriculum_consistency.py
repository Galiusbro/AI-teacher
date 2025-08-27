#!/usr/bin/env python3
"""
Script to verify consistency between curriculum files and module files.
Checks if module IDs match between curriculum overview and detailed modules.
"""

import os
import json
import glob


def load_json_file(file_path):
    """Load and parse JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None


def get_curriculum_modules(curriculum_file):
    """Extract all module IDs from a curriculum file."""
    modules = []
    data = load_json_file(curriculum_file)
    if not data:
        return modules
    
    for stage in data.get('stages', []):
        for module in stage.get('modules', []):
            modules.append({
                'id': module.get('id'),
                'title': module.get('title'),
                'stage': stage.get('id'),
                'subject': data.get('subject')
            })
    
    return modules


def get_module_files(modules_dir):
    """Get all module files and their content."""
    module_files = {}
    
    for file_path in glob.glob(os.path.join(modules_dir, "**", "*.json"), recursive=True):
        data = load_json_file(file_path)
        if data:
            if isinstance(data, list):
                for module in data:
                    module_files[module.get('id')] = {
                        'file': os.path.relpath(file_path, modules_dir),
                        'subject': module.get('subject'),
                        'stage': module.get('stage'),
                        'title': module.get('title')
                    }
            else:
                module_files[data.get('id')] = {
                    'file': os.path.relpath(file_path, modules_dir),
                    'subject': data.get('subject'),
                    'stage': data.get('stage'),
                    'title': data.get('title')
                }
    
    return module_files


def verify_consistency(curriculum_dir, modules_dir):
    """Verify consistency between curriculum and module files."""
    print("🔍 Verifying curriculum consistency...")
    print("=" * 60)
    
    # Get all curriculum files
    curriculum_files = glob.glob(os.path.join(curriculum_dir, "curriculum_*.json"))
    
    total_issues = 0
    
    for curriculum_file in curriculum_files:
        subject_name = os.path.basename(curriculum_file).replace('curriculum_', '').replace('.json', '')
        print(f"\n📚 Checking {subject_name.upper()}:")
        
        # Get modules from curriculum file
        curriculum_modules = get_curriculum_modules(curriculum_file)
        
        if not curriculum_modules:
            print(f"  ⚠️  No modules found in curriculum file")
            continue
        
        # Get all module files
        all_modules = get_module_files(modules_dir)
        
        issues = 0
        
        for module_info in curriculum_modules:
            module_id = module_info['id']
            
            if module_id not in all_modules:
                print(f"  ❌ Module {module_id} from curriculum not found in modules/")
                issues += 1
                continue
            
            # Check subject consistency
            if module_info['subject'] != all_modules[module_id]['subject']:
                print(f"  ⚠️  Subject mismatch for {module_id}:")
                print(f"     Curriculum: {module_info['subject']}")
                print(f"     Module: {all_modules[module_id]['subject']}")
                issues += 1
            
            # Check stage consistency
            if module_info['stage'] != all_modules[module_id]['stage']:
                print(f"  ⚠️  Stage mismatch for {module_id}:")
                print(f"     Curriculum: {module_info['stage']}")
                print(f"     Module: {all_modules[module_id]['stage']}")
                issues += 1
        
        # Check for orphaned modules (in modules/ but not in curriculum)
        curriculum_module_ids = {m['id'] for m in curriculum_modules}
        for module_id, module_data in all_modules.items():
            if (module_data['subject'].lower().replace(' ', '') == subject_name.replace('_', '') and
                module_id not in curriculum_module_ids):
                print(f"  ⚠️  Module {module_id} in modules/ but not in curriculum")
                issues += 1
        
        if issues == 0:
            print(f"  ✅ All {len(curriculum_modules)} modules consistent")
        else:
            print(f"  ❌ Found {issues} issues")
            total_issues += issues
    
    print(f"\n{'='*60}")
    if total_issues == 0:
        print("🎉 All curriculum files are consistent with module files!")
    else:
        print(f"⚠️  Found {total_issues} consistency issues that need attention")


def main():
    """Main function."""
    curriculum_dir = "curriculum"
    modules_dir = "curriculum/modules"
    
    if not os.path.exists(curriculum_dir):
        print(f"❌ Curriculum directory not found: {curriculum_dir}")
        return
    
    if not os.path.exists(modules_dir):
        print(f"❌ Modules directory not found: {modules_dir}")
        return
    
    verify_consistency(curriculum_dir, modules_dir)


if __name__ == "__main__":
    main()
