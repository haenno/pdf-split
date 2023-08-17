"""This script walks through a folder of PDF files and splits each file into individual pages.
The resulting pages are saved in a separate folder. Any files that cannot be processed
due to errors are saved in a separate error folder.
"""
import os

from pypdf import PdfReader


def split_pdfs():
    """Main function from this module. It splits pdfs."""

    # prepare needed foldernames
    WORK_DIR = os.getcwd()
    INPUT_DIR = os.path.join(WORK_DIR, "data", "input")  # folder with the pdfs to split
    FINISHED_DIR = os.path.join(
        WORK_DIR, "data", "finished"
    )  # folder for the splitted pdfs
    ERROR_DIR = os.path.join(WORK_DIR, "data", "error")  # folder for files with errors

    # our list of pdfs to split
    PDFS_TO_SPLIT = []

    # walk input folder and add pdfs to list
    # root_dir=root, d=directories=_, files_from_root=files
    for root_dir, _, files_from_root in os.walk(INPUT_DIR):
        for file in files_from_root:
            if file.endswith(".pdf"):
                print(file)
                PDFS_TO_SPLIT.append(os.path.join(root_dir, file))

    for pdf in PDFS_TO_SPLIT:
        reader = PdfReader(pdf)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()
        print(f"Number of pages: {number_of_pages}")
        print(f"Text: '{text}'")
        input("Press Enter to continue...")


if __name__ == "__main__":
    split_pdfs()
