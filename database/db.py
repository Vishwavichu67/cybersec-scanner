from pymongo import MongoClient

def get_mongo_collection():
    """Establish a connection to MongoDB and return the 'scans' collection."""
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["cybersec_scanner"]  # Database name
        return db.scans  # Collection name
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return None

def save_scan_result(target, scan_type, result):
    """Skip saving if MongoDB is not installed."""
    print(f"Skipping database save. Scan result for {target}: {scan_type}")

def get_scan_results(target):
    """Retrieve all scan results for a given target."""
    collection = get_mongo_collection()
    if collection:
        return list(collection.find({"target": target}, {"_id": 0}))
    return []
