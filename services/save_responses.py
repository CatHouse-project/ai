# services/save_responses.py

import json
import os

def save_user_responses(request):

    # 요청 데이터에서 필요한 정보 추출
    userid = request.userid
    gender = request.gender
    room_capacity = request.room_capacity
    # 질문 응답 추출
    response_data = {f"question_{i}": getattr(request, f"question_{i}") for i in range(1, 25)}

    # FastAPI에서 경로가 올바르게 해석되는지 확인
    print("Info file path:", )

    # 1. information.json 업데이트
    # 현재 파일 위치를 기준으로 data 폴더의 절대 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    info_file_path = os.path.join(base_dir, "../data/information.json")


    # 기존 정보 로드
    if os.path.exists(info_file_path):
        with open(info_file_path, 'r') as f:
            info_data = json.load(f)
    else:
        info_data = []



    # 새로운 사용자 정보 추가
    new_user_info = {
        "user_id": userid,
        "gender": 'M' if gender == 'male' else 'F',
        "room_type": room_capacity
    }
    info_data.append(new_user_info)

    # 정보 저장
    with open(info_file_path, 'w') as f:
        json.dump(info_data, f, indent=4)

    # 2. 응답 데이터 저장
    # 파일명 결정
    gender_prefix = 'male' if gender == 'male' else 'female'
    response_file_name = f"{gender_prefix}_{room_capacity}.json"
    response_file_path = os.path.join(base_dir, f"../data/{response_file_name}")


    # 기존 응답 데이터 로드
    if os.path.exists(response_file_path):
        with open(response_file_path, 'r') as f:
            responses = json.load(f)
    else:
        responses = []

    # 기존 id의 최대값 찾기
    if responses:
        max_id = max(response['id'] for response in responses)
    else:
        max_id = 0

    # 새로운 응답 데이터 생성
    new_response_entry = {
        "id": max_id + 1,
        "user_id": userid
    }
    # 질문 응답 추가
    new_response_entry.update(response_data)

    # 응답 데이터에 추가
    responses.append(new_response_entry)

    # 응답 데이터 저장
    with open(response_file_path, 'w') as f:
        json.dump(responses, f, indent=4)

if __name__ == '__main__':
    requests = {
  "userid": 123582,
  "gender": "male",
  "room_capacity": 2,
  "question_1": 1,
  "question_2": 2,
  "question_3": 1,
  "question_4": 2,
  "question_5": 1,
  "question_6": 2,
  "question_7": 1,
  "question_8": 2,
  "question_9": 1,
  "question_10": 2,
  "question_11": 1,
  "question_12": 2,
  "question_13": 1,
  "question_14": 2,
  "question_15": 1,
  "question_16": 2,
  "question_17": 1,
  "question_18": 2,
  "question_19": 1,
  "question_20": 2,
  "question_21": 1,
  "question_22": 2,
  "question_23": 1,
  "question_24": 2,
  "question_25": 1
}
    save_user_responses(requests)
