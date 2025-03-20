# Python File Organizer

A modern GUI application to organize files based on various criteria such as file type, date, or size.

## Features

- Modern and user-friendly interface
- Organize files by:
  - File type (extension)
  - Date (creation/modification date)
  - Size (small, medium, large)
- Preview organization before execution
- Progress tracking
- Threaded operation to keep UI responsive

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python file_organizer.py
```

2. Select the source directory containing the files you want to organize
3. Select the destination directory where organized files will be moved
4. Choose how you want to organize the files (by type, date, or size)
5. Click "Preview Organization" to see how files will be organized
6. Click "Start Organization" to begin the process

## Organization Methods

### By File Type
Files are organized into folders based on their extensions (e.g., .pdf files go into a "pdf" folder)

### By Date
Files are organized into folders based on their modification date (format: YYYY-MM)

### By Size
Files are organized into three categories:
- small: < 1MB
- medium: 1MB - 10MB
- large: > 10MB

## Safety Features

- Preview before execution
- Progress tracking
- Error handling
- Threaded operation to prevent UI freezing
- Confirmation dialogs for important actions

## Requirements

- Python 3.6 or higher
- ttkthemes
- Pillow 