import os
import logging
from datetime import datetime, timedelta

# Get the directory path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, 'log_files', 'logfile.log')

def initialize_logger(log_file_path):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Add a console handler to log to terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger, console_handler

logger, console_handler = initialize_logger(log_file_path)

# Create a separate logger for terminal-only messages
terminal_only_logger = logging.getLogger('terminal_only_logger')
terminal_only_logger.setLevel(logging.INFO)  # Set the desired log level
terminal_only_logger.addHandler(console_handler)

def remove_blank_lines(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through each line in the file
    for i, line in enumerate(lines):
        # Check if the line is blank
        if not line.strip():
            # If it's blank, remove it from the list
            lines[i] = None
        else:
            # If it's not blank, stop iterating
            break

    # Remove all the None elements from the list
    lines = [line for line in lines if line is not None]

    # Write the non-blank lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def cleanup_old_logs(logger, log_file_path=None, days_to_keep=7):
    """
    Removes log entries older than a specified number of days from a log file.

    Args:
        logger: The logger instance.
        log_file_path (str, optional): The path to the log file. Defaults to 'log_files/logfile.log' if not provided.
        days_to_keep (int): The number of days to keep log entries for. Defaults to 7.
    """
    # Log the start of the cleanup process
    logger.info("Starting log cleanup process.")

    # Set default log file path if not provided
    if log_file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(current_dir, 'log_files', 'logfile.log')

    # Remove existing handlers from the logger
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Calculate the cutoff date
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)

    # Create a temporary file to write filtered lines
    temp_file_path = log_file_path + ".tmp"

    with open(log_file_path, 'r') as input_file, open(temp_file_path, 'w') as output_file:
        # Flag to track if the first line is encountered
        first_line = True
        
        # Iterate through each line in the input log file
        for line in input_file:
            # Skip writing blank lines at the beginning of the file
            if first_line and line.strip() == '':
                continue
            
            # Update the flag after processing the first line
            first_line = False

            # Extract the date from the line (assuming the date format is consistent)
            date_str = line.split(' - ')[0]
            try:
                log_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S,%f')
            except ValueError:
                # If unable to parse the date, keep the line as is (including blank lines)
                log_date = None

            # Check if the date is None or less than the cutoff date
            if log_date is None or log_date >= cutoff_date:
                # Write the line to the temporary file (keeping lines with dates within the specified days)
                output_file.write(line)

    remove_blank_lines(temp_file_path)
    # Replace the original log file with the temporary file
    try:
        os.replace(temp_file_path, log_file_path)
    except PermissionError:
        with open(temp_file_path, 'r') as input_file, open(log_file_path, 'w') as output_file:
            for line in input_file:
                output_file.write(line)
        os.remove(temp_file_path)

    # Reinitialize the logger (after removing existing handlers)
    logger, console_handler = initialize_logger(log_file_path)

    return logger