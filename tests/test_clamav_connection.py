import pyclamd

try:
    cd = pyclamd.ClamdAgnostic()
    if cd.ping():
        print("ClamAV daemon is running and reachable!")
    else:
        print("ClamAV daemon is not responding.")
except Exception as e:
    print(f"Error connecting to ClamAV: {e}")
