from fastapi import FastAPI, HTTPException, status

from pydantic import BaseModel, ConfigDict

import mysql.connector
import time
import datetime

# connecting to the mysql database, the api won't run until everything is set up.
while True:
    try:
        my_conn = mysql.connector.connect(host='localhost',
                                          database='office',
                                          user='root',
                                          password='root')

        my_cursor = my_conn.cursor()
        print('Connecting to the database...')
        print("You are connected to the office database successfully !!")
        break

    except Exception as e:
        print("Error", e)
        time.sleep(4)

app = FastAPI()


class Post(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str
    content: str
    published: bool = 0


post = [{'id': 1, 'title': 'title of post1', 'content': 'content of content1'},
        {'id': 2, 'title': 'title of post2', 'content': 'content of post2'}]


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get('/posts')
def get_posts():
    query = ("SELECT * FROM posts")
    my_cursor.execute(query)
    data = my_cursor.fetchall()

    json_format = []
    for p in data:
        temp = {'id': p[0],
                'title': p[1],
                'content': p[2],
                'published': p[3],
                'created_at': p[4]
                }
        json_format.append(temp)

    return {"data": json_format}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    new_data = (new_post.title, new_post.content, new_post.published)

    add_post = ("INSERT INTO posts "
                "(title, content, published) "
                "VALUES (%s, %s, %s)")

    my_cursor.execute(add_post, new_data)
    my_conn.commit()

    return {"Message": "Data successfully posted to the array "}


@app.get("/posts/{id}")
def get_post(id: int):
    query = "SELECT * FROM posts WHERE id = %s;"
    my_cursor.execute(query, (id,))
    data = my_cursor.fetchone()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    post_ = {
        'id': data[0],
        'title': data[1],
        'content': data[2],
        'published': data[3],
        'created_at': data[4]
    }

    return {"post_detail": post_}


# title: str, content: str, category: str, Published or Draft: Bool

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    query = ("DELETE FROM posts WHERE id = %s")

    my_cursor.execute(query, (id,))
    my_conn.commit()

    query = ("SELECT * FROM posts WHERE id = %s")

    my_cursor.execute(query, (id,))
    data = my_cursor.fetchone()

    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="error: the post does not exist")

    return {"message": "post was successfully deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    query = ("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s")
    my_cursor.execute(query, (post.title, post.content, post.published, id))

    query = ("SELECT * FROM posts WHERE id = %s")

    my_cursor.execute(query, (id,))
    data = my_cursor.fetchone()
    my_conn.commit()

    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="error: the post does not exist")

    return {"message": "updated post"}
