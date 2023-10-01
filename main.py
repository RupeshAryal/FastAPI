from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body

from pydantic import BaseModel, ConfigDict

app = FastAPI()


class Post(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: int
    title: str
    content: str


post = [{'id': 1, 'title': 'title of post1', 'content': 'content of content1'},
        {'id': 2, 'title': 'title of post2', 'content': 'content of post2'}]


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get('/posts')
def get_posts():
    return {"data": post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    new_data = {'id': new_post.id, 'title': new_post.title, 'content': new_post.content}
    post.append(new_data)

    return {"Message": "Data successfully posted to the array "}


def find_post(id):
    for p in post:
        if p['id'] == id:
            return p


@app.get("/posts/{id}")
def get_post(id: int):
    p = find_post(id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return {"post detail": p}


# title: str, content: str, category: str, Published or Draft: Bool

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = get_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="error: the post does not exist")

    post.pop(index['id'])

    return {"message": "post was successfully deleted"}


def get_index(id):
    for p in post:
        if p['id'] == id:
            return p


@app.put("posts/id")
def update_post(id: int, post: Post):
    print(post)
    index = get_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="error: the post does not exist")

    post_dict = post.model_dump()
    post_dict['id'] = id


    return {"message": "updated post"}
