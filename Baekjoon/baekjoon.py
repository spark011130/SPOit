import json
import os
import requests
import pickle

def get_profile(user_id) -> dict: 
    url = f"https://solved.ac/api/v3/user/show?handle={user_id}"
    r_profile = requests.get(url)
    if r_profile.status_code == requests.codes.ok:
        profile = json.loads(r_profile.content.decode('utf-8'))
        profile = \
        {
        "tier" : profile.get("tier"),
        "rank" : profile.get("rank"),
        "solvedCount" : profile.get("solvedCount"),
        "rating" : profile.get("rating"),
        }
    else:
        print("프로필 요청 실패")
    return profile

def get_solved(user_id) -> [int, dict]:
    url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=level&direction=desc"
    r_solved = requests.get(url)
    if r_solved.status_code == requests.codes.ok:
        solved = json.loads(r_solved.content.decode('utf-8'))
        
        count = solved.get("count")

        items = solved.get("items")
        solved_problems = []
        for item in items:
            solved_problems.append(
                {
                    'problemId': item.get("problemId"),
                    'titleKo': item.get("titleKo"),
                    'level': item.get("level"),
                }
            )
    else:
        print("푼 문제들 요청 실패")
    return count, solved_problems


user_ids = ["spark_1130", "slkimslkim", "chlgkstmd"]
for user_id in user_ids:
    print('\n')
    profile_dict = get_profile(user_id)
    print(f"========{user_id}님의 프로필========")
    print(profile_dict)
    count, solved_list = get_solved(user_id)


    if os.path.isfile(f'./{user_id}.pickle'):
        user_data = pickle.load(open(f'./{user_id}.pickle', 'rb'))
        count_new = count - user_data['count']
        if count_new != 0:
            print(f"========{user_id}님이 새로 푼 문제 수 ({count_new})========")
            if count_new:
                if len([x for x in solved_list if x not in user_data['solved_list']]) == 0:
                    print(f"{user_id}님이 푼 상위 100문제 안에 들지 않네요!")
                else:
                    print(f"========{user_id}님이 새로 푼 문제(들)========\n({[x for x in solved_list if x not in user_data['solved_list']]})========")
        else:
            print(f"========{user_id}님이 새로 푼 문제가 없네요!========")

    f = open(f'{user_id}.pickle', 'wb')

    pickle.dump({'count' : count, 'solved_list' : solved_list, 'tier' : profile_dict['tier']}, f)
    f.close()
    