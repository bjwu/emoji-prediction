from pyspark.ml.feature import Word2Vec
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression

#
spark = SparkSession.builder\
    .master("local") \
    .appName("Word2Vec") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

import math
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from preprocessing import get_tweets
from fetch.config import raw_emojis

##TODO: sentence length

en_stopwords = set(stopwords.words('english'))
snowball_stemmer = SnowballStemmer('english')

emoji_id_mapper = {emoji: id for (id, emoji) in enumerate(raw_emojis)}
id_emoji_mapper = {id: emoji for (id, emoji) in enumerate(raw_emojis)}

def linguistic_preprocess(tweet):
    without_stopwords = [w for w in tweet.split() if w not in en_stopwords]
    stemmed = [snowball_stemmer.stem(w) for w in without_stopwords]
    return ' '.join(stemmed)

def emojis_balanced_dataset(amount=None, lame_limit=5000, lame_min_classes=100):
    emoji_tweet_map = {}
    data = []
    target = []

    for i, single_tweet in enumerate(get_tweets()):
        ### 排除长度大于lame_limit的tweet
        if i >= lame_limit:
            break
        [tweet, emojis, raw_tweet] = single_tweet

        ### emoji与tweet的对应统计
        first_emoji = emojis[0]
        if first_emoji in emoji_tweet_map:
            emoji_tweet_map[first_emoji].append(tweet)
        else:
            emoji_tweet_map[first_emoji] = [tweet]

    emoji_names_in_dataset = emoji_tweet_map.keys()
    emoji_name_count = [(e, len(emoji_tweet_map[e])) for e in emoji_names_in_dataset]

    print(emoji_name_count)

    ### 删掉出现率小的emoji
    for emoji_name, count in emoji_name_count:
        if count < lame_min_classes:
            del emoji_tweet_map[emoji_name]
        else:
            # should probably be random...
            emoji_tweet_map[emoji_name] = emoji_tweet_map[emoji_name][:lame_min_classes]
            # emoji_tweet_map[emoji_name] = emoji_tweet_map[emoji_name]

    for emoji_name, tweets in emoji_tweet_map.items():
        for tweet in tweets:
            data.append(linguistic_preprocess(tweet))
            target.append(emoji_name)

    return [data, None, target]


def predict(text, vectorizer, classifier):
    cleaned = linguistic_preprocess(text)
    vector = vectorizer.transform([cleaned])
    prediction = classifier.predict(vector.toarray())[0]
    emoji_name = id_emoji_mapper[prediction]
    return emoji_name

def learn_with(dataset=None, save=True):
    [data, target_multi, target_single] = dataset

    # 利用word2vec构建词向量， 词向量长度100
    documentDF = spark.createDataFrame([(data[i].split(" "),emoji_id_mapper[target_single[i]]) for i in range(len(data))], ["text", "label"])
    word2Vec = Word2Vec(vectorSize=100, minCount=0, inputCol="text", outputCol="features")
    model = word2Vec.fit(documentDF)
    result = model.transform(documentDF)

    result.select("label", "features").show()

    # train & test data
    (trainingData, testData) = result.randomSplit([0.8, 0.2], seed=100)
    print("Training Dataset Count: " + str(trainingData.count()))
    print("Test Dataset Count: " + str(testData.count()))

    # 建立 LR 模型
    lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
    lrModel = lr.fit(trainingData)
    predictions = lrModel.transform(testData)
    predictions.select("features", "label", "prediction") \
        .show(n=30, truncate=30)

    if save:
        lrModel.save('trained_models/')


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('usage: python sklearn_classifier.py <tweets_number>')
    #     sys.exit(1)

    # MAX_TWEETS = int(sys.argv[1])

    MAX_TWEETS = 80000

    #dataset = emojis_ordered_dataset(MAX_TWEETS)
    dataset = emojis_balanced_dataset(lame_limit=MAX_TWEETS, lame_min_classes=150)

    TRAINING = 0.8
    TRAIN = int(math.floor(MAX_TWEETS * TRAINING))
    print("total_tweets={} total_training={} diff_emojis={}".format(
        MAX_TWEETS,
        TRAIN,
        len(set(dataset[2]))
    ))

    learn_with(dataset=dataset)

