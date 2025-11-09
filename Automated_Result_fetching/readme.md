# Automated Student Results PDF Downloader

This Python script automates the process of fetching and saving student exam results as PDF files from the [MGU Result Portal](https://dsdc.mgu.ac.in/exQpMgmt/index.php/public/ResultView_ctrl/index).

---

## Features

- Automatically selects the specified exam from the dropdown.
- Enters each student's PRN number.
- Submits the form to retrieve the result.
- Saves the result page as a PDF file.
- Loops through a range of PRN numbers.
- Saves PDFs in a designated folder.

---

## Prerequisites

- Python 3.x
- Google Chrome browser installed
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed and accessible in your system PATH (must match your Chrome version)
- Python packages:
  - `selenium`

Install Selenium via pip:

```
pip install selenium
```
## Usage

1. Clone or download this repository.

2. Modify the script as needed:
   - Update the `prn_list` variable with your list or range of PRNs.
   - Verify the exact exam option text in `semester_option`.
   - Ensure the element IDs (`exam_id`, `prn`, `btnresult`) match the webpage.

3. Run the script:

   ```
   python app1.py
   ```
4. PDF files will be saved in the `results_pdfs` folder.


## Notes

- This script **must be run locally**, not in cloud environments like Google Colab, due to browser and file system access requirements.
- Make sure no Chrome instances with the same user data directory are running to avoid session conflicts.
- The script runs Chrome in headless mode and uses Chrome's built-in "Print to PDF" functionality.
- Adjust `time.sleep()` delays if the site loads slowly or network is unstable.

## Troubleshooting

- **SessionNotCreatedException**: Close other Chrome instances or try adding a unique `--user-data-dir` argument in Chrome options.
- **Element not found errors**: Inspect the website and update element selectors accordingly.
- For help with ChromeDriver installation and matching versions, refer to the [official documentation](https://sites.google.com/chromium.org/driver/).
