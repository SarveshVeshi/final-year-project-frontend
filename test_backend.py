import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(name, url, method="GET", json_data=None, expected_status=200):
    print(f"Testing {name} ({method} {url})...", end=" ")
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=json_data)
        
        if response.status_code == expected_status:
            print(f"PASS ({response.status_code})")
            return True
        else:
            print(f"FAIL ({response.status_code})")
            print(f"  Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    all_passed = True
    
    # 1. Server Root
    if not test_endpoint("Root", f"{BASE_URL}/"): all_passed = False
    
    # 2. Static File
    if not test_endpoint("Static CSS", f"{BASE_URL}/static/main.css"): all_passed = False
    
    # 3. API Endpoint (Sign Video Generation)
    payload = {"text": "hello", "language": "ASL"}
    if not test_endpoint("Sign Gen API", f"{BASE_URL}/generate_sign_video_api", method="POST", json_data=payload): all_passed = False
    
    # 4. Sign Text Converter Page
    if not test_endpoint("Converter Page", f"{BASE_URL}/sign-text-converter"): all_passed = False

    if all_passed:
        print("\nAll checks PASSED!")
        sys.exit(0)
    else:
        print("\nSome checks FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
