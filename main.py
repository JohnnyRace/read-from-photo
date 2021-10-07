import cv2
import numpy as np
import pytesseract
import os
import json

output = {
    'Выписка из протокола': '',
    'пункт': '',
    'номер': '',
    'дата': '',
    'Наименование объекта': '',
    'Авторы проекта': '',
    'Генеральная проектная организация': '',
    'Застройщик': '',
    'Референт': '',
    'Докладчик': '',
    'Выступили': ''
}

for image_name in os.listdir('cv'):
    if image_name.endswith('jpg'):
        im1 = cv2.imread(f'cv/{image_name}', 0)
        im = cv2.imread(f'cv/{image_name}')
        background = np.zeros(im.shape[:2], dtype='uint8')

        ret, thresh_value = cv2.threshold(im1, 180, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((1, 1), np.uint8)
        dilated_value = cv2.dilate(thresh_value, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(thresh_value, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            S = w * h
            if S >= 2000:
                # cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 1)
                i += 1
                crop_img = im[y:y + h, x:x + w]
                cv2.imwrite(f'crop{i}.jpg', crop_img)

        for key in output.keys():
            crop = cv2.imread(f'crop{i}.jpg')
            output[key] = pytesseract.image_to_string(image=crop, lang='rus').strip().replace('\n', ' ')
            os.remove(f'crop{i}.jpg')
            i -= 1

        with open(image_name.replace('jpg', 'json'), 'w', encoding='utf-8') as json_file:
            json.dump(output, json_file, indent=4)

        print(output)
