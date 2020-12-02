import cv2 as cv
import numpy as np
#default images directory
images_dir = '/Users/larsdepauw/Documents/Lars.nosync/Documents/School/1Ma ing/Masterproef/TWI/code/Vision/Datasets/second_automated/birthday_dataset/'

strips = ["A", "B"]


batches = [1,2,3,4,5,11]


def view_color_batch(bnr, pnr, color):

    minled=3
    maxled=12
    fraction = 1 / ((maxled - minled) * 2)
    fraction = 1
    #print(str(fraction)+ 'fraction * 9*2: '+str(fraction*18))
    save_dir = images_dir + 'batch_' + bnr + '_plate_' + pnr + '/'
    result = cv.imread(save_dir + 'b_' + bnr + '_p_' + pnr + '_' + bullet + '_l_' + '000' + '_' + color + '_' + 'A' + '.png')
    for light in range(minled, maxled):
        lnr = '{:03d}'.format(light)
        for strip in strips:

            url = save_dir + 'b_' + bnr + '_p_' + pnr + '_' + bullet + '_l_' + lnr + '_' + color + '_' + strip + '.png'
            #print(url)
            img = cv.imread(url)


            result = cv.addWeighted(result, fraction, img, fraction, 0.0)

    return result

index = 0
batch = batches[0]
plate = 1
bullet = 'nb'
last = 0
#for batch in batches:
while batch in batches:

    #for plate in range(1,11):
   # while plate < 11:
        #for bullet in ["nb", "b"]:

            # format plate and batch number
            bnr = '{:03d}'.format(batch)
            pnr = '{:03d}'.format(plate)

            save_dir = images_dir + 'batch_' + bnr + '_plate_' +pnr + '/'
            path =save_dir+'b_'+bnr+'_p_'+pnr+'_l_000_'+bullet+'.png'
            img = cv.imread(path)
            if img is None:
                print("could not read image "+path)
                break

            print('batch: '+bnr+' plate: '+pnr+' bullet: '+bullet)
            cv.imshow('img', img )
            white = view_color_batch(bnr, pnr, 'white')
            red = view_color_batch(bnr, pnr, 'red')
            blue = view_color_batch(bnr, pnr, 'blue')
            green = view_color_batch(bnr, pnr, 'green')
            resup = np.hstack((white, red))
            resdown = np.hstack((blue, green))
            res = np.vstack((resup, resdown))

            cv.imshow("result", res)

            if True:
                if cv.waitKey(0) & 0xFF == ord('a'):
                    #volgende
                    if bullet == 'b':
                        if plate == 10:
                            # last plate
                            index+=1
                            batch = batches[index]
                            plate = 1
                        else:
                            plate += 1
                    print("next")
                elif cv.waitKey(0) & 0xFF == ord('z'):
                    #volgende
                    if bullet != 'b':
                        if plate == 1:
                            # first plate of batch, go to previous batch
                            index -=1
                            batch = batches[index]
                            plate = 10
                        else:
                            plate -= 1
                    print("previous")
                    if  plate != 1 and batch != batches[0]:
                        #last = 1
                        print('last')
            if bullet == 'nb' and last !=1:
                bullet = 'b'
            else:
                bullet = 'nb'


