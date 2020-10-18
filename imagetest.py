from PIL import Image, ImageFont, ImageDraw
import qrcode

voucher_accept_url = "http://127.0.0.1:10002/service-vouchers/redeem/" + "123" # URL TO BE CHANGED
qr = qrcode.make(voucher_accept_url)
voucher_type = 'Meal'
background = Image.open('vouchers/images/' + voucher_type + '.jpg')

background.paste(qr, (300, 600))
draw = ImageDraw.Draw(background)

#Draw title
font = ImageFont.truetype('C:/Users/andre/AppData/Local/Microsoft/Windows/Fonts/Helvetica 400.ttf', 80)
if voucher_type == 'meal':
    title = "Meal Voucher"
    w,h = font.getsize(title)
    draw.text(((1000-w)/2, 100), title ,(0,0,0),font=font)

elif voucher_type == 'hotel':
    title = "Hotel Voucher"
    w,h = font.getsize(title)
    draw.text(((1000-w)/2, 100), title ,(0,0,0),font=font)

elif voucher_type == 'lounge':
    title = "Lounge Voucher"
    w,h = font.getsize(title)
    draw.text(((1000-w)/2, 100), title ,(0,0,0),font=font)

elif voucher_type == 'transport':
    title = "Transport Voucher"
    w,h = font.getsize(title)
    draw.text(((1000-w)/2, 100), title ,(0,0,0),font=font)

#draw content
font = ImageFont.truetype('C:/Users/andre/AppData/Local/Microsoft/Windows/Fonts/Helvetica 400.ttf', 40)
title = "Entitled to one free night at Hotel"
w,h = font.getsize(title)
draw.text(((1000-w)/2, 250), title ,(0,0,0),font=font)

background.save('vouchers/vouchers/test' + '.jpg')
background.show()
#voucher_image.save('vouchers/vouchers/vid.jpg')