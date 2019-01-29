import zipfile, shutil, os, MySQLdb, datetime
from secrets import corpora # Bad! Fix this later.

class NovayaArticle:

    def __init__(self, file_structure, kp, category, proc_path):
        self.originally_posted = file_structure[0]
        self.pub_date = file_structure[1].split(': ')[1]
        self.author = file_structure[2]
        self.content = file_structure[3:]
        self.kp = kp
        self.category = category
        self.proc_path = proc_path # Path to temporarily stored txt file

def extract_files():
    # extract_files()
    # Extracts content from zip files and moves the zip to storage
    for subdir, dirs, files in os.walk("./dump/new"):
        for file in [f for f in files if f[-4:] == '.zip']:
            path = "{0}/{1}".format(subdir, file)

            # Extract zip
            with zipfile.ZipFile(path, 'r') as zipped_file:
                zipped_file.extractall("./dump/new/{0}".format(file[:-4]))

            # Move zip to storage (old)
            shutil.move(path, "./dump/old/{0}".format(file))

def process_novaya():
    # process_novaya()
    # Processes content from extracted files, stores in db, removes processed files
    article_list = []

    for root, dirs, files in os.walk("./dump/new", topdown=False):
        # Only look in valid directories ( e.g ./dump/new/category)
        if "__" not in root and len(root.split('/')) > 3:
            category = root.split('/')[3]
            for file in [f for f in files if f != '.DS_Store']:
                file_path = '{0}/{1}'.format(root, file)

                # Read file from bottom-up; files not CSV
                file_structure = [line for line in reversed(open(file_path).readlines())]

                # Check for malformed articles
                if len(file_structure) < 3:
                    shutil.move(file_path, "./dump/processing/malformed/{0}".format(file))
                    continue
                else:
                    proc_path = "./dump/processing/{0}".format(file)
                    shutil.move(file_path, proc_path)

                # if we've already processed an article, increment that kp, otherwise generate one
                if article_list:
                    kp = generate_kp(article_list[-1])
                else:
                    kp = generate_kp(None)

                run_article = NovayaArticle(file_structure, kp, category, proc_path)
                article_list.append(run_article)

        # Remove empty or useless directories
        if len(root.split('/')) > 3:
            shutil.rmtree(root) # Note: probably dangerous

    return push_to_corpora(article_list)

def generate_kp(last_article):
    # generate_kp()
    # Creates a new kp from the most recent kp using most recent article
    sql = "SELECT kp FROM novaya_gazeta ORDER BY kp DESC LIMIT 1"

    # If we've already polled corpora -> increment
    if last_article:
        kp = last_article.kp + 1
    # Poll corpora for most recent KP, assign 1 if none found
    else:
        result = perform_sql(sql)
        if result:
            kp = result
        else:
            kp = 1
    return kp

def push_to_corpora(article_list):
    # push_to_corpora()
    # Builds an INSERT statement from list of processed articles, executes

    total_count = 0
    for art in article_list:
        run_sql = "INSERT INTO novaya_gazeta (kp, pub_date, author, original_post, content, category, ret_date) VALUES "

        run_sql = "{0} (%s, %s, %s, %s, %s, %s, %s);".format(run_sql)
        params = [art.kp, art.pub_date, art.author, art.originally_posted, art.content[0], art.category, str(datetime.datetime.now())]
        perform_sql(run_sql, params)
        total_count += 1

        os.remove(art.proc_path) # now safe in db, remove stored txt file
    return "{0} articles succesfully stored!".format(total_count)

def perform_sql(sql, params=None):
    # perform_sql()
    # Performs a SQL query and returns results
    db = MySQLdb.connect(host=corpora['host'], user=corpora['username'], passwd=corpora['password'], db=corpora['database'])
    c = db.cursor()

    c.execute(sql, params)
    results = c.fetchall()

    db.commit()
    c.close()

    return results
