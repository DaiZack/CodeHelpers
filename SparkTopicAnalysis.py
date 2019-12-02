import findspark
findspark.init()
from pyspark.sql import SparkSession
import pandas as pd
from pyspark.ml import Pipeline
from pyspark.sql.functions import udf,col
from pyspark.ml.feature import CountVectorizer, IDF, StopWordsRemover, RegexTokenizer
from pyspark.ml.clustering import LDA

spark = SparkSession.builder.getOrCreate()

data = pd.read_csv('https://raw.githubusercontent.com/DaiZack/MLdatasets/master/imdb500.csv')
df = spark.createDataFrame(data)
textCol = 'review'
selfstopwords = ['br']
numOfTopics = 10
numOfKeywords = 5

tokenizer = RegexTokenizer(inputCol=textCol, outputCol='token', pattern='\\W+')
stopwords = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol='clean0')
stopwords1 = StopWordsRemover(inputCol=stopwords.getOutputCol(), stopWords=selfstopwords,outputCol='clean')
cv = CountVectorizer(inputCol=stopwords1.getOutputCol(), outputCol='cv')
idf = IDF(inputCol=cv.getOutputCol(), outputCol='idf')
lda = LDA(featuresCol=idf.getOutputCol(), k=numOfTopics, maxIter=10)

pipe1 = Pipeline(stages=[tokenizer, stopwords,stopwords1,cv,idf, lda])

model = pipe1.fit(df)
output = model.transform(df)

def topicsTerms(vocab, termindices, leng=None):
  if not leng:
    return [voca[t] for t in termindices]
  return [vocab[t] for t in termindices][:leng]

def topicsTerm_udf(vocab, leng=None):
  return udf(lambda x: topicsTerms(vocab,x, leng))

topweights = udf(lambda x: x[:numOfKeywords])

topics = model.stages[-1].describeTopics()
vocab = model.stages[3].vocabulary
topics.withColumn('Terms', topicsTerm_udf(vocab, numOfKeywords)(col('termIndices')))\
  .withColumn('weights', topweights(col('termWeights')) )\
  .select([col('Terms'),col('weights')]).show(truncate=False)

