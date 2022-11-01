import os
import sys
import os.path

if (len(sys.argv)!=3):
    print("\nmd2hugo.py - Exports markdown files in wp2md format into a hugo file structure and format.\n\nExample : python md2hugo.py c:\\my\\md2wp\\files\\2022 ../../blog/site/content/posts")
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
        if '.md' in file and 'README.md' not in file:
        
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

            # get the body trim the first 4 lines (contain the title)
            output_text = ("---\ntitle: " + post_title + "\ndate: " + post_date + "\n---\n") + "".join(input_text[4:])
            
            output_file_path = os.path.join(output_path,file.replace(" ","_").lower())
            output_file = open(output_file_path, 'wb')
            output_file.write(bytes(output_text,'utf-8'))
            output_file.close()
