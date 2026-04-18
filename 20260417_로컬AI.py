from openai import OpenAI

# 1. LM Studio 로컬 서버 연결 설정
# LM Studio는 기본적으로 localhost의 1234 포트를 사용합니다.
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # 실제 API 키가 필요 없으므로 아무 문자나 넣어도 됩니다.
)

# 2. 대화 기록(Context)을 저장할 리스트 초기화
# system 역할을 부여하여 AI의 성격을 지정할 수 있습니다.
history = [
    {"role": "system", "content": "당신은 한국어로 대답하는 도움이 되고 친절한 AI 어시스턴트입니다."}
]

print("======================================================")
print(" 🤖 로컬 AI(Gemma) 챗봇과 대화를 시작합니다! ")
print(" (대화를 종료하려면 '종료', 'quit', 'exit' 중 하나를 입력하세요.)")
print("======================================================\n")

# 3. 챗봇 대화 루프
while True:
    # 사용자 입력 받기
    user_input = input("나: ")
    
    # 종료 조건
    if user_input.lower() in ['종료', 'quit', 'exit']:
        print("🤖 AI: 대화를 종료합니다. 로컬 AI 서버를 꺼주세요!")
        break
        
    if not user_input.strip():
        continue
        
    # 사용자의 질문을 대화 기록에 추가
    history.append({"role": "user", "content": user_input})
    
    try:
        # LM Studio 서버에 대화 기록 전송 및 응답 요청
        response = client.chat.completions.create(
            model="local-model", # LM Studio는 로드된 모델을 무조건 사용하므로 이름은 아무거나 적어도 됩니다.
            messages=history,
            temperature=0.7 # 0에 가까울수록 진지하고, 1에 가까울수록 창의적입니다.
        )
        
        # AI의 응답 텍스트 추출
        ai_message = response.choices[0].message.content
        print(f"🤖 AI: {ai_message}\n")
        
        # AI의 응답도 대화 기록에 추가하여 다음 질문 시 문맥을 기억하게 함
        history.append({"role": "assistant", "content": ai_message})
        
    except Exception as e:
        print(f"\n[오류 발생] 연결 실패! LM Studio에서 'Start Server'를 눌렀는지 확인해주세요.\n상세 오류: {e}\n")