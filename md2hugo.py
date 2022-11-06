import os
import sys
import os.path
import re

if (len(sys.argv)!=3):
    print("\nmd2hugo.py - Exports markdown files in wp2md format into a hugo file structure and format.\n\nExample : python md2hugo.py c:\\my\\md2wp\\files\\2022 ../../blog/site/content/posts\n")
    sys.exit(0)

input_path = sys.argv[1]
output_path = sys.argv[2]

if not os.path.isdir(input_path):
    print("The input path (" + input_path +") does not exist")
    sys.exit(0)

if not os.path.isdir(output_path):
    print("The output path (" + output_path +") does not exist")
    sys.exit(0)

for subdir, dirs, files in os.walk(input_path):
    for file in files:
        if '.md' in file and 'readme.md' not in file:
                    
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
            # also make it YAML safe (remove colons)
            output_text = ("---\ntitle: " + post_title.replace(":"," ") + "\ndate: " + post_date + "\n---\n\n") + "".join(input_text[4:])
                
            # work out the final filename
            output_filename = file.strip() # grab the filename and strip any spaces from the ends
            output_filename = re.sub(r"\s+","-", output_filename) # replace any spaces with a hyphen
            output_filename = re.sub(r"\-+","-", output_filename) # replace multiple hyphens with single hyphens
            output_file_path = os.path.join(output_path,output_filename.lower()) # create the final path

            # write the file
            print("> " + output_file_path)
            output_file = open(output_file_path, 'wb')
            output_file.write(bytes(output_text,'utf-8'))
            output_file.close()
