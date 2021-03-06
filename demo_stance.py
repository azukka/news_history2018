# coding: utf-8

import argparse
import logging

import numpy as np
from keras import preprocessing
from keras.models import load_model as load_keras_model

from helpers import load_model, get_number

if __name__ == '__main__':
    # Настраиваем логирование:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('--modelfile', help='Обученная модель', required=True)
    arg('--embeddings', help='Дистрибутивная модель', required=True)
    args = parser.parse_args()

    model_filename = args.modelfile
    embeddings_file = args.embeddings

    logger.info('Загружаем дистрибутивную модель...')
    emb_model = load_model(embeddings_file)
    logger.info('Загрузка дистрибутивной модели завершена')
    vocabulary = emb_model.vocab
    embedding_layer = emb_model.get_keras_embedding()

    classes = ['0', '1', '2']

    max_seq_length = 20  # Паддинг: приводим все документы к этой длине (лишнее обрезаем, недостающее заполняем нулями)

    # Загрузка модели
    print('Загрузка готовой модели')
    model = load_keras_model(model_filename)
    print(model.summary())

    while True:
        text = input('Введите ваш текст: ')
        x = [[get_number(w, vocab=vocabulary) for w in text.split()]]
        vectorized = preprocessing.sequence.pad_sequences(
            x, maxlen=max_seq_length, truncating='post', padding='post')
        pred = model.predict(vectorized)
        print(pred)
        cl = [classes[np.argmax(pred)] for pr in pred]
        print(cl)

