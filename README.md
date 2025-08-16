# Python Data Pipeline for Image Datasets

A simple and robust Python script that automates the cleaning, validation, and processing of image datasets for machine learning projects.

This pipeline ensures that only high-quality, valid data is used for training AI models by inspecting each file, logging its metadata, and sorting it based on a defined set of rules.

### Core Features

*   **Validates Images:** Checks each file for corruption, correct file format (`.jpg`, `.png`, `.jpeg`), and minimum dimensions.
*   **Extracts Metadata:** Gathers key information like image dimensions (width, height), file size, and image format.
*   **Logs to a Database:** Records the results for every file, both passed and failed, into a structured SQLite database for easy querying and analysis.
*   **Sorts Files:** Automatically moves files to `validated` or `bad` folders based on the inspection outcome.

### Tech Stack

*   **Language:** Python 3
*   **Libraries:**
    *   `Pillow (PIL)`: For image inspection and validation.
    *   `SQLite3`: For database management.
    *   `tqdm`: For displaying a clean progress bar.
    *   `pathlib`: For modern, OS-agnostic path management.

### Setup and Usage

To run this pipeline, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/thonmay/python-data-pipeline.git
    cd python-data-pipeline
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
    

3.  **Add data:**
    *   Place your raw image files into the `source_data` folder. (I already put around 1000 images)

4.  **Set up the database:**
    *   This script only needs to be run once to create the database file and table.
    ```bash
    python setup_database.py
    ```

5.  **Run the pipeline:**
    ```bash
    python main_pipeline.py
    ```
    The script will process all files in `source_data`, populate the `image_metadata.db`, and move the files to the appropriate `processed_data` subfolders.


