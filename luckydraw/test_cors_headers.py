#!/usr/bin/env python3
"""
Quick test script to verify CORS headers are being set correctly
"""
import requests

def test_cors_headers():
    base_url = "http://127.0.0.1:5000"
    
    print("Testing CORS headers...")
    print("=" * 50)
    
    # Test 1: OPTIONS preflight request
    print("\n1. Testing OPTIONS (preflight) request:")
    try:
        response = requests.options(
            f"{base_url}/api/users",
            headers={
                "Origin": "http://127.0.0.1:5500",
                "Access-Control-Request-Method": "GET"
            }
        )
        print(f"   Status: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'MISSING!')}")
        print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'MISSING!')}")
        print(f"   Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'MISSING!')}")
    except Exception as e:
        print(f"   ERROR: {e}")
        print("   Make sure Flask server is running on http://127.0.0.1:5000")
        return
    
    # Test 2: GET request
    print("\n2. Testing GET request:")
    try:
        response = requests.get(
            f"{base_url}/api/users",
            headers={"Origin": "http://127.0.0.1:5500"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'MISSING!')}")
        print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'MISSING!')}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: POST request
    print("\n3. Testing POST request:")
    try:
        response = requests.post(
            f"{base_url}/api/register/initiate",
            headers={"Origin": "http://127.0.0.1:5500"},
            data={"test": "data"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'MISSING!')}")
        print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'MISSING!')}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("\nIf Access-Control-Allow-Origin shows 'MISSING!', CORS is not configured correctly.")
    print("If it shows '*', CORS should work for all origins.")

if __name__ == "__main__":
    test_cors_headers()

