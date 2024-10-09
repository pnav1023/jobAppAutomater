import hashlib

# Function to generate a hash of the resume content
def generate_resume_hash(file_path):
    hash_md5 = hashlib.md5()
    #with open(file_path, "rb") as f:
    for chunk in iter(lambda: file_path.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()