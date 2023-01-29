from PIL import Image, ImageDraw, ImageFont
import asyncio
import base64
from io import BytesIO
import json
import numpy as np

async def photo_with_currencies(arrAnarchyPrices):
	im = Image.open('Frame 1.png')
	draw_text = ImageDraw.Draw(im)

	font = ImageFont.truetype('IstokWeb-Regular.ttf', size=60)
	arr_y = {'binance   ': 572, 'whitebit  ':679, "kuna        ":785, "okx           ":892, "huobi       ":998, "qmall       ":1105, "exmo       ":1211, "bybit        ":1318, "kucoin     ":1426}
	inx = 0
	for i in arrAnarchyPrices:
		for t in i:
			if float(i.get(t)) != 0:
				draw_text.text((529,arr_y[t]), str(i.get(t)), font=font, fill=('#FFFFFF'))
				print(str(i.get(t)))
			else:
				draw_text.text((529,arr_y[t]), '***', font=font, fill=('#FFFFFF'))
	# buffered = BytesIO()
	im = im.convert("RGB")
	# im.save(buffered, format="JPEG")
	# img_str = base64.b64encode(buffered.getvalue())
	# json_data = json.dumps(np.array(im).tolist())
	# new_image = Image.fromarray(np.array(json.loads(json_data), dtype='uint8'))
	buffered = BytesIO()
	buffered.name = 'image.jpeg'
	im.save(buffered, 'PNG')
	buffered.seek(0)

	return buffered
