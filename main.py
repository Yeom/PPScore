#-*- coding:utf-8 -*-
import argparse
import json
import glob
import os

import PPScore

def main(args):
    config = json.loads(open(args.config, 'r').read())
    fileList = glob.glob(os.path.join(config['data']['path'], '*.%s' % config['data']['extension']))
    module = PPScore.PPScore(config)
    for file in fileList:
        module.Exec(file)
    module.fo.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='input config.ini path')
    args = parser.parse_args()
    main(args)
