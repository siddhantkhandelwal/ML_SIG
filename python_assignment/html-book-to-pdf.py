import pdfkit
import validators
import sys

print("Enter Option:")
print("1. From HTML file")
print("2. From Website URL")
choice = int(input())

if choice == 1:
    inputpath = input("Enter path of HTML File: ")
    outputpath = input("Enter path for Output PDF File (Leave Blank for default): ")
    if outputpath == '':
        outputpath = "output.pdf"
    pdfkit.from_file(inputpath, outputpath)

elif choice == 2:
    inputpath = input("Enter Website URL: ")
    if not validators.url(inputpath):
        print("Invalid URl. Aborting....")
        sys.exit()
    outputpath = input("Enter path for Output PDF File (Leave Blank for default): ")
    if outputpath == '':
        outputpath = "output.pdf"
    pdfkit.from_url(inputpath, outputpath)