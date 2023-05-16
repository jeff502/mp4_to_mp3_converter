import os
import shutil
from datetime import datetime, date
from typing import List


def collapse_sub_folders(path: str) -> None:
    """
    Recursively collapses subfolders and moves all items to the parent folder.

    Parameters:
        path (str): The path of the folder to collapse.

    Returns:
        None

    Raises:
        OSError: If an error occurs while moving or removing files or directories.

    Note:
        - This function collapses subfolders within the specified path and moves all items to the parent folder.
        - Empty subfolders are removed after moving their contents to the parent folder.
        - The function performs potentially destructive operations, so use with caution and ensure you have a backup of your data.

    Example:
        # Provide the path of the folder to collapse subfolders
        folder_path = '/path/to/folder'
        collapse_sub_folders(folder_path)
    """
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            if os.path.isdir(item_path):
                collapse_sub_folders(item_path)

                for sub_item in os.listdir(item_path):
                    sub_item_path = os.path.join(item_path, sub_item)
                    new_item_path = os.path.join(path, sub_item)
                    shutil.move(sub_item_path, new_item_path)

                os.rmdir(item_path)
    except OSError as e:
        print(f"An error occurred while collapsing subfolders: {e}")
        raise


def get_most_recent_recording(path: str) -> str | None:
    """
    Retrieves the most recent recording file in the specified path.

    Parameters:
        path (str): The path of the folder containing the recording files.

    Returns:
        str or None: The path to the most recent recording file, or None if no recording files are found.

    Note:
        - This function searches for recording files (files with the '.mp4' extension) within the specified path.
        - If no recording files are found, the function returns None.
        - The most recent recording file is determined based on its modification timestamp.
        - If multiple recording files have the same modification timestamp, the function returns the first
        encountered in the list.
        - The function assumes that the 'os' module is imported.

    Example:
        # Provide the path of the folder containing the recordings
        folder_path = '/path/to/recordings'
        most_recent_recording = get_most_recent_recording(folder_path)

        if most_recent_recording:
            print("Most recent recording:", most_recent_recording)
        else:
            print("No recordings found in the folder.")
    """
    files = os.listdir(path)
    files = [f for f in files if f.endswith(".mp4")]

    if not files:
        return

    most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(path, f)))
    return os.path.join(path, most_recent_file)


def get_all_recordings_for_today(path: str) -> List[str] | None:
    """
    Retrieves the all mp4 files in the specified path that occurred today.

    Parameters:
        path (str): The path of the folder containing the recording files.

    Returns:
        list[str] or []: The path to the most recent recording file, or None if no recording files are found.

    Note:
        - This function searches for recording files (files with the '.mp4' extension) within the specified path.
        - If no recording files are found, the function returns an empty list.
        - Recording files are determined based on their modification timestamp.
        - If multiple recording files have the same modification timestamp, the function returns all.
        - The function assumes that the 'os' module is imported.

    Example:
        # Provide the path of the folder containing the recordings
        folder_path = '/path/to/recordings'
        recordings_for_today = get_all_recordings_for_today(folder_path)

        if recordings_for_today:
            for file in recordings_for_today:
                print(file)
        else:
            print("No recordings found in the folder for today.")
    """
    files = os.listdir(path)
    files = [
        os.path.join(path, f)
        for f in files
        if f.endswith(".mp4") and file_was_created_today(os.path.join(path, f))
    ]
    return files


def file_was_created_today(mp4: str) -> bool | None:
    """
    Checks if the specified MP4 file was created today.

    Parameters:
        mp4 (str): The path of the MP4 file to check.

    Returns:
        bool: True if the file was created today, None otherwise.

    Example:
        # Check if the file "video.mp4" was created today
        is_today = file_was_created_today("path/to/video.mp4")

    Raises:
        FileNotFoundError: If the specified file does not exist.

    Note:
        - This function determines if the MP4 file was created on the same day as the current date.
        - The function uses the modification timestamp of the file to make the determination.
        - The file path should be provided as a string.
    """
    try:
        mp4_time_stamp = os.path.getmtime(os.path.join(mp4))
        current_date = date.today()
        timestamp_datetime = datetime.utcfromtimestamp(mp4_time_stamp)
        timestamp_date = timestamp_datetime.date()
        if timestamp_date == current_date:
            return True
    except FileNotFoundError:
        print(f"File: {mp4} was not found.")
        raise
