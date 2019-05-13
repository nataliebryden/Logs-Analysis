# Log Analysis Reporting Tool

I have built a reporting tool that will analyse logs from a PostgreSQL database to answer questions about news data. It is a Python3 program that uses the Psycopg2 library to connect to the PostgreSQL database and prints out reports in plain text. I have completed this project as part of Udacity's Full Stack Web Developer Nanodegree.

## Project Context

This task involves building an internal reporting tool that will answer questions about user behaviour, using information from a database behind a news website. The database contains news articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, the reporting tool will answer these three questions about the site's user activity:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Installation
Below are installation instructions and the views I have created in PostgreSQL. You will need to create these views before running the `newsdata.py` file.
Note: my operating system is Mac OS X.  

### Install Virtual Box
VirtualBox is free, open-source software published by Oracle that allows you to run a Virtual Machine (VM) from your device. It can be downloaded from [virtualbox.org](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

### Install vagrant
Vagrant is an open-source software product used to build and maintain a VM, it makes it simple to manage VM environments through the command line. It can be downloaded from [vagrantup.com](https://www.vagrantup.com/downloads.html).

### Download the VM configuration
Download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
It will give you a directory called FSND-Virtual-Machine.

### Download the Data
Download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip the file `newsdata.sql` and move it into into the Vagrant directory.
## Usage

### Start the virtual machine
`cd` into the Vagrant directory on your machine.
Run the following command from your terminal:
```
vagrant up
```
Once `vagrant up` has finished running, run the following command to log in to your Linux Virtual Machine:
```
vagrant ssh
```
### Load the data
To load the data, `cd` into the vagrant directory and use the command `psql -d news -f newsdata.sql`.

### Create Views
Create the below three views in PostgreSQL before running the python script `newsdata.py`.

CountArticles view:
```
create view countArticles as
select r.title, COUNT(tableOne.logslug)
from (select regexp_split_to_array(path, '/') as logslug from log) as tableOne
JOIN articles r
ON r.slug = tableOne.logslug[3]
GROUP BY r.title
ORDER BY COUNT(tableOne.logslug) DESC;
```


countAuthors view:
```
CREATE view countAuthors as
select COUNT(tableOne.logslug), a.name
from articles r
JOIN (select regexp_split_to_array(path, '/') as logslug from log) as tableOne
ON r.slug = tableOne.logslug[3]
JOIN authors a
ON a.id = r.author
GROUP BY a.name
ORDER BY COUNT(tableOne.logslug) DESC;
```


siteErrors view:
```
CREATE view siteErrors as
SELECT okTable.date_trunc::date as date, (notOkTable.notOkCount::float/okTable.okCount::float * 100) as errorPercent
FROM (SELECT DATE_TRUNC('day',time), COUNT(*) okCount FROM log
WHERE status LIKE '200 OK' GROUP BY DATE_TRUNC('day',time),status) okTable
JOIN (SELECT DATE_TRUNC('day',time), COUNT(*) notOkCount FROM log
WHERE status NOT LIKE '200 OK' GROUP BY DATE_TRUNC('day',time),status) notOkTable
ON okTable.DATE_TRUNC = notOkTable.DATE_TRUNC
```

### Run newsdata.py
Download `newsdata.py` from my GitHub repository, and move it into your vagrant directory. You can now run the following code:
```
python newsdata.py
```
The plain text file `output.txt` contains a copy of what my program printed out.
### Exit vagrant
Exit vagrant by running following command:
```
exit
```
