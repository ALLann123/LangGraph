#!/usr/bin/python3
import speedtest

def run_speedtest():
    """
    Run a speed test (download, upload, ping).
    Returns:
        dict with server info and speed results
    """
    # Create a Speedtest object
    test = speedtest.Speedtest()

    # Load server list
    test.get_servers()

    # Pick the best server
    best = test.get_best_server()

    # Run download & upload tests
    download_result = test.download()
    upload_result = test.upload()
    ping_result = test.results.ping

    # Convert to Mbps
    download_mbps = round(download_result / 1024 / 1024, 2)
    upload_mbps = round(upload_result / 1024 / 1024, 2)

    # Return results as dictionary
    return {
        "server": {
            "host": best["host"],
            "country": best["country"],
            "sponsor": best["sponsor"],
        },
        "ping_ms": ping_result,
        "download_mbps": download_mbps,
        "upload_mbps": upload_mbps,
    }


# Example usage
if __name__ == "__main__":
    results = run_speedtest()
    print(results)
