import cv2
import os
import numpy as np

def pixelate():

    width, height = 16, 24
    directories = ["covers", "posters", "podcasts"]
    scale_factor = 3
    debug = False

    for directory in directories:
        
        artwork = os.listdir(f"site/images/{directory}")

        resized_art = []
        rows = []

        for art in artwork:
            img = cv2.imread(f"site/images/{directory}/{art}")
            img = cv2.resize(img, (width, height))
            img = cv2.resize(img, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_AREA)
            resized_art.append(img)
            cv2.imwrite(f"site/images/pixelated_{directory}/{art}", img)
            if debug:
                cv2.imshow("ART", img)
                cv2.waitKey(1)

        h, w, c = resized_art[-1].shape
        black_cover = np.zeros((h, w, c), dtype=np.uint8)

        for i in range(0, len(resized_art), 5):
            batch = resized_art[i:i + 5]
            while len(batch) < 5:
                batch.append(black_cover)

            row = cv2.hconcat(batch)
            rows.append(row)
            if debug:
                cv2.imshow("ART", row)
                cv2.waitKey(1)
            
        cover_grid = cv2.vconcat(rows)
        if debug:
            cv2.imshow("ART", cover_grid)
            cv2.waitKey(1)
