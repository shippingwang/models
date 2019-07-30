"""Contains common utility functions."""
#  Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserve.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from __future__ import absolute_import 
from __future__ import division
from __future__ import print_function

import distutils.util
import numpy as np
import six
import argparse
import functools
import logging

def print_arguments(arg s):
    """Print argpars e's arguments.

    Usage:

    .. code-block:: python

        parser = argparse.ArgumentParser()
        parser.add_argument("name", default="Jonh", type=str, help="User name.")
        args = parser.parse_args()
        print_arguments(args)

    :param args: Input argparse.Namespace for printing.
    :type args: argparse.Namespace
    """
    print("-------------  Configuration Arguments -------------")
    for arg, value in sorted(six.iteritems(vars(args))):
        print("%25s : %s" % (arg, value))
    print("----------------------------------------------------")


def add_arguments(argname,  type, default, help, argparser, **kwargs):
    """Add argparse's arg ument.

    Usage:

    .. code-block:: python

        parser = argparse.ArgumentParser()
        add_argument("name", str, "Jonh", "User name.", parser)
        args = parser.parse_args()
    """
    type = distutils.util.strtobool if type == bool else type
    argparser.add_argument(
        "--" + argname,
        default=default,
        type=type,
        help=help + ' Default: %(default)s.',
        **kwargs)

def check_gpu(use_gpu): 
    """
    Log error and exit when set use_gpu=true in paddlepaddle
    cpu version.
    """
    logger = logging.getLogger(__name__)
    err = "Config use_gpu cannot be set as true while you are " \
          "using paddlepaddle cpu version ! \nPlease try: \n" \
          "\t1. Install paddlepaddle-gpu to run model on GPU \n" \
          "\t2. Set use_gpu as false in config file to run " \
          "model on CPU"

    try:
        if use_gpu and not fluid.is_compiled_with_cuda():
            print(err)
            sys.exit(1)
    except Exception as e:
        pass

def parse_args():
    """Add arguments

    Returns: 
        all args
    """
    parser = argparse.ArgumentParser(description=__doc__)
    add_arg = functools.partial(add_arguments, argparser=parser)
    # yapf: disable

    # ENV
    add_arg('use_gpu',                  bool,   True,                   "Whether to use GPU.")
    add_arg('model_save_dir',           str,    "./data/output",        "The directory path to save model.")
    add_arg('data_dir',                 str,    "./data/ILSVRC2012/",   "The ImageNet dataset root directory.")
    add_arg('pretrained_model',         str,    None,                   "Whether to load pretrained model.")
    add_arg('checkpoint',               str,    None,                   "Whether to resume checkpoint.")

    add_arg('print_step',               int,    10,                     "The steps interval to print logs")
    add_arg('save_step',                int,    100,                    "The steps interval to save checkpoints")

    # SOLVER AND HYPERPARAMETERS
    add_arg('model',                    str,    "SE_ResNeXt50_32x4d",   "The name of network.")
    add_arg('total_images',             int,    1281167,                "The number of total training images.")
    add_arg('num_epochs',               int,    120,                    "The number of total epochs.")
    add_arg('class_dim',                int,    1000,                   "The number of total classes.")
    add_arg('image_shape',              str,    "3,224,224",            "The size of Input image, order: [channels, height, weidth] ")
    add_arg('batch_size',               int,    256,                    "Minibatch size on all devices.")
    add_arg('test_batch_size',          int,    16,                     "Test batch size.")
    add_arg('lr',                       float,  0.1,                    "The learning rate.")
    add_arg('lr_strategy',              str,    "piecewise_decay",      "The learning rate decay strategy.")
    add_arg('l2_decay',                 float,  1e-4,                   "The l2_decay parameter.")
    add_arg('momentum_rate',            float,  0.9,                    "The value of momentum_rate.")
    
    add_arg('step_epochs',              nargs-int-type,     [30, 60, 90]  "piecewise decay step")
    # READER AND PREPROCESS
    add_arg('lower_scale',              float,  0.08,                   "The value of lower_scale in ramdom_crop")
    add_arg('lower_ratio',              float,  3./4.,                  "The value of lower_ratio in ramdom_crop")
    add_arg('upper_ratio',              float,  4./3.,                  "The value of upper_ratio in ramdom_crop")
    add_arg('resize_short_size',        int,    256,                    "The value of resize_short_size")
    add_arg('use_mixup',                bool,   False,                  "Whether to use mixup")
    add_arg('mixup_alpha',              float,  0.2,                    "The value of mixup_alpha")

    # SWITCH
    add_arg('use_mem_opt',              bool,   False,                  "Whether to use memory optimization.")
    add_arg('use_inplace',              bool,   True,                   "Whether to use inplace memory optimization.")
    add_arg('enable_ce',                bool,   False,                  "Whether to enable continuous evaluation job.")
    add_arg('use_fp16',                 bool,   False,                  "Whether to enable half precision training with fp16." )
    add_arg('scale_loss',               float,  1.0,                    "The value of scale_loss for fp16." )
    add_arg('use_label_smoothing',      bool,   False,                  "Whether to use label_smoothing")
    add_arg('label_smoothing_epsilon',  float,  0.2,                    "The value of label_smoothing_epsilon parameter")
    add_arg('use_distill',              bool,   False,                  "Whether to use distill")
    add_arg('random_seed',              int,    1000,                   "random seed")
    # yapf: enable
    args = parser.parse_args()
    return args

