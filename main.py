#===============================================================================
# Trabalho 3 - Bloom
#-------------------------------------------------------------------------------
# Autora: Mayara Dal Vesco Hoger
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'img.png'
THRESHOLD = 180

#===============================================================================

def bright_pass(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, mascara = cv2.threshold(cinza, THRESHOLD, 255, cv2.THRESH_BINARY)
    
    mascara_rgb = cv2.merge([mascara, mascara, mascara])
    
    bright_pass_result = cv2.bitwise_and(img, mascara_rgb)

    cv2.imwrite ('bright_pass_result.png', bright_pass_result)
    return bright_pass_result

def borrar_mascara_gaussian(mascara):
    mascara = mascara.astype (np.float32) / 255
    sigma = 2
    gaussian = mascara
    soma = mascara
    while sigma < 20:
        gaussian = cv2.GaussianBlur(gaussian, (0,0), sigma)
        soma = soma + gaussian
        sigma = sigma*2
    
    soma = np.where(soma > 1, 1, soma)
    soma = soma * 255
    cv2.imwrite ('gaussian.png', soma)
    return soma

def borrar_mascara_box_blur(mascara):
    mascara = mascara.astype (np.float32) / 255
    kernel = (15, 15)
    blur = mascara
    soma = mascara
    for x in range(0, 5):
        blur = cv2.blur(blur, kernel)
        soma = soma + blur
    
    soma = np.where(soma > 1, 1, soma)
    soma = soma * 255
    cv2.imwrite ('blur.png', soma)
    return soma

def juntar_mascara(img, mascara):
    alfa = 0.7
    beta =  1 - alfa
    return alfa*img + beta*mascara 

def main():
     # Abre a imagem.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)

    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
		
    mascara = bright_pass(img)
    mascara_gaussian = borrar_mascara_gaussian(mascara)
    mascara_blur = borrar_mascara_box_blur(mascara)

    result_gaussian = juntar_mascara(img, mascara_gaussian)
    result_blur = juntar_mascara(img, mascara_blur)

    cv2.imwrite("result_gaussian.png", result_gaussian)
    cv2.imwrite("result_blur.png", result_blur)

if __name__ == '__main__':
    main ()