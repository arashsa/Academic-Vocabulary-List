import sys
import os
import multiprocessing as mp


def tag(file_path):
    print file_path
    os.system('./tag-bm.sh "' + file_path + '" > "' + file_path + '.obt"')

proc_list = []
count = 0
for root, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        if f.endswith('.obt'):
            p = os.path.join(root, f)
            if os.stat(p).st_size == 0:
                count += 1
                process = mp.Process(target=tag, args=(p.replace('.obt', ''), ))
                proc_list.append(process)
                try:
                    process.start()
                except Exception as e:
                    print e

for p in proc_list:
    p.join()

print count