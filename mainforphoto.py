import requests
import random
import string
from PIL import Image, ImageFilter, ExifTags
from io import BytesIO
from aiohttp import FormData
from aiogram.types import InputFile
from connect import write_key, print_all_keys, get_count, delete_key, check, get_info_db, print_all, write, delete, get_real_count



def get_random_name():
    length = 10
    # choose from all lowercase letter
    symbols = "abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLXCVBNM1234567890"
    return (''.join(random.choice(symbols) for i in range(length)))
# print(get_random_name())


import aiohttp
import asyncio


# api_key = 'MtT24Hwq9XGDzUY4po9u1Sqq'


async def give_apikey():
    all_keys = await print_all_keys()
    random_key = random.choice(list(all_keys.keys()))
    random_value = all_keys[random_key]
    if random_value < 5:
        await delete_key(random_key)
    else:
        return random_key
    # print(random_key, random_value)




async def request_photo(file_input_Bytes):
    api_key = await give_apikey()
    # byte = file_input_Bytes
    async with aiohttp.ClientSession() as session:
        # image = Image.open(file_input_Bytes)
        input_io_copy = BytesIO(file_input_Bytes.getvalue())
        image = Image.open(input_io_copy)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        try:
            exif=dict(image._getexif().items())
            if exif[orientation] == 3:
                image=image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image=image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image=image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Ошибка чтения EXIF-данных
            pass

        # image.show() # показать изображение
        # print(1564564, image.size)

        data = aiohttp.FormData()
        data.add_field('image_file', file_input_Bytes, filename='image.png')
        data.add_field('size', 'auto')
        headers = {'X-Api-Key': api_key}
        async with session.post('https://api.remove.bg/v1.0/removebg', data=data, headers=headers) as response:
            if response.status == 200:
                result_image_bytes = BytesIO(await response.read())
                image1 = Image.open(result_image_bytes)
                # image1.show()
                # image.save(file_input_Bytes, format="PNG")
                image2 = image
                image1 = image1.resize(image2.size)
                # image2.show()

                # print(image1.size, image2.size)

                # print(2)


                result_image = Image.new('RGBA', image2.size)
                # print(3)

                result_image.paste(image1, (0, 0))
                mask = image1.convert('L')
                # mask.show()
                result_image.paste(image2, (0, 0), image1)

                result_image_bytes2 = BytesIO()
                result_image.save(result_image_bytes2, format='PNG')
                result_image_bytes2.seek(0)

                # result_image_bytes.seek(0)
                filename = "result.png"
                input_file = InputFile(BytesIO(result_image_bytes2.getvalue()), filename=filename)
                await write_key(api_key)
                return input_file
            else:
                if "Insufficient credits" in str(await response.read()):
                    print('token is killed')
                await write_key(api_key)

                return False





# result_folder = r'C:\Users\artsl\Documents\python\delbg\results'

# async def request_photo(file_input_Bytes, api_key):
#     # try:
#     async with aiohttp.ClientSession() as session:
#         data = aiohttp.FormData()
#         data.add_field('image_file', file_input_Bytes, filename='image.jpg')
#         data.add_field('size', 'auto')
#         headers = {'X-Api-Key': api_key}
#         async with session.post('https://api.remove.bg/v1.0/removebg', data=data, headers=headers) as response:
#             if response.status == 200:
#                 image1 = Image.open(BytesIO(await response.content.read()))
#                 image2 = Image.open(file_input_Bytes)
#                 image2.show()
#                 summ_x_y = image2.size[0] * image2.size[1]
#                 if summ_x_y < 100000:
#                     box_blur = 1;
#                 elif 100000 < summ_x_y < 300000:
#                     box_blur = 3;
#                 elif 300000 < summ_x_y < 800000:
#                     box_blur = 4;
#                 elif 800000 < summ_x_y:
#                     box_blur = 6;

#                 # Изменяем размер второго изображения до размеров первого изображения
#                 image1 = image1.resize(image2.size)
#                 image1 = image1.filter(ImageFilter.EDGE_ENHANCE)
#                 image1 = image1.filter(ImageFilter.BoxBlur(box_blur))  # .filter(ImageFilter.EDGE_ENHANCE)

#                 # Создаем новое изображение
#                 result_image = Image.new('RGBA', image1.size)

#                 # Накладываем второе изображение на первое с использованием маски
#                 result_image.paste(image1, (0, 0))
#                 mask = image1.convert('L')
#                 result_image.paste(image2, (0, 0), image1)

#                 result_image_bytes = BytesIO()
#                 result_image.save(result_image_bytes, format='PNG')
#                 # result_image_bytes.seek(0)
#                 result_image.show()

#                 filename = "result.png"
#                 input_file = InputFile(result_image_bytes, filename=filename)

#                 return input_file
#             else:
#                 return False
    # except:
    #     return False



# async def request_photo(file_input_Bytes, api_key):
#     # try:
#     async with aiohttp.ClientSession() as session:
#         data = aiohttp.FormData()
#         data.add_field('image_file', file_input_Bytes, filename='image.png')
#         data.add_field('size', 'auto')
#         async with session.post('https://api.remove.bg/v1.0/removebg', data={'size', 'auto'}, files={'image_file': file_input_Bytes}, headers={'X-Api-Key': api_key}) as response:
#         # response = requests.post(
#         #     'https://api.remove.bg/v1.0/removebg',
#         #     files={'image_file': file_input_Bytes},
#         #     data={'size': 'auto'},
#         #     headers={'X-Api-Key': api_key},
#         # )
#             if response.status_code == requests.codes.ok:

#                 image1 = Image.open(BytesIO(await response.content.read()))
#                 image2 = Image.open(file_input_Bytes)
#                 # image1.show()

#                 summ_x_y = image2.size[0] * image2.size[1]
#                 if summ_x_y < 100000: 
#                     box_blur = 1;
#                 elif 100000 < summ_x_y < 300000: 
#                     box_blur = 3;
#                 elif 300000 < summ_x_y < 800000: 
#                     box_blur = 4;
#                 elif 800000 < summ_x_y: 
#                     box_blur = 6;
                    
#                 # Изменяем размер второго изображения до размеров первого изображения
#                 image1 = image1.resize(image2.size)
#                 image1 = image1.filter(ImageFilter.EDGE_ENHANCE)
#                 image1 = image1.filter(ImageFilter.BoxBlur(box_blur))#.filter(ImageFilter.EDGE_ENHANCE)


#                 # Создаем новое изображение
#                 result_image = Image.new('RGBA', image1.size)


#                 # Накладываем второе изображение на первое с использованием маски
#                 result_image.paste(image1, (0, 0))
#                 mask = image1.convert('L')
#                 result_image.paste(image2, (0, 0), image1)

#                 result_image_bytes = BytesIO()
#                 result_image.save(result_image_bytes, format='PNG')
#                 result_image_bytes.seek(0)

#                 filename = "result.png"
#                 input_file = InputFile(result_image_bytes, filename=filename)

#                 return input_file
#             else:
#                 return False
    # except:
    #     return False

# while True:
#     file = str(input("Give a file for changing:"))
#     print(request_photo(file))
#     print('complete')
