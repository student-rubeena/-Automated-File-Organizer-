import os
import shutil
import hashlib
import logging

# Setup logging to track actions
logging.basicConfig(filename='file_organizer.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to calculate file checksum (MD5 hash)
def calculate_checksum(file_path):
    md5_hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating checksum for {file_path}: {e}")
        return None

# Function to organize files by extension
def organize_files(directory):
    try:
        # Dictionary to store checksums of files
        checksum_dict = {}

        # Iterate through all files in the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = file.split('.')[-1].lower()

                # Calculate file checksum to detect duplicates
                checksum = calculate_checksum(file_path)
                if checksum in checksum_dict:
                    logging.info(f"Duplicate file found: {file_path} (Skipping)")
                    continue  # Skip duplicate files

                checksum_dict[checksum] = file_path

                # Define destination folder based on file extension
                dest_dir = os.path.join(directory, file_ext.upper())

                # Create the folder if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                # Move file to the appropriate subdirectory
                try:
                    shutil.move(file_path, os.path.join(dest_dir, file))
                    logging.info(f"Moved file {file_path} to {dest_dir}")
                except Exception as e:
                    logging.error(f"Error moving file {file_path}: {e}")
    
    except Exception as e:
        logging.error(f"Error organizing files: {e}")

if _name_ == "_main_":
    folder_to_organize = input("Enter the path of the folder to organize: ")
    organize_files(folder_to_organize)
    print("File organization complete. Check 'file_organizer.log' for details.")
