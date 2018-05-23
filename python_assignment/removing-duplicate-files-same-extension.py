import sys, os, hashlib

def chunk_read(fobj, chunk_size = 1024):
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def remove_duplicate_files(paths, hash = hashlib.sha1):
    hashes = {}
    for path in paths:
        for dir_path, dir_names, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dir_path, filename)
                hash_obj = hash()
                for chunk in chunk_read(open(file_path, 'rb')):
                    hash_obj.update(chunk)
                file_id = (hash_obj.digest(), os.path.getsize(file_path))
                duplicate = hashes.get(file_id, None)
                if duplicate:
                    if input("Duplicate found %s. Enter 1 to delete: " % duplicate):
                        os.remove(duplicate)
                        del hashes[file_id]
                        print("Done")
                else:
                    hashes[file_id] = file_path

if sys.argv[1:]:
    remove_duplicate_files(sys.argv[1:])
