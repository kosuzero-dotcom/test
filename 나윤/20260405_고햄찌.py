import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("우주로 가는 무한의 계단")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
STAIR_COLOR = (200, 200, 200)
STAIR_SHADOW = (150, 150, 150)

# 폰트 설정
font_large = pygame.font.SysFont("malgungothic", 48, bold=True)
font_medium = pygame.font.SysFont("malgungothic", 32, bold=True)

# 게임 변수
score = 0
game_over = False
STAIR_WIDTH = 100
STAIR_HEIGHT = 20
STEP_X = 80  # 좌우 이동 간격
STEP_Y = 60  # 상하 이동 간격

# 계단 리스트 초기화 함수
def init_stairs():
    stairs = []
    # 캐릭터가 서 있는 첫 번째 계단은 화면 중앙 하단
    current_x = WIDTH // 2
    current_y = HEIGHT - 150
    stairs.append({'x': current_x, 'y': current_y})
    
    # 미리 20개의 계단을 생성
    for _ in range(20):
        direction = random.choice([-1, 1]) # -1: 왼쪽, 1: 오른쪽
        current_x += direction * STEP_X
        current_y -= STEP_Y
        stairs.append({'x': current_x, 'y': current_y})
    return stairs

stairs = init_stairs()

# 우주 배경용 별 생성
stars = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'size': random.randint(1, 3)} for _ in range(100)]

# 게임 루프
running = True
while running:
    # 1. 이벤트 처리 (키보드 입력)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if game_over:
                # 게임 오버 시 스페이스바로 재시작
                if event.key == pygame.K_SPACE:
                    score = 0
                    game_over = False
                    stairs = init_stairs()
            else:
                # 다음 계단이 현재 계단보다 왼쪽에 있는지 오른쪽에 있는지 판별
                current_x = stairs[0]['x']
                next_x = stairs[1]['x']
                
                correct_key = False
                if event.key == pygame.K_LEFT and next_x < current_x:
                    correct_key = True
                elif event.key == pygame.K_RIGHT and next_x > current_x:
                    correct_key = True
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # 방향키를 눌렀는데 틀린 경우
                    game_over = True
                
                # 올바른 방향키를 누른 경우 (계단 오르기 성공)
                if correct_key:
                    score += 1
                    # 현재 계단을 제거하고 맨 위에 새 계단 추가
                    stairs.pop(0)
                    last_stair = stairs[-1]
                    new_dir = random.choice([-1, 1])
                    stairs.append({'x': last_stair['x'] + new_dir * STEP_X, 'y': last_stair['y'] - STEP_Y})
                    
                    # 카메라 효과: 캐릭터가 항상 제자리에 있는 것처럼 보이도록 모든 계단의 위치를 아래로 내림
                    shift_x = (WIDTH // 2) - stairs[0]['x']
                    shift_y = (HEIGHT - 150) - stairs[0]['y']
                    for s in stairs:
                        s['x'] += shift_x
                        s['y'] += shift_y

    # 2. 배경색 계산 (점수가 올라갈수록 하늘 -> 우주로 변화)
    # 점수 100점일 때 완전한 우주(진한 남색/검정)가 되도록 비율 계산
    progress = min(1.0, score / 100.0) 
    
    # 하늘색 (135, 206, 235) -> 우주색 (10, 10, 30)으로 그라데이션 전환
    r = int(135 * (1 - progress) + 10 * progress)
    g = int(206 * (1 - progress) + 10 * progress)
    b = int(235 * (1 - progress) + 30 * progress)
    screen.fill((r, g, b))

    # 우주에 가까워질수록(점수가 높을수록) 별이 밝게 보임
    if progress > 0.1:
        star_brightness = int(255 * progress)
        for star in stars:
            pygame.draw.circle(screen, (star_brightness, star_brightness, star_brightness), (star['x'], star['y']), star['size'])

    # 3. 화면 그리기
    # 계단 그리기
    for s in stairs:
        rect = pygame.Rect(s['x'] - STAIR_WIDTH//2, s['y'], STAIR_WIDTH, STAIR_HEIGHT)
        pygame.draw.rect(screen, STAIR_SHADOW, (rect.x, rect.y + 5, rect.width, rect.height)) # 그림자
        pygame.draw.rect(screen, STAIR_COLOR, rect) # 계단

    # 캐릭터 그리기 (항상 화면의 고정된 위치에 존재)
    char_width, char_height = 40, 50
    char_x = (WIDTH // 2) - (char_width // 2)
    char_y = (HEIGHT - 150) - char_height
    
    if not game_over:
        pygame.draw.rect(screen, RED, (char_x, char_y, char_width, char_height))
    else:
        # 게임 오버 시 캐릭터가 떨어지는 연출 (아래로 살짝 이동)
        pygame.draw.rect(screen, RED, (char_x, char_y + 50, char_width, char_height))

    # 점수(올라간 계단 수) 표시
    score_text = font_large.render(str(score), True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))

    # 게임 오버 텍스트 표시
    if game_over:
        over_text = font_medium.render("게임 오버! (재시작: SPACE)", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()