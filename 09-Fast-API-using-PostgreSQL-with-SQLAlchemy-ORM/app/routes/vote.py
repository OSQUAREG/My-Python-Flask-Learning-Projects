from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database

# Using FastAPI Router with a prefix and tags (to group the routes)
router = APIRouter(prefix="/vote", tags=["Vote"])  # used instead of importing app from main.py


# Vote Operation Logic for a user is adding or removing a vote to a certain post.
"""
After, checking if the post exist, then do below checks and actions:
1) When user tries to ADD a vote to certain post:
    a) Query to check if vote exist already (that is; user_id and post_id combination exist in the Vote model).
    b) if it does not exist, then vote will be added and committed to votes table.
    c) if it exists, vote is not added, then returns user already added a vote.
2) When user tries to REMOVE a vote from certain post:
    a) Query to check if vote exist already (that is; user_id and post_id combination exist in the Vote model).
    b) if it does not exist, return vote not found
    c) if it exist, then delete the vote, removing the record from the votes table.
"""


@router.post("/", status_code=status.HTTP_201_CREATED)
def voting(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):

    # Check if post exist
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

    # Check if vote exist
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_exist = vote_query.first()

    if vote.dir == 1:  # if user is trying to add a vote and...
        if vote_exist is None:  # if user has not added vote to the post before.

            # sets the current user as the author and use **vote.dict() to unpack the new vote data as a dict into the Vote model like this...
            new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)

            db.add(new_vote)
            db.commit()

            return {"message": f"User: {current_user.id} added vote to post: {vote.post_id} successfully."}

        else:  # if user already added a vote to the post before.
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User: {current_user.id} already added a vote to post: {vote.post_id}.")

    else:  # if user is removing a vote from a post

        if vote_exist is None:  # if user has not added vote to the post before.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist.")

        else:  # if user already added a vote to the post before.
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": f"Vote on post: {vote.post_id} by user: {current_user.id} removed successfully."}
