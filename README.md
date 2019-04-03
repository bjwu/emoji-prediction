## emoji-prediction
emoji prediction given a text using machine learning techniques

#### Usage
You'll need python3 

```bash
$ git clone git@github.com:javierhonduco/emoji-prediction.git
$ cd emoji-prediction
```

* Fetch some tweets
```bash
$ cd fetch
$ script/bootstrap # to install everything
$ # fill in fetch/config.py using config_sample.py as a template
$ # you'll need: * a Twitter API token * a Sentry DSN
$ bin/benchmark # just to download tweets and see how many per second can you fetch
```

* Do some 🔬
```bash
$ cd classify
$ script/bootstrap # to install everything
$ # once the training file is in the folder
$ python3 sk_learn_experiments.py 10000 # use 10.000 tweets. The percentage used for training is defined in the `TRAINING` variable
$ # generate statistics
$ python3 emoji_stats.py
```
