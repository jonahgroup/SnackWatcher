import os
import sys

if (len(sys.argv) < 2):
    print "Usage: %s rename_prefix" % sys.argv[0]
    exit(0)

files = os.listdir('.')
prefix = sys.argv[1]

num = 1
for file in files:
    if file.endswith('.png'):
        (name, ext) = os.path.splitext(file)
        outname = prefix + '_' + ('%03d' % num) + ext
        print 'rename %s to %s' % (file, outname)
        os.rename(file, outname)
        num += 1
