from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from model.siamese_net import find_similar_users

app = FastAPI()


# Request body model
class SimilarityRequest(BaseModel):
    user_id: int
    core_questions: List[int]
    core_weight: float
    num_results: int


@app.post("/find_similar_users/")
def get_similar_users(request: SimilarityRequest):
    # Call find_similar_users function from siamese_net
    similar_user_ids = find_similar_users(
        request.user_id,
        request.core_questions,
        request.core_weight,
        request.num_results
    )

    # Check if similar users were found
    if not similar_user_ids:
        raise HTTPException(status_code=404, detail="User not found or no similar users available")

    return {"similar_user_ids": similar_user_ids}
