import os
import re
import subprocess
import sys

DIRECTORY = "."
EXTENSIONS = (".m4v", ".mp4", ".mov")

def parse_date_from_filename(filename):
    pattern = r"Clip-(\d{4})-(\d{2})-(\d{2})\s+(\d{2});(\d{2});(\d{2})-\d{2}"
    match = re.search(pattern, filename)
    
    if match:
        year, month, day, hour, minute, second = match.groups()
        formatted_date = f"{year}:{month}:{day} {hour}:{minute}:{second}"
        return formatted_date
    return None

def update_metadata(filepath, date_string):
    print(f"Processing: {filepath} -> {date_string}")
    
    try:
        cmd = [
            "exiftool",
            "-overwrite_original",
            "-api", "QuickTimeUTC=1",
            f"-AllDates={date_string}",
            f"-Track*Date={date_string}",
            f"-Media*Date={date_string}",
            f"-FileModifyDate={date_string}",
            filepath
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"SUCCESS: {os.path.basename(filepath)}")
        else:
            print(f"ERROR processing {filepath}: {result.stderr}")
            
    except FileNotFoundError:
        print("ERROR: 'exiftool' is not installed or not in your PATH.")
        sys.exit(1)

def main():
    print(f"Scanning directory: {os.path.abspath(DIRECTORY)}\n")
    files_found = 0
    
    for filename in os.listdir(DIRECTORY):
        if filename.lower().endswith(EXTENSIONS):
            date_string = parse_date_from_filename(filename)
            if date_string:
                files_found += 1
                filepath = os.path.join(DIRECTORY, filename)
                update_metadata(filepath, date_string)

    if files_found == 0:
        print("No matching files found. Check your filename pattern.")
    else:
        print(f"\nFinished processing {files_found} files.")

if __name__ == "__main__":
    main()