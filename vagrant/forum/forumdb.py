# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

#POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  conn = psycopg2.connect("dbname=forum")
  cur = conn.cursor()
  cur.execute("select content, time from posts order by time desc")
  entries = cur.fetchall()
  cur.close()
  conn.close()
  return entries

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  conn = psycopg2.connect("dbname=forum")
  cur = conn.cursor()
  cur.execute("insert into posts (content) VALUES (%s)", 
    (bleach.clean(content),))
  conn.commit()
  cur.close()
  conn.close()