from PIL import Image
import pygame

"""
# 모듈 작성자 : 장은재
# 모듈 작성일 : 2021.02.18
# 업데이트
## 2021.02.18 작성
"""


class ImageView:
    def __init__(self, surface, image_name, image_size):
        self._surface = surface
        self._image_name = image_name
        self._image_width, self._image_height = image_size

    def setSurface(self, surface):
        self._surface = surface

    def setImageName(self, image_name):
        self._image_name = image_name

    def setImageSize(self, image_size):
        pass


def resizeImage(image_folder: str, original_name: str, width: int, height: int, num=0):
    """
    :param image_folder: str -> 이미지 파일 경로('/이미지 이름' 이전의 파일 경로)
    :param original_name: str -> 이미지 이름(확장자 명을 뺀 이름/ .png 파일만 가능)
    :param width: int -> 이미지의 너비
    :param height: int -> 이미지의 높이
    :return: None
    """
    image = Image.open(f'{image_folder}/{original_name}.png')
    image_resize = image.resize((width, height))
    image_resize.save(f'{image_folder}/{original_name}_{width}x{height}.png')
    if num:
        return f'{image_folder}/{original_name}_{width}x{height}.png'


def getImageSize(image_folder: str, image_name: str):
    """
    :param image_folder: str -> 이미지 경로
    :param image_name: str -> 크기를 알고 싶은 이미지 이름
    :return: tuple -> image.size 를 반환, 즉 이미지의 너비와 높이(width, height)를 순서대로 튜플 형태로 반환
    """
    image_string = f"{image_folder}/{image_name}.png"
    image = Image.open(image_string)
    return image.size


def showImage(surface, image_name):
    load_image = pygame.image.load(f'images/{image_name}.png')
    load_image_rect = load_image.get_rect()
    load_image_rect.center = left + box_width // 2, top + box_height // 2
    surface.blit(load_image, load_image_rect)