from utils.database import get_oracle_connection
import oracledb

try:
    conn = get_oracle_connection()
    cursor = conn.cursor()
    
    # Check columns
    print("--- Columns in EXAMES table ---")
    cursor.execute("SELECT column_name FROM all_tab_columns WHERE table_name = 'EXAMES' AND owner = 'DBAMV'") # Assuming DBAMV, or just filter by table name
    # Using simple query if permission issues with all_tab_columns
    try:
        cursor.execute("SELECT * FROM exames WHERE ROWNUM <= 1")
        print([col[0] for col in cursor.description])
    except:
        print("Could not describe table, trying generic select")
        
    # Get sample data
    print("\n--- Sample Data (nome_exame, tipo) ---")
    try:
        cursor.execute("SELECT nome_exame, tipo FROM exames WHERE ROWNUM <= 10")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"Error selecting data: {e}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Connection error: {e}")
