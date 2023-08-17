"""This script walks through a folder of PDF files and splits each file into individual pages.
The resulting pages are saved in a separate folder. Any files that cannot be processed
due to errors are saved in a separate error folder.
"""
import os

from pypdf import PdfReader, PdfWriter


def move_file(old, new):
    """
    Move a file from the old path to the new path.

    Args:
        old (str): The old path of the file to be moved.
        new (str): The new path where the file should be moved.

    Raises:
        FileExistsError: If the file already exists in the new path.
        PermissionError: If the user does not have permission to move the file.
        FileNotFoundError: If the file does not exist in the old path.

    Returns:
        None
    """
    print(f"Move file from '{old}' to '{new}'...")
    try:
        os.rename(old, new)
        print("...done!")

    except FileExistsError:
        print("A 'FileExistsError' occoured! Manual action/cleanup needed!")

    except PermissionError:
        print("A 'PermissionError' occoured! Manual action/cleanup needed!")

    except FileNotFoundError:
        print("A 'FileNotFoundErroroccoured! Manual action/cleanup needed!")


def split_pdfs():
    """Main function from this module. It splits pdfs. The filenames are preserved, the outputfiles are numbered."""

    # split pdfs every n pages
    PAGES_PER_PDF = 2

    # set file extension without dot
    PDF_FILE_EXTENSION = "pdf"

    # prepare needed foldernames
    WORK_DIR = os.getcwd()
    INPUT_DIR = os.path.join(WORK_DIR, "data", "input")  # folder with the pdfs to split
    FINISHED_DIR = os.path.join(
        WORK_DIR, "data", "finished"
    )  # folder for the successfully splitted pdfs from INPUT_DIR
    OUPUT_DIR = os.path.join(
        WORK_DIR, "data", "output"
    )  # folder for the output (newly splitted pdfs)
    ERROR_DIR = os.path.join(
        WORK_DIR, "data", "error"
    )  # folder for files with  -> Errors

    print(f"Splitting pdfs every {PAGES_PER_PDF} pages in folder {INPUT_DIR}...")

    # our list of pdfs to split
    PDFS_TO_SPLIT = []

    # walk input folder and add pdfs to list
    # root_dir=root, d=directories=_, files_from_root=files
    for root_dir, _, files_from_root in os.walk(INPUT_DIR):
        for file in files_from_root:
            if file.endswith(f".{PDF_FILE_EXTENSION}"):
                print(file)
                PDFS_TO_SPLIT.append(os.path.join(root_dir, file))

    print(f"Found {len(PDFS_TO_SPLIT)} pdfs to split...")
    print(PDFS_TO_SPLIT)

    for pdf in PDFS_TO_SPLIT:
        reader = PdfReader(pdf)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]

        # show some data of the current pdf
        print(f"Processing {pdf} with pages {number_of_pages} pages...")

        # check if there are at least 2 pages
        if number_of_pages < PAGES_PER_PDF:
            print(
                f" -> Error: Number of pages is less than absolute minimum of {PAGES_PER_PDF} pages: {number_of_pages}"
            )
            move_file(pdf, os.path.join(ERROR_DIR, os.path.basename(pdf)))
            continue

        # check if number of pages is even
        if number_of_pages % PAGES_PER_PDF != 0:
            print(
                f" -> Error: Number of pages is not even (does not fit export): {number_of_pages}"
            )
            move_file(pdf, os.path.join(ERROR_DIR, os.path.basename(pdf)))
            continue

        # set number of export pdfs
        try_num_of_pages_even = number_of_pages / PAGES_PER_PDF
        if not try_num_of_pages_even.is_integer():
            print(
                f" -> Error: Number of pages is not even (does not fit export): {number_of_pages}"
            )
            move_file(pdf, os.path.join(ERROR_DIR, os.path.basename(pdf)))
            continue

        NUM_PDFS_TO_CREATE = int(try_num_of_pages_even)
        print(f" -> Will create {NUM_PDFS_TO_CREATE} pdfs...")

        for i in range(NUM_PDFS_TO_CREATE):
            print(f" ---> Start with file {i+1} of {NUM_PDFS_TO_CREATE}")
            start_page = PAGES_PER_PDF * i
            end_page = start_page + (PAGES_PER_PDF - 1)

            print(f" ----> Export pages  {start_page+1} to {end_page+1}...")
            splitted_pdf = PdfWriter()
            for page in range(start_page, end_page + 1):
                print(f" ------> Adding page {page+1}...")
                splitted_pdf.add_page(reader.pages[page])

            _, old_filename = os.path.split(pdf)
            old_filename = str(old_filename[: -len(PDF_FILE_EXTENSION) - 1])

            splitted_pdf_filename = f"{old_filename}_Part_{i+1}_with_\
Pages_{start_page+1}_to_{end_page+1}.{PDF_FILE_EXTENSION}"
            with open(os.path.join(OUPUT_DIR, splitted_pdf_filename), "wb") as output:
                print(f" --------> Writing file '{splitted_pdf_filename}'...")
                splitted_pdf.write(output)  # type: ignore[arg-type]

        print(f" -> Finished with {pdf}!")
        # finally move the original file to the finished folder
        move_file(pdf, os.path.join(FINISHED_DIR, os.path.basename(pdf)))


if __name__ == "__main__":
    split_pdfs()
