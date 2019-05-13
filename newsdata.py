#!/usr/bin/python3

import psycopg2
DBNAME = "news"


# Question one answer in one query
def get_articles():
    """ Get top three most popular articles from database."""
    conn = psycopg2.connect(dbname=DBNAME)
    cur = conn.cursor()
    cur.execute("select * from countArticles LIMIT 3;")
    for result in cur:
        print('{} -- {} views'.format(result[0], result[1]))
    conn.close()


# Question 2 with a view
def get_authors():
    """ Get top three most popular authors from database."""
    conn = psycopg2.connect(dbname=DBNAME)
    cur = conn.cursor()
    cur.execute("select * from countAuthors limit 3;")
    for result in cur:
        print('{} -- {} views'.format(result[0], result[1]))
    conn.close()



# Question 3 with a view
def get_percentage():
    """ Get the log error results greater than one percent."""
    conn = psycopg2.connect(dbname=DBNAME)
    cur = conn.cursor()
    cur.execute("select * from siteErrors where errorPercent > 1;")
    for result in cur:
        print('{} -- {}% errors'.format(result[0], result[1]))
    conn.close()

def main():
    print('The most popular three articles of all time:')
    get_articles()
    print('')
    print('The most popular three authors of all time:')
    get_authors()
    print('')
    print('The days where more than 1% of requests led to errors:')
    get_percentage()

if __name__ == '__main__':
    main()
