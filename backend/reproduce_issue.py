import sys
import os
import logging

# Add backend to path if needed (running from backend dir)
sys.path.append(os.getcwd())

from utils.files import search_patient_files, clear_file_cache
from config import get_config

def reproduce():
    with open('reproduce_log.txt', 'w') as log_file:
        def log(msg):
            print(msg)
            log_file.write(str(msg) + "\n")
            
        log("--- Reproduction Script for Patient 2209394 ---")
        
        # 0. Check Config
        config = get_config()
        log("Configuration:")
        log(f"FILES_BASE_PATHS: {config.FILES_BASE_PATHS}")
        
        # 1. Clear Cache to ensure fresh search
        clear_file_cache()
        
        # 2. Search
        prontuario = "2209394"
        log(f"\nSearching for patient: {prontuario}")
        
        try:
            files = search_patient_files(prontuario, count_only=False)
            
            log(f"\nResults: found {len(files)} files.")
            for f in files:
                log(f" - {f.get('name')} ({f.get('path')})")
                
            if not files:
                log("\n❌ NO FILES FOUND. Debugging strategies:")
                # Manually check paths
                for base in config.FILES_BASE_PATHS:
                    log(f"\nChecking base path: {base}")
                    if os.path.exists(base):
                        log("  ✅ Base path exists.")
                        # Check subdir
                        patient_dir = os.path.join(base, prontuario)
                        log(f"  Checking specific dir: {patient_dir}")
                        if os.path.exists(patient_dir):
                            log("    ✅ Patient directory exists!")
                            try:
                                contents = os.listdir(patient_dir)
                                log(f"    Contents: {contents}")
                            except Exception as e:
                                log(f"    ❌ Error listing directory: {e}")
                        else:
                            log("    ❌ Patient directory does NOT exist.")
                            
                        # Check glob pattern 2
                        import glob
                        pattern = os.path.join(base, f"{prontuario}-*")
                        log(f"  Checking glob pattern: {pattern}")
                        matches = glob.glob(pattern)
                        log(f"    Matches found: {len(matches)}")
                        for m in matches[:5]:
                            log(f"      - {m}")
                    else:
                        log("  ❌ Base path does NOT exist or is inaccessible.")
                        
        except Exception as e:
            log(f"❌ Error during search: {e}")
            import traceback
            traceback.print_exc(file=log_file)

if __name__ == "__main__":
    reproduce()
