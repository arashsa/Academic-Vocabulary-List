import sys
import os
import multiprocessing as mp


def tag(path):
    print path
    os.system('cd /corpora/bokm/tools/The-Oslo-Bergen-Tagger/ && ./tag-bm.sh ' + path + ' > ' + path + '.obt')
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