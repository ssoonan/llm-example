from openai import OpenAI
import os

openai_client = OpenAI(
  api_key=os.environ['OPENAI_KEY']
)

import requests
import json
 
 
def weather():
    apikey = os.environ['OPEN_WEATHER']
    api = f"""http://api.openweathermap.org/data/2.5/weather?lat=37.5683&lon=126.9778&appid={apikey}"""
    result = requests.get(api)
    data = json.loads(result.text)
    return data['main']['temp']


def diet(current, goal, month):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 건강과 운동에 관한 전문가입니다. 사용자가 건강과 관련된 질문에 대해 명확하고 실용적인 조언을 제공하는 것이 당신의 임무입니다."},
            {"role": "user", "content": f"""
            Context: 사용자는 체중 감량을 목표로 하고 있으며, 효과적인 운동 루틴과 식단에 대한 정보를 필요로 합니다.\n\n
            Input Data: 사용자의 현재 체중은 {current}kg이며, 목표 체중은 {goal}kg을 {month}달 안에 만들고 싶어.\n\n
            Output Indicator: 체중 감량을 위한 주간 운동 루틴과 함께 추천 식단을 제공해 주세요."""}
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


def poet(weather):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 아름다운 시를 만드는 재능을 가진 도우미입니다. 주어진 입력에 따라 날씨와 기분을 반영한 시를 작성하는 것이 당신의 임무입니다."},
            {"role": "user", "content": f"""
            Context: 사용자는 현재 날씨와 기분을 바탕으로 시를 작성하고자 합니다.\n\n
            Input Data: {weather}\n\n
            Output Indicator: 주어진 날씨와 기분을 반영한 아름다운 시를 작성해 주세요."""}

        ]
    )
    print(response.choices[0].message.content)
# poet("현재 날씨는 24도에 선선함, 기분은 놀고 싶어서 근질거린다.")

def recommend_menu(current_mood, preferred_food_type, hunger_level, dining_companion):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 사용자의 현재 상태와 선호도를 바탕으로 적절한 메뉴를 추천하는 도우미입니다. 사용자가 제공한 정보를 통해 오늘의 메뉴를 추천하는 것이 당신의 임무입니다."},
            {"role": "user", "content": f"""
             Context: 사용자는 오늘의 메뉴를 추천받고자 합니다.\n\n
             Input Data: 현재 기분은 {current_mood}, 선호하는 음식 종류는 {preferred_food_type}, 현재 배고픔의 정도는 {hunger_level}, 식사를 함께할 사람은 {dining_companion}입니다.\n\n
             Output Indicator: 주어진 정보에 따라 오늘의 메뉴를 추천해주되 응원의 한마디: ~, 메인: ~, 반찬: ~ 의 형태로 출력해줘"""}
        ]
    )
    
    print(response.choices[0].message.content)
# recommend_menu("기쁨", "양식", "적당히 배고픔", "두명")

def generate_quote(current_mode):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 세계 각국의 유명한 인물의 명언을 제공하는 도우미입니다. 사용자가 제공한 나라를 바탕으로 해당 나라의 유명한 사람의 명언을 생성하는 것이 당신의 임무입니다."},
            {"role": "user", "content": f"""
             Context: 사용자는 특정 기분일 때 이에 맞는 명언을 알고자 합니다.\n\n
             Input Data: 현재의 기분은 {current_mode}\n\n
             Output Indicator: 명언: ~ 의 형태로 간결하게 출력해주세요\n\n"""}
        ]
    )
    print(response.choices[0].message.content)
# generate_quote("당당함")

def provide_answer_based_on_context(context, question):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 주어진 문맥에 기반하여 정확하고 관련성 있는 정보를 제공하는 도우미입니다."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
    
    print(response.choices[0].message.content)
provide_answer_based_on_context("", "어떤 운동을 하는 게 좋을까?")