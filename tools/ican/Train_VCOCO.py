# --------------------------------------------------------
# Tensorflow iCAN
# Licensed under The MIT License [see LICENSE for details]
# Written by Chen Gao, based on code from Zheqi he and Xinlei Chen
# --------------------------------------------------------


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths
import tensorflow as tf
import numpy as np
import argparse
import pickle
import ipdb


from ult.config import cfg
from models.train_Solver_VCOCO import train_net

def parse_args():
    parser = argparse.ArgumentParser(description='Train an iCAN on VCOCO')
    parser.add_argument('--num_iteration', dest='max_iters',
            help='Number of iterations to perform',
            default=300000, type=int)
    parser.add_argument('--model', dest='model',
            help='Select model',
            default='iCAN_ResNet50_VCOCO', type=str)
    parser.add_argument('--Restore_flag', dest='Restore_flag',
            help='Number of Res5 blocks',
            default=5, type=int)
    parser.add_argument('--Pos_augment', dest='Pos_augment',
            help='Number of augmented detection for each one. (By jittering the object detections)',
            default=15, type=int)
    parser.add_argument('--Neg_select', dest='Neg_select',
            help='Number of Negative example selected for each image',
            default=30, type=int)
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()

    Trainval_GT       = pickle.load( open( cfg.DATA_DIR + '/' + 'Trainval_GT_VCOCO.pkl', "rb" ) )
    Trainval_N        = pickle.load( open( cfg.DATA_DIR + '/' + 'Trainval_Neg_VCOCO.pkl', "rb" ) ) 

    np.random.seed(cfg.RNG_SEED)
    weight    = cfg.ROOT_DIR + '/Weights/res50_faster_rcnn_iter_1190000.ckpt'

    # output directory where the logs are saved
    tb_dir     = cfg.ROOT_DIR + '/logs/' + args.model + '/'

    # output directory where the models are saved
    output_dir = cfg.ROOT_DIR + '/Weights/' + args.model + '/'

    if args.model == 'iCAN_ResNet50_VCOCO':
        from networks.iCAN_ResNet50_VCOCO import ResNet50
        iCAN_Early_flag = 0
    if args.model == 'iCAN_ResNet50_VCOCO_Early':
        from networks.iCAN_ResNet50_VCOCO_Early import ResNet50
        iCAN_Early_flag = 1

    net = ResNet50()
    

    train_net(net, Trainval_GT, Trainval_N, output_dir, tb_dir, args.Pos_augment, args.Neg_select, iCAN_Early_flag, args.Restore_flag, weight, max_iters=args.max_iters)
