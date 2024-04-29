import hashlib

def calculate_checksum(data):
    """Calculate the MD5 checksum of byte data."""
    hasher = hashlib.md5()
    hasher.update(data)
    return hasher.hexdigest()

# Example usage:
byte_data = b'Hello, world!'
checksum = calculate_checksum(byte_data)
print("MD5 checksum:", checksum)
