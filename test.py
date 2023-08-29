import pygame
import sys
from TextView import TextView
from Button import Button


def test():
    # pygame 초기화
    pygame.init()

    # 스크린 객체 저장
    screen = pygame.display.set_mode((512, 512))
    pygame.display.set_caption("Game")

    # 게임 시간을 위한 Clock 생성
    clock = pygame.time.Clock()

    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 스크린 배경색 칠하기
        screen.fill((255, 255, 255))

        text = TextView(screen, "테스트", "fonts/ELAND_Choice_M.ttf", 100, (0, 0, 0), (512//2, 512//2), (255, 0, 255))
        text.showText()
        button = Button(screen, '테슬라', 50, (0, 0, 0), (512//2, 512//10), (200, 100), (255, 0, 0), (0, 255, 0), 10)
        button.onClickListener()
        # 작업한 내용 갱신하기
        pygame.display.flip()

        # 1초에 60번의 빈도로 순환하기
        clock.tick(60)


# test()


movie_rank = ["닥터 스트레인지", "스플릿", "럭키"]
movie_rank.append("배트맨")
print(movie_rank)

movie_rank.insert(1, "슈퍼맨")
print(movie_rank)

movie_rank.remove("럭키")
print(movie_rank)

# del movie_rank[2:]
del movie_rank[-2:]
print(movie_rank)

lang1 = ["C", "C++", "JAVA"]
lang2 = ["Python", "Go", "C#"]
langs = lang1 + lang2
print(langs)


nums = [1, 2, 3, 4, 5, 6, 7]
print("max :", max(nums))
print("min :", min(nums))

nums = [1, 2, 3, 4, 5]
print(sum(nums))

cook = ["피자", "김밥", "만두", "양념치킨", "족발", "피자", "김치만두", "쫄면", "쏘세지", "라면", "팥빙수", "김치전"]
print(len(cook))

nums = [1, 2, 3, 4, 5]
print(sum(nums) / len(nums))

