import pygame
from PIL import Image, ImageEnhance
import os
import pprint

_all_images = None
_initialized = False


def pil_to_pygame(pil_image):
    """
    :param: pil_image: a PIL image

    :return: a pygame image

    :py:obj:`PIL.Image.Image` -> :py:obj:`pygame.Surface`
    """
    return pygame.image.frombuffer(pil_image.tobytes(), pil_image.size, pil_image.mode)
def pygame_to_pil(image: pygame.Surface):
    """
    :param image: a pygame image

    :return: a PIL image

    :py:obj:`pygame.Surface` -> :py:obj:`PIL.Image.Image`
    """
    image = image.convert_alpha()
    return Image.frombuffer("RGBA", image.get_size(), image.get_view("2"), "raw", "RGBA", 0, 1)
def load(path: str) -> pygame.Surface:
    return pil_to_pygame(Image.open(path))

def init():
    global _initialized, _all_images
    if not _initialized:
        _all_images = _extract_all_files("./Mario/images")
        _initialized = True

def _extract_all_files(path: str):
    """
    :param path: a path to a folder
    :return: a dictionary :py:obj:`str` -> :py:obj:`dict` of all the images in the folder as a tree structure
    \n
    .. note::
        This function is recursive
    """
    if os.path.isdir(f"{path}"):
        result = {}
        for file in os.listdir(f"{path}"):
            result[file.split(".")[0]] = _extract_all_files(f"{path}/{file}")
        return result
    else:
        # print(path)
        return load(f"{path}")

def get_images(name: str):
    init()
    assert name in _all_images, f"image folder {name} not found"
    return _all_images.get(name)

def print_all_images():
    init()
    pprint.pprint(_all_images)

def change_color(color: tuple[float, float, float], image: pygame.Surface) -> pygame.Surface:
    image = pygame_to_pil(image)
    image = image.convert("RGBA")
    r, g, b, a = image.split()
    r = r.point(lambda i: i * color[0])
    g = g.point(lambda i: i * color[1])
    b = b.point(lambda i: i * color[2])
    image = Image.merge("RGBA", (r, g, b, a))
    return pil_to_pygame(image)
def change_brightness(brightness: float, image: pygame.Surface) -> pygame.Surface:
    image = pygame_to_pil(image)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    return pil_to_pygame(image)
def change_contrast(contrast: float, image: pygame.Surface) -> pygame.Surface:
    image = pygame_to_pil(image)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    return pil_to_pygame(image)
def change_black_white(bw: bool, image: pygame.Surface) -> pygame.Surface:
    image = pygame_to_pil(image)
    if bw:
        image = image.convert("LA")
        image = image.convert("RGBA")
    return pil_to_pygame(image)
def remove_color(color: tuple[float, float, float], image: pygame.Surface) -> pygame.Surface:
    image = pygame_to_pil(image)
    inrange = 0 <= color[0] <= 1 and\
              0 <= color[1] <= 1 and\
              0 <= color[2] <= 1
    assert inrange, "color values must be a float between 0 and 1"
    image = image.convert("RGBA")
    r, g, b, a = image.split()
    r = r.point(lambda i: int(i * (1 - color[0])))
    g = g.point(lambda i: int(i * (1 - color[0])))
    b = b.point(lambda i: int(i * (1 - color[0])))
    image = Image.merge("RGBA", (r, g, b, a))
    return pil_to_pygame(image)
def add_color(color: tuple[float, float, float], image: pygame.Surface) -> pygame.Surface:
    image = pygame_to_pil(image)
    inrange = 0 <= color[0] <= 1 and\
              0 <= color[1] <= 1 and\
              0 <= color[2] <= 1
    assert inrange, "color values must be a float between 0 and 1"
    image = image.convert("RGBA")
    r, g, b, a = image.split()
    r = r.point(lambda i: min(int(i * (1 + color[0])), 255))
    g = g.point(lambda i: min(int(i * (1 + color[1])), 255))
    b = b.point(lambda i: min(int(i * (1 + color[2])), 255))
    image = Image.merge("RGBA", (r, g, b, a))
    return pil_to_pygame(image)
def show(image: pygame.Surface) -> None:
    image = pygame_to_pil(image)
    image.show()

def resize_all(size: tuple[int, int], images: dict[str, dict | pygame.Surface], resize_mode: str = "nearest") -> dict[str, dict | pygame.Surface]:
    """Resize all images to the given size and return the same tree structure as the original one."""
    result = {}
    for key, value in images.items():
        if isinstance(value, dict):
            result[key] = resize_all(size, value)
        else:
            result[key] = resize(size, value)
    return result

def scale_all(scale: float, images: dict[str, dict | pygame.Surface]) -> dict[str, dict | pygame.Surface]:
    """Scale all images by the given scale and return the same tree structure as the original one."""
    result = {}
    for key, value in images.items():
        if isinstance(value, dict):
            result[key] = scale_all(scale, value)
        else:
            result[key] = resize((int(value.get_width() * scale), int(value.get_height() * scale)), value)
    return result

def resize(size: tuple[int, int], image: pygame.Surface, resize_mode: str = "nearest") -> pygame.Surface:
    if resize_mode == "nearest":
        image = pygame.transform.scale(image, size)
        return image
    image = pygame_to_pil(image)
    match resize_mode:
        case "bilinear":
            image = image.resize(size, Image.BILINEAR)
        case "bicubic":
            image = image.resize(size, Image.BICUBIC)
        case "lanczos":
            image = image.resize(size, Image.LANCZOS)
        case "nearest":
            image = image.resize(size, Image.NEAREST)
        case _:
            raise ValueError(f"Unknown resize mode: {resize_mode}")
    return pil_to_pygame(image)