import urllib.request
import urllib.error

url = "http://localhost:5000/api/patients/search?prontuario=2345170"

print(f"Requesting {url}...")
try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
        with open("debug_response.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print("Response saved to debug_response.txt")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    content = e.read().decode('utf-8')
    with open("debug_response.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Error response saved to debug_response.txt")
except Exception as e:
    print(f"Error: {e}")

