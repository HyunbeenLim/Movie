import openai
from django.conf import settings
import os

openai.api_key = 'sample_key'

def chat_with_gpt(user, user_message):
    from movies.models import ChatMessage
    
    file_path = os.path.join(settings.BASE_DIR, 'movies', 'utils', 'prompt.txt')
    prompt_text = open(file_path, mode='r', encoding='utf-8')

    # 초기 프롬프트 설정
    initial_prompt = {"role": "system", "content": prompt_text.read()}

    # 해당 사용자의 대화 기록 불러오기
    chat_history = ChatMessage.objects.filter(user=user).order_by('timestamp')
    messages = [initial_prompt] + [
        {"role": msg.role, "content": msg.content} for msg in chat_history
    ]

    # 사용자의 메시지 추가
    messages.append({"role": "user", "content": user_message})

    # OpenAI API 호출
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    # GPT의 응답 저장
    bot_response = response.choices[0].message.content
    ChatMessage.objects.create(user=user, role="user", content=user_message)
    ChatMessage.objects.create(user=user, role="assistant", content=bot_response)

    return bot_response