# novaya_proc
ETL script to load scraped content from the Novaya Gazeta into a database. Information is loaded onto the dev server via
zip files, then extracted, moved, scraped, inserted into the novaya_gazeta table, and then deleted. 

## Usage

Place zip files, or unzipped text files within a folder with the category's name, inside `novaya/dump/new` and run command `python /path/to/novaya_proc.py`. Messages will appear keeping you updated as to the status of the operation. Once the extraction and insertion is done, the script will terminate, the zip file will be moved to `novaya/dump/old` and all extracted files will be deleted. 

Check for malformed files in `novaya/dump/processing/malformed` and report any errors. 

## Structure

The file structure looks like this:
```
                novaya
                  |
novaya_proc.py - dump - novaya.py
                  |
           new - old - processing
                           |
                       malformed
```
Zip files containing new articles are loaded into `novaya/dump/new`. Once novaya_proc.py is run, articles are extracted from
their zips into the same directory. The zip files are moved to `dump/old` for storage. The extracted articles are then parsed
and loaded into novaya/dump/processing, then deleted upon confirmation of final insertion into the database. 

Articles that do not match the format or otherwise cause error are loaded into `novaya/dump/processing/malformed`.

## Schema

The schema of novaya_gazeta looks like this:
```
+---------------+------------+------+-----+---------+-------+
| Field         | Type       | Null | Key | Default | Extra |
+---------------+------------+------+-----+---------+-------+
| kp            | int(11)    | NO   | PRI | NULL    |       |
| pub_date      | datetime   | YES  |     | NULL    |       |
| author        | text       | YES  |     | NULL    |       |
| original_post | text       | YES  |     | NULL    |       |
| content       | mediumtext | YES  |     | NULL    |       |
| category      | text       | YES  |     | NULL    |       |
| ret_date      | datetime   | YES  |     | NULL    |       |
+---------------+------------+------+-----+---------+-------+
```
**Explanation:**
* KP: The primary key linked to an article, unique and incrementing.
* pub_date: Date the article was published.
* author: The listed author from the article, in Russian. When there is no author, a message is specified in Russian.
* original_post: An explanation in Russian of when and where the article was originally published.
* content: The content of the article.
* category: The category of news the article came from.
* ret_date: When the article was retrieved from its zip and loaded into the database. 
