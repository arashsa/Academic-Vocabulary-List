import sys
import os
import multiprocessing as mp


def tag(obt_path, corpora_path):
    print corpora_path
    os.system('cd ' + obt_path + ' && ./tag-bm.sh ' + corpora_path + ' > ' + corpora_path + '.obt')
    os.system('pwd')
    # os.system('./tag-bm.sh ' + path + ' > '
    #           + path + '.obt')

# proc_list = []
for root, dirs, files in os.walk(sys.argv[1]):
    for f in files:
        if f.endswith('.txt') and not f.endswith('_metadata.txt') and not f.endswith('pdf') and not f.endswith('obt'):
            p = os.path.join(root, f)
            process = mp.Process(target=tag, args=(p, ))
            # proc_list.append(process)

            try:
                process.start()
            except Exception as e:
                print e