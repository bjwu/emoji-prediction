from sklearn_experiments import emoji_id_mapper, id_emoji_mapper, linguistic_preprocess
import pickle

if __name__ == '__main__':

    with open('trained_models/vectorizer', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('trained_models/SGDClassifier', 'rb') as g:
        sgd = pickle.load(g)

    while True:
        words = input().strip()

        x = vectorizer.transform([words])
        print(id_emoji_mapper[sgd.predict(x)[0]])