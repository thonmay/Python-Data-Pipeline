import sqlite3
import shutil
from pathlib import Path
from PIL import Image
from datetime import datetime
from tqdm import tqdm


SOURCE_DIR = Path("source_data")

VALIDATED_DIR = Path("processed_data/validated")
BAD_DIR = Path("processed_data/bad")

DB_FILE = "image_metadata.db"

ALLOWED_FORMATS = ['.png', '.jpeg', '.jpg']

MIN_WIDTH = 100   # in pixel

# The Inspector
def process_image(img_path : Path):
    """
    Validates each image and extracts it metadata, returning a dictionary 
    """
    
    # Assuming the file has failed initially
    result = {
        "filename": img_path.name,
        "validation_status": "FAILED",
        "notes": "Unknown error has occured."
    }
    
    try:
        # Check 1
        if img_path.suffix.lower() not in ALLOWED_FORMATS:
            raise ValueError(f"Invalid file format {img_path}")
        
        with Image.open(img_path) as img:
            img.verify()            # checks for corruption and raises exception on error
        
        with Image.open(img_path) as img:
            width, height = img.size
            image_format = img.format
            
            if width < MIN_WIDTH:
                raise ValueError(f"File {img_path} is below minimum({MIN_WIDTH})px resolution")
            
            
            size_kb = img_path.stat().st_size / 1024
            
            if size_kb < 10: 
                raise ValueError(f"File {img_path} is too small")
            
            # All checks have passed here
            # Updating the result
            result.update({
                "validation_status": "PASSED",
                "width": width,
                "height": height,
                "size_kb": round(size_kb, 2),
                "format": image_format,
                "notes": "Validation successfull"
            })

            
            
        
    except Exception as e:
        result["notes"] = str(e)
        
    return result


# The Manager
def main():
    """
    Overlooks the entire process
    """
    
    print("Starting the Pipeline...")
    
    # Making sure Destination folders exists
    VALIDATED_DIR.mkdir(parents=True, exist_ok =True)
    BAD_DIR.mkdir(parents=True, exist_ok =True)
        
    img_paths = list(SOURCE_DIR.iterdir())
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print(f"Found {len(img_paths)} images to process.")
    
    # Iterating throught the images with a progress bar and skipping folders
    for img in tqdm(img_paths, desc="Processing Images...."):
        if not img.is_file():
            continue
        
        # Step 1. Get the report from the Inspector
        metadata = process_image(img)
        
        # Step 2. Add timestamp to the Metadata
        metadata["timestamp"] = datetime.now().isoformat()
        
        # Step 3. Insert Metadata into the Database
        if metadata["validation_status"] == "PASSED":
            cursor.execute(
                """
                INSERT INTO img_data(filename, width, height, size_kb, format, validation_status, notes, processed_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metadata["filename"], metadata["width"], metadata["height"], metadata["size_kb"], metadata["format"], metadata["validation_status"], metadata["notes"], metadata["timestamp"]
                    )
            )
            # Step 4.1 Move the image to the appropriate folder
            shutil.move(str(img), VALIDATED_DIR/img.name)
        else:
            cursor.execute(
                """
                INSERT INTO img_data(filename, validation_status, notes, processed_timestamp)
                VALUES (?, ?, ?, ?)
                """, (
                    metadata["filename"], metadata["validation_status"], metadata["notes"], metadata["timestamp"]
                )
            )
            # 4.2
            shutil.move(str(img), BAD_DIR/img.name)
            
            
    # Commiting the changes made and closing the connection
    conn.commit()
    conn.close()
    
    print("Pipeline closed successfully")
    

if __name__ == "__main__":
    main()
    
    
    