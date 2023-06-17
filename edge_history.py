import sqlite3
import tempfile
import zipfile
from pathlib import Path

def get_edge_history():
    history_file = Path.home() / 'AppData' / 'Local' / 'Microsoft' / 'Edge' / 'User Data' / 'Default' / 'History'
    if not history_file.exists():
        return []

    try:
        connection = sqlite3.connect(history_file)
        cursor = connection.cursor()
        cursor.execute("SELECT url, title FROM urls")
        results = cursor.fetchall()
        connection.close()
        return results
    except sqlite3.Error as error:
        return []

edge_history = get_edge_history()

# Get the path to the temporary directory
temp_dir = tempfile.gettempdir()

# Create the file path for edge_history.txt in the temporary directory
edge_file = Path(temp_dir) / "edge_history.txt"

if edge_history:
    with open(edge_file, "w", encoding="utf-8") as file:
        file.write("Edge History:\n")
        for url, title in edge_history:
            file.write(f"URL: {url}\n")
            file.write(f"Title: {title}\n\n")

    # Create the path for the ZIP archive
    zip_file = Path(temp_dir) / "Microsoft Edge Data.zip"

    # Create a ZIP archive and add the edge_history.txt file to it
    with zipfile.ZipFile(zip_file, "w") as zipf:
        zipf.write(edge_file, "edge_history.txt")

    # Delete the edge_history.txt file
    edge_file.unlink()

    print("Edge history saved to", zip_file)
else:
    output_file = Path(temp_dir) / "browser_history.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Microsoft Edge is not found/used on this PC.")
    
    print("Microsoft Edge is not found/used on this PC. Output file:", output_file)
