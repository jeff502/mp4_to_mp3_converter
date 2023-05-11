import os

from datetime import datetime
from dotenv import dotenv_values
from moviepy.editor import VideoFileClip

from folder_logic import (
    collapse_sub_folders,
    get_most_recent_recording,
    get_all_recordings_for_today,
)


env_vars = dotenv_values(".env")

FOLDER_PATH = env_vars["FOLDER_PATH"]
DESTINATION_PATH = env_vars["DESTINATION_PATH"]


def convert_mp4_to_mp3(file_path: str, destination_path: str = None) -> None:
    """
    Converts an MP4 file to MP3 format.

    Parameters:
        file_path (str): The path of the input MP4 file.
        destination_path (str, optional): The path where the converted MP3 file should be saved.
            If not provided, the MP3 file will be saved in the same directory as the input file with a new filename.

    Returns:
        None

    Example:
        # Convert the file "video.mp4" to MP3 format
        convert_mp4_to_mp3("path/to/video.mp4")

    Note:
        - This function uses the `VideoFileClip` class from the moviepy library to extract the audio from the MP4 file.
        - If the `destination_path` parameter is not provided, the MP3 file will be saved in the same directory as the input file.
        - The output file name will be generated based on the current date and time in the format: "YYYY-MM-DD_HH_MM_SS.mp3".
        - The output file path will be created by replacing the file name in the `destination_path` with the generated output file name.
        - The input MP4 file should have compatible audio codecs that can be extracted and saved as an MP3 file.

    Raises:
        OSError: If an error occurs during the conversion process, such as a file not found error or unsupported codec.

    """
    if destination_path is None:
        destination_path = file_path

    video = VideoFileClip(file_path)

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

    output_file_name = current_datetime + ".mp3"
    output_file_path = os.path.join(
        os.path.dirname(destination_path), output_file_name
    ).replace("\\", "/")

    try:
        video.audio.write_audiofile(output_file_path, codec="mp3")
    except OSError as e:
        print(f"An error occurred during MP4 to MP3 conversion: {e}")
        raise
    finally:
        video.close()


def convert_most_recent_mp4() -> None:
    """
    Converts the most recent MP4 recording to MP3 format.

    Returns:
        None

    Example:
        # Convert the most recent MP4 recording to MP3 format
        convert_most_recent_mp4()

    Note:
        - This function retrieves the most recent MP4 recording file using the `get_most_recent_recording` function
          from the "folder_logic" module.
        - If there are no MP4 recordings found, the function will return without performing any conversion.
        - The retrieved MP4 file path is then passed to the `convert_mp4_to_mp3` function for conversion.

    """
    mp4 = get_most_recent_recording(FOLDER_PATH)
    if mp4 is None:
        return
    convert_mp4_to_mp3(mp4, DESTINATION_PATH)


def convert_all_mp4s_for_today() -> None:
    """
    Converts all MP4 recordings for the current day to MP3 format.

    Returns:
        None

    Example:
        # Convert all MP4 recordings for today to MP3 format
        convert_all_mp4s_for_today()

    Note:
        - This function retrieves a list of MP4 recordings for the current day using the `get_all_recordings_for_today`
          function from the "folder_logic" module.
        - The function then iterates over each MP4 file in the list and passes it to the `convert_mp4_to_mp3` function
          for conversion.
        - If there are no MP4 recordings found for the current day, the function will not perform any conversion.

    """
    list_of_mp4s = get_all_recordings_for_today(FOLDER_PATH)
    for mp4 in list_of_mp4s:
        convert_mp4_to_mp3(mp4, DESTINATION_PATH)


def main():
    """
    Entry point function for the program.

    Prompts the user for input to select an option and performs the corresponding action.

    Returns:
        None

    Example:
        # Run the main function
        if __name__ == "__main__":
            main()

    Note:
        - This function serves as the entry point for the program.
        - The user is prompted to select an option by entering '1' for the most recent recording
          or '2' for all recordings today.
        - If an invalid selection is made, the program will display an error message and prompt again.
        - The function then calls the `collapse_sub_folders` function to collapse sub-folders.
        - Based on the user's input, the corresponding conversion function (`convert_most_recent_mp4`
          or `convert_all_mp4s_for_today`) is called from the `menu_logic` dictionary.

    """
    while (
        user_input := input(
            "Press '1' for the most recent recording.\n"
            "Press '2' for all recordings today.\n"
            ">> "
        )
    ) not in {"1", "2"}:
        print("Invalid selection.")

    collapse_sub_folders(FOLDER_PATH)
    menu_logic = {"1": convert_most_recent_mp4, "2": convert_all_mp4s_for_today}
    menu_logic[user_input]()


if __name__ == "__main__":
    main()
