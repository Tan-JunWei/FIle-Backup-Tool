import sys
import os
import shutil
import zipfile
import datetime
import time

def copy_files(source_directory: str, destination_directory: str):
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

def compress_directory(directory_path: str, zip_name: str):
    zip_file_path = f"{zip_name}.zip"
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, relative_path)
    print(f"Compressed {directory_path} into {zip_file_path}")

if len(sys.argv) < 3:
    print("Usage: python data_safe.py <source-directory-path> <destination-directory-path> [compress-flag]")
    sys.exit()

else:
    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    if os.path.exists(source_directory):
        copy_files(source_directory, destination_directory)

        # Check if the user wants to compress the destination directory
        if len(sys.argv) == 4 and sys.argv[3].lower() == 'compress':
            compress_directory(destination_directory, destination_directory)
        
        elif len(sys.argv) == 4:
            print("Invalid compress flag. Please use 'compress' to compress the destination directory.")
        
        else:
            print("Backup completed successfully.")
