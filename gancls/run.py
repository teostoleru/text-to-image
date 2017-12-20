import os
import numpy as np

from gancls.model import GanCls
from gancls.trainer import GanClsTrainer
from gancls.visualizer import GanClsVisualizer
from gancls.utils import pp, show_all_variables
from preprocess.dataset import TextDataset

import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_integer('epoch', 600, 'Epoch to train [600]')
flags.DEFINE_float('learning_rate', 0.0002, 'Learning rate of for adam [0.0002]')
flags.DEFINE_float('beta1', 0.5, 'Momentum term of adam [0.5]')
flags.DEFINE_integer('train_size', np.inf, 'The size of train images [np.inf]')
flags.DEFINE_integer('batch_size', 64, 'The size of batch images [64]')
flags.DEFINE_integer('output_size', 64, 'The size of the output images to produce [64]')
flags.DEFINE_integer('sample_num', 64, 'Number of samples to generate [64]')
flags.DEFINE_string('dataset', 'flowers', 'The name of dataset [celebA, mnist, lsun]')
flags.DEFINE_string('checkpoint_dir', 'checkpoint', 'Directory name to save the checkpoints [checkpoint]')
flags.DEFINE_string('sample_dir', 'samples', 'Directory name to save the image samples [samples]')
flags.DEFINE_string('test_dir', 'visualisation', 'Directory name to save the image samples [visualisation]')
flags.DEFINE_boolean('train', False, 'True for training, False for testing [False]')
flags.DEFINE_string('logs_dir', '/tmp/logs', 'Directory where the tensorboard logs are saved [tmp/logs]')
FLAGS = flags.FLAGS


def main(_):
    pp.pprint(flags.FLAGS.__flags)

    if not os.path.exists(FLAGS.checkpoint_dir):
        os.makedirs(FLAGS.checkpoint_dir)
    if not os.path.exists(FLAGS.sample_dir):
        os.makedirs(FLAGS.sample_dir)
    if not os.path.exists(FLAGS.logs_dir):
        os.makedirs(FLAGS.logs_gir)

    run_config = tf.ConfigProto()
    run_config.gpu_options.allow_growth = True

    datadir = './data/%s' % FLAGS.dataset
    embedding_type = 'cnn-rnn'
    dataset = TextDataset(datadir, embedding_type, 1)

    filename_test = '%s/test' % datadir
    dataset._test = dataset.get_data(filename_test)

    filename_train = '%s/train' % datadir
    dataset.train = dataset.get_data(filename_train)

    with tf.Session(config=run_config) as sess:
        gancls = GanCls(
                dataset=dataset,
                output_size=FLAGS.output_size,
                batch_size=FLAGS.batch_size,
                sample_num=FLAGS.sample_num,
            )

        show_all_variables()

        if FLAGS.train:
            gancls_trainer = GanClsTrainer(
                sess=sess,
                model=gancls,
                dataset=dataset,
                config=FLAGS,
            )
            gancls_trainer.train()
        else:
            gancls_visualiser = GanClsVisualizer(
                sess=sess,
                model=gancls,
                dataset=dataset,
                config=FLAGS,
            )
            gancls_visualiser.visualize()


if __name__ == '__main__':
    tf.app.run()
