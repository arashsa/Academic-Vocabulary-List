import sys
import os
import multiprocessing as mp


def tag(file_path):
    print file_path
    os.system('./tag-bm.sh "' + file_path + '" > "' + file_path + '.obt"')

proc_list = []
for root, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        if f.endswith('.txt') and not f.endswith('_metadata.txt') and not f.endswith('.pdf') and not f.endswith('.obt'):
            p = os.path.join(root, f)
            print p
            process = mp.Process(target=tag, args=(p, ))
            proc_list.append(process)
            try:
                process.start()
            except Exception as e:
                print e

for p in proc_list:
    p.join()