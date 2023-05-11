# MP4 to MP3 Converter

This is a Python script that converts MP4 recordings to MP3 format. It provides options to convert the most recent recording or all recordings for the current day.

## Prerequisites

- Python 3.7 or higher
- Required Python packages listed in the `requirements.txt` file

## Installation

 Clone the repository:


   `git clone https://github.com/jeff502/mp4-to-mp3-converter.git`
   
## Usage

    Set up the environment variables:

        Create a .env file in the project directory.

        Specify the paths for the FOLDER_PATH and DESTINATION_PATH variables in the .env file. These paths should point to the input MP4 recordings folder and the destination folder for the converted MP3 files, respectively.

    `FOLDER_PATH=/path/to/mp4_recordings`
    `DESTINATION_PATH=/path/to/mp3_files`

Run the script:
  `python main.py`

Follow the on-screen prompts to select an option:

    Press '1' for converting the most recent recording.
    Press '2' for converting all recordings for the current day.

## License
MIT License
