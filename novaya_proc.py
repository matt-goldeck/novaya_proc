from novaya import extract_files, process_novaya

# INSTRUCTIONS:
# 1) Use .zip of file structure following format -> 'category/(.../.../...)/12345.txt'
# -- where 12345.txt is a txt file with at least 3 lines, such that the last two are the author
# -- and the originally published date.
# 2) Run 'sudo python novaya_proc.py' and wait for process to complete.
# 3) Check to make sure dump/new and processing are empty, and that there are no malformed articles
# 4) Report any errors!

if __name__ == '__main__':
    print("Extracting files...")
    try:
        extract_files()
        print("Completed extraction!")
    except Exception as e:
        print "Failed extraction!"
        print e

    print("Processing files...")
    try:
        result = process_novaya()
        print result
    except Exception as e:
        print "Failed processing!"
        print e

    print("Finished processing Novaya Gazeta articles!")