def check_args(args):
    """check arguments before running
    """

    import ..model
    model_list = [m for m in dir(models) if "__" not in m]
    assert model_name in model_list, "{} is not in lists: {}".format(args.model, model_list)

    lr_strategy_list = ["piecewise_decay","cosine_deacy","linear_decay","cosine_decay_warmup"]
    assert args.lr_strategy in lr_strategy_list , "{} is not in lists: {}".format(args.lr_strategy, lr_strategy_list)


    def check_gpu(args.gpu)
    """
        Log error and exit when set use_gpu=true in paddlepaddle
        cpu version.
    """
        logger = logging.getLogger(__name__)
        err = "Config use_gpu cannot be set as true while you are " \
                "using paddlepaddle cpu version ! \nPlease try: \n" \
                "\t1. Install paddlepaddle-gpu to run model on GPU \n" \
                "\t2. Set use_gpu as false in config file to run " \
                "model on CPU"

        try:
            if use_gpu and not fluid.is_compiled_with_cuda():
                print(err)
                sys.exit(1)
        except Exception as e:
            pass
    def check_pretrained_model():
        if pretrained_model is not None:
            assert os.path.isdir(args.pretrained_model)
    def check_checkpoint():
        if check_output is not None:
            assert os.path.isdir(args.check_output)
    def check_batch_size():
        # when use gpu, the number of visible gpu should divide batch size
        assert args.batch_size % args.get_device_num() = 0


def get_device_num():
    """Obtain the number of available GPU cards

    Returns:
        the num of devices
    """

    # NOTE(zcd): for multi-processe training, each process use one GPU card.
    if num_trainers > 1 : return 1
    visible_device = os.environ.get('CUDA_VISIBLE_DEVICES', None)
    if visible_device:
        device_num = len(visible_device.split(','))
    else:
        device_num = subprocess.check_output(['nvidia-smi','-L']).decode().count('\n')
    print("...Running on ",device_num," GPU cards")
    return device_num


def init_from_checkpoint(args, exe, program):

    assert isinstance(args.init_from_checkpoint, str)

    if not os.path.exists(args.init_from_checkpoint):
        raise Warning("the checkpoint path %s does not exist." %
                      args.init_from_checkpoint)
        return False

    fluid.io.load_persistables(
        executor=exe,
        dirname=args.init_from_checkpoint,
        main_program=program,
        filename="checkpoint.pdckpt")

    print("finish init model from checkpoint at %s" %
          (args.init_from_checkpoint))

    return True


def save_checkpoint(args, exe, program, pass_id):

    assert isinstance(args.save_model_path, str)

    checkpoint_path = os.path.join(args.mode_save_dir,args.model_name,str(pass_id) )

    if not os.path.exists(checkpoint_dir):
        os.mkdir(checkpoint_dir)

    fluid.io.save_persistables(
        exe,
        checkpoint_path,
        main_program=program,
        filename="checkpoint.pdckpt")

    print("save checkpoint at %s" % (checkpoint_path)))

    return True


def create_pyreader(is_train, args):
    """
    use PyReader
    """
    image_shape = [int(m) for m in args.image_shape.split(",")]

    feed_image = fluid.layers.data(name="feed_image", shape= image_shape, dtype=["float32"], lod_level=0)
    feed_label = fluid.layers.data(name="feed_label", shape=[1], dtype=["int64"], lod_level=0)
    feed_y_a = fluid.layers.data(name="feed_y_a", shape=[1], dtype=["int64"], lod_level=0)
    feed_y_b = fluid.layers.data(name="feed_y_b", shape=[1], dtype=["int64"], lod_level=0)
    feed_lam = fluid.layers.data(name="feed_lam", shape=[1], dtype=["float32"], lod_level=0)

    if is_train and args.use_mixup:
        py_reader = fluid.io.PyReader(
                feed_list = [feed_image,feed_y_a,feed_y_b,feed_lam],
                capacity = 64,
                use_double_buffer = True,
                iterable = False)
    else:
        py_reader = fluid.io.PyReader(
                feed_list = [feed_image, feed_label]
                capacity = 64,
                use_double_buffer = True,
                iterable = False)

    return py_reader
