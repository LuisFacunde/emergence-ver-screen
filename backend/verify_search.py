from app import create_app
from utils.database import get_oracle_connection
from utils.files import search_patient_files
import sys
import os

# Add backend to path if needed (running from backend dir)
sys.path.append(os.getcwd())

def verify_setup():
    print("--- Verifying Setup ---")
    
    # 1. Test Oracle Connection
    print("\n1. Testing Oracle Connection and Query...")
    try:
        conn = get_oracle_connection()
        print("✅ Oracle Connection Successful!")
        
        cursor = conn.cursor()
        print("   Executing simple query (DUAL)...")
        cursor.execute("SELECT 1 FROM DUAL")
        print("   ✅ Simple Query (DUAL) Successful!")
        
        print("   Executing table query (PACIENTE) with ROWNUM...")
        print("   Query: SELECT cd_paciente, nm_paciente, dt_nascimento FROM paciente WHERE ROWNUM <= 1")
        cursor.execute("SELECT cd_paciente, nm_paciente, dt_nascimento FROM paciente WHERE ROWNUM <= 1")
        row = cursor.fetchone()
        print(f"   ✅ Table Query Successful! Result: {row}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Oracle Error: {e}")

    # 2. Test File Search (Mock)
    print("\n2. Testing File Search Logic...")
    # Create a dummy file to find
    dummy_prontuario = "TEST123"
    dummy_dir = "test_files"
    os.makedirs(dummy_dir, exist_ok=True)
    dummy_file = os.path.join(dummy_dir, f"{dummy_prontuario}-report.pdf")
    with open(dummy_file, 'w') as f:
        f.write("dummy content")
        
    # Temporarily override config path
    from config import get_config
    config = get_config()
    original_path = config.FILES_BASE_PATH
    config.FILES_BASE_PATH = os.path.abspath(dummy_dir)
    
    try:
        files = search_patient_files(dummy_prontuario)
        if files and files[0]['name'] == f"{dummy_prontuario}-report.pdf":
            print(f"✅ File Search Successful! Found: {files[0]['name']}")
        else:
            print(f"❌ File Search Failed. Found: {files}")
            
    except Exception as e:
        print(f"❌ File Search Logic Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
        if os.path.exists(dummy_dir):
            os.rmdir(dummy_dir)
        config.FILES_BASE_PATH = original_path

if __name__ == "__main__":
    verify_setup()
