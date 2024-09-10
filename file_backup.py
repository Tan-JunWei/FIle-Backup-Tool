import sys
import os
import shutil
import zipfile
import datetime
import time

# "C:\Users\Admin\Desktop\CS\eJPT\Pen test"

def copy_files(source_directory: str, destination_directory: str):
    '''
    Copy files from the source directory to the destination directory.
    If the file already exists in the destination directory, it will only be copied if it has been modified.
    A log file will be created in the source directory to track the backup operation.

    ARGS:
        source_directory: The directory from which files will be copied.
        destination_directory: The directory to which files will be copied.
    '''
    backed_up_files = 0
    start_time = time.time()
    
    log_file_path = os.path.join(source_directory, "backup_log.txt")
    
    with open(log_file_path, "a") as log_file:
        for root, dirs, files in os.walk(source_directory):
            if os.path.commonpath([root]) == os.path.abspath(destination_directory):
                continue
            
            for filename in files:
                source_file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(source_file_path, source_directory)
                destination_file_path = os.path.join(destination_directory, relative_path)
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

                # Incremental backup logic: Only copy files that have been modified
                if not os.path.exists(destination_file_path) or os.path.getmtime(source_file_path) > os.path.getmtime(destination_file_path):
                    backed_up_files += 1
                    shutil.copy2(source_file_path, destination_file_path)

                    # Log the individual file copy
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"[{current_time}] Copied {source_file_path} to {destination_file_path}\n")
        
        end_time = time.time()
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{current_time}] Total files backed up: {backed_up_files}\n")
        log_file.write(f"Operation duration: {end_time - start_time:.2f} seconds\n\n")

def compress_directory(directory_path: str, zip_file_path: str):
    '''
    Compress a directory into a zip file.

    ARGS:
        directory_path: The directory to be compressed.
        zip_file_path: The name of the zip file to be created.
    '''
    zip_file_path = f"{zip_file_path}.zip"
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, relative_path)
    print(f"Compressed {directory_path} into {zip_file_path}")

def decompress_directory(zip_file_path: str, destination_directory: str):
    '''
    Decompress a zip file into a directory.

    ARGS:
        zip_file_path: The path to the zip file to be decompressed.
        destination_directory: The directory where the zip file contents will be extracted.
    '''
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extractall(destination_directory)
    print(f"Decompressed {zip_file_path} into {destination_directory}")

if len(sys.argv) < 3:
    print("Usage: python data_safe.py <source-directory-path> <destination-directory-path> [compress-flag]")
    sys.exit()

else:
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    if os.path.exists(source_directory) or os.path.isfile(source_directory + ".zip"):
        if len(sys.argv) == 3:
            # Create the destination directory if it doesn't exist
            os.makedirs(destination_directory, exist_ok=True)
            copy_files(source_directory, destination_directory)
            print(f"Backed up files from {source_directory} to {destination_directory}")

        elif len(sys.argv) == 4:
            if sys.argv[3].lower() == 'compress':
                compress_directory(source_directory, destination_directory)
            elif sys.argv[3].lower() == 'decompress':
                os.makedirs(destination_directory, exist_ok=True)
                decompress_directory(source_directory + ".zip", destination_directory)
            else:
                print("Invalid flag. Please use 'compress' or 'decompress'.")

    elif not os.path.exists(source_directory):
        print("Source directory does not exist.")
    
    elif not os.path.isfile(source_directory + ".zip"):
        print("Source zip file does not exist.")

# Improvements
# Edge Case Handling: Ensure the script handles cases like empty directories or permissions issues more gracefully (e.g., adding try-except blocks).
# Compression Flag Validation: Could add more robust validation for the compression flag or support multiple flags for different behaviors.