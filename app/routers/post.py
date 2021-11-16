import optional as optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=List[schemas.PostResponce])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
             skip: int = 0, search: Optional[str] = ""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


"""
def get_posts():

    curser.execute
SELECT * FROM
posts
)
    posts = curser.fetchall()

    return "ser"
"""


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(
        **post.dict(), owner_id=current_user.id  # unpacking a dictionary
    )
    print(current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # actlike returning
    return new_post


@router.get("/{id}", response_model=schemas.PostResponce)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not Found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access Denied")

    return post


"""
def get_post(id: int):  # , responce: Response):  # telling fast api that wee need a intiger
    # post = find_post(id)

    if not post:
        responce.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id {id} not found"}

    # achiving above goal using HTTP excepyions

    # curser.execute("SELECT * FROM posts WHERE id = %s "", (str(id),))
    post = curser.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return {"post_details": post}
"""


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # rsponce = db.query(models.Post).filter(models.Post.id == id).delete().first()
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found in server")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    curser.execute("" delete from posts where id = %s returning *"", (str(id),))
    deleted_post = curser.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return deleted_post
   """


@router.put("/{id}", response_model=schemas.UpdateResponce)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    query_data = query.first()

    if query_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")

    elif query_data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perfimr requested action")

    response = query.update(post.dict(), synchronize_session=False)
    db.commit()
    test = query.first()
    return test


"""
def create_post(id: int, post: Post):

    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    curser.execute(
        ""Update posts set title = %s, content = %s, published = %s, updated_at = now() where id = %s returning * "",
        (post.title, post.content, post.published, str(id)))
    response = curser.fetchone()
    conn.commit()

    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {id} not found on server")
    # curser.commit()
    return {"data": response}
"""
