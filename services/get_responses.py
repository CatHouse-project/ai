import json
import os

def get_user_responses(userid):
    # 현재 파일 위치를 기준으로 data 폴더의 절대 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    info_file_path = os.path.join(base_dir, "../data/information.json")

    # information.json 파일에서 gender와 room_capacity 검색
    if not os.path.exists(info_file_path):
        return None  # 정보 파일이 없으면 None 반환

    with open(info_file_path, 'r') as f:
        info_data = json.load(f)

    # userid에 해당하는 사용자 정보 검색
    user_info = next((user for user in info_data if user["user_id"] == userid), None)
    if not user_info:
        return None  # 해당 userid가 정보 파일에 없으면 None 반환

    # gender와 room_capacity 정보를 가져옴
    gender = 'male' if user_info["gender"] == 'M' else 'female'
    room_capacity = user_info["room_type"]

    # 응답 데이터 파일명 결정
    response_file_name = f"{gender}_{room_capacity}.json"
    response_file_path = os.path.join(base_dir, f"../data/{response_file_name}")

    # 응답 데이터 파일이 없으면 None 반환
    if not os.path.exists(response_file_path):
        return None

    # 응답 데이터 파일에서 해당 userid의 응답을 검색
    with open(response_file_path, 'r') as f:
        responses = json.load(f)

    # userid와 일치하는 응답 데이터 찾기
    for response in responses:
        if response["user_id"] == userid:
            # 질문 응답 데이터 반환
            return {
                "userid": response["user_id"],
                **{f"question_{i}": response[f"question_{i}"] for i in range(1, 25)}
            }

    # userid에 해당하는 응답이 없으면 None 반환
    return None

if __name__ == "__main__":
    get_user_responses(406825)