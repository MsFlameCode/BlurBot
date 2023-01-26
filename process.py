import emoji
from PIL import Image, ImageDraw, ImageFont
import const
from pilmoji import Pilmoji
import cv2


def create_blur_emoji(str_emoji):
    em = emoji.emojize(str_emoji)
    create_image_with_emoji(em)


def create_image_with_emoji(em):
    with Image.new('RGBA', (150, 150), (255, 255, 255, 0)) as image:
        font = ImageFont.truetype('Lobster-Regular.ttf', 100)

        with Pilmoji(image) as pilmoji:
            pilmoji.text((10, 10), em, (0, 0, 0), font)
        image.show()
        const.CUR_NAME = 'front_{:d}.png'.format(const.CONST_COUNT)
        image.save(const.CUR_NAME)
        const.CONST_COUNT += 1
        blur_image()

def blur_image():
    kernal_size = 10
    if const.IS_PHOTO:
        const.CUR_NAME = const.PHOTO_NAME
        kernal_size = 20
    image = cv2.imread(const.CUR_NAME, cv2.IMREAD_UNCHANGED)
    img_rst = cv2.blur(image, (kernal_size, kernal_size))
    const.CUR_NAME = 'front_{:d}.png'.format(const.CONST_COUNT)
    const.CONST_COUNT += 1
    cv2.imwrite(const.CUR_NAME, img_rst)
