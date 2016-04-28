from SimpleCV import *

img_background = Image("snack-background.jpg")

img_snack = Image("snack-snack1.jpg")

img_diff = (img_snack - img_background).invert()
img_diff_bin = img_diff.binarize(thresh=250)

snack_blobs = img_diff_bin.findBlobs(minsize=100)
snack_blobs.draw(color=Color.RED, width=2)
img_snack.addDrawingLayer(img_diff_bin.dl())

img_snack.save("snack-result.jpg")

while True:
    img_snack.show()
