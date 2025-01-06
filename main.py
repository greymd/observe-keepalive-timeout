import http.client
import time
import ssl
import sys
import subprocess

def get_connection_status(port):
    try:
        result = subprocess.run(["ss", "-tna", "sport", str(port)], stdout=subprocess.PIPE)
        # Example output:
        # ~~~~~~~~~~
        # State Recv-Q Send-Q Local Address:Port Peer Address:Port
        # TIME-WAIT 0 0 10.4.0.7:34296 93.184.215.14:80
        # ~~~~~~~~~~

        # Retrive the connection status from the output
        # Search for :port in the output and get the first column
        for line in result.stdout.decode("utf-8").split("\n"):
            if f":{port}" in line:
                return line.split()[0]
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    return None

def main(url):
    # remove the protocol (*://) from the URL
    url_parts = url.split("://", 1)[-1].split("/", 1)
    domain = url_parts[0]
    path = "/" + (url_parts[1] if len(url_parts) > 1 else "")
    max_wait_time = 1024
    conn = http.client.HTTPSConnection(domain, timeout=max_wait_time, context=ssl._create_unverified_context())
    conn.request("GET", path, headers={"Connection": "keep-alive"})
    response = conn.getresponse()
    for header, value in response.getheaders():
        print(f"{header}: {value}")
    print(response.read().decode("utf-8"), file=sys.stderr)
    for i in range(0, max_wait_time):
        # check if the connection status is not ESTAB
        conn_status = get_connection_status(conn.sock.getsockname()[1])
        if conn_status != "ESTAB":
            print(f"Connection is in {conn_status} state", file=sys.stderr)
            break
        print(f"Waiting for {i} seconds, connection = {conn_status}")
        time.sleep(1)
    conn.close()

if __name__ == "__main__":
    if len (sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <URL>", file=sys.stderr)
        print(f"  i.e: python3 {sys.argv[0]} https://example.com/", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
