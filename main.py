from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, validator
from typing import List, Literal, Dict
from fastapi.responses import JSONResponse

# FastAPI 앱 초기화
app = FastAPI()

# 정보저장 입력양식
class SaveResponsesRequest(BaseModel):
    userid: int
    gender: Literal['male', 'female']
    room_capacity: Literal[2, 3, 4]
    question_1: int
    question_2: int
    question_3: int
    question_4: int
    question_5: int
    question_6: int
    question_7: int
    question_8: int
    question_9: int
    question_10: int
    question_11: int
    question_12: int
    question_13: int
    question_14: int
    question_15: int
    question_16: int
    question_17: int
    question_18: int
    question_19: int
    question_20: int
    question_21: int
    question_22: int
    question_23: int
    question_24: int

# 정보저장 출력양식
class SaveResponsesSuccess(BaseModel):
    status: Literal['success']
    message: str

# 유저 질의 출력양식
class RetrieveResponsesResponse(BaseModel):
    userid: int
    question_1: int
    question_2: int
    question_3: int
    question_4: int
    question_5: int
    question_6: int
    question_7: int
    question_8: int
    question_9: int
    question_10: int
    question_11: int
    question_12: int
    question_13: int
    question_14: int
    question_15: int
    question_16: int
    question_17: int
    question_18: int
    question_19: int
    question_20: int
    question_21: int
    question_22: int
    question_23: int
    question_24: int
# 매칭 출력방식
class RoommateMatchingResponse(BaseModel):
    user_list: Dict[int, float]

class ErrorResponse(BaseModel):
    status: Literal['error']
    message: str
    error_code: str

# 에러 응답을 포맷팅하기 위한 커스텀 예외 처리기
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "error_code": str(exc.status_code),
        },
    )

# 유저 응답을 저장하는 엔드포인트
@app.post("/save_responses", response_model=SaveResponsesSuccess, responses={400: {"model": ErrorResponse}})
async def save_responses(request: SaveResponsesRequest):
    try:
        # 유저 응답을 저장하는 함수가 있다고 가정
        from services.save_responses import save_user_responses
        save_user_responses(request)
        return SaveResponsesSuccess(
            status="success",
            message="응답이 성공적으로 저장되었습니다.",
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="입력이 유효하지 않습니다. 응답 형식을 확인해주세요.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="서버 내부 오류입니다.")

# 유저 응답을 불러오는 엔드포인트
@app.get("/get_responses", response_model=RetrieveResponsesResponse, responses={400: {"model": ErrorResponse}})
async def get_responses(userid: int = Query(...)):
    try:
        # 유저 응답을 가져오는 함수가 있다고 가정
        from services.get_responses import get_user_responses
        response_data = get_user_responses(userid)
        if response_data is None:
            raise HTTPException(status_code=400, detail="입력한 userid를 확인해주세요.")
        return RetrieveResponsesResponse(**response_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="서버 내부 오류입니다.")

# 룸메이트 매칭 엔드포인트
@app.get("/roommate_matching", response_model=RoommateMatchingResponse, responses={400: {"model": ErrorResponse}})
async def roommate_matching(userid: int = Query(...), core_questions: List[int] = Query(...)):
    try:
        # core_questions가 비어 있지 않은지 확인
        if not core_questions:
            raise HTTPException(status_code=400, detail="core_questions를 확인해주세요.")

        # 룸메이트 매칭을 수행하는 함수가 있다고 가정
        from services.roommate_matching import roommate_matching_function
        user_list = roommate_matching_function(userid, core_questions)
        if not user_list:
            raise HTTPException(status_code=400, detail="입력한 userid를 확인해주세요.")
        return RoommateMatchingResponse(user_list=user_list)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="입력한 userid를 확인해주세요.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="서버 내부 오류입니다.")

# 참고: save_user_responses, get_user_responses, roommate_matching_function의 실제 구현은 각각의 모듈(파일)에 위치해야 하며,
# 각 엔드포인트 함수의 시작 부분에서 임포트됩니다.
