# WORK IN PROGRESS
# It doesn't work yet, so don't take much notice of it :)

import os
import sys
import os.path
import re

if (len(sys.argv)!=3):
    print("\nmd2hugo_archive.py - Exports markdown files in wp2md format into a hugo file structure and format.\n\nExample : python md2hugo.py c:\\my\\md2wp\\files\\2022 ../../blog/site/content/posts\n")
    sys.exit(0)

input_path = sys.argv[1]
output_path = sys.argv[2]

if not os.path.isdir(input_path):
    print("The input path (" + input_path +") does not exist")
    sys.exit(0)

if not os.path.isdir(output_path):
    print("The output path (" + output_path +") does not exist")
    sys.exit(0)

# prepare a dictionary 
years = {}

for subdir, dirs, files in os.walk(input_path):
    for file in files:
        if '.md' in file and 'readme.md' not in file:
        
            print("Processing " + file)
            
            # read the source file
            input_file_path = os.path.join(subdir, file)
            input_file = open(input_file_path,'r',encoding="latin-1")
            input_text = input_file.readlines()
            input_file.close()

            # get the title
            post_title = "".join(input_text[0:1])[2:-1]

            # get the date (the first 10 chars of the filename)
            post_date = file[0:10]
            post_year = post_date[0:4]
            post_month = post_date[5:7]

            # get the body and trim the first 4 lines (contains the title)
            output_text = ("## " + post_title.replace(":"," ") + "\n\n### " + post_date + "\n\n") + "".join(input_text[4:]) + "\n\n---\n\n"
            
            # create a year folder
            year_path = os.path.join(output_path,post_year)
            if not os.path.exists(year_path):
                print("Creating Parent Path for " + post_year)
                os.makedirs(year_path)
            
            # create a month folder within the year folder
            month_path = os.path.join(output_path,post_year,post_year + "-" + post_month)
            if not os.path.exists(month_path):
                print("Creating Child Path for " + post_year + "-" + post_month)
                os.makedirs(month_path)
            
            if post_year not in years:
                years[post_year] = "---\ntitle: " + post_year + "\n---\n\n"

            years[post_year] += output_text
            
print(len(years))

for year in years:
    if years[year]:

        # work out the year filename
        output_file_path = os.path.join(output_path,year + ".md")
        
        print("Creating " + output_file_path)
        output_file = open(output_file_path, 'wb')
        output_file.write(bytes(output_text,'utf-8'))
        output_file.close()


# write the archive file
output_file_path = os.path.join(output_path,year + ".md")

print("Creating " + output_file_path)
#output_file = open(output_file_path, 'wb')
#output_file.write(bytes(output_text,'utf-8'))
#output_file.close()
