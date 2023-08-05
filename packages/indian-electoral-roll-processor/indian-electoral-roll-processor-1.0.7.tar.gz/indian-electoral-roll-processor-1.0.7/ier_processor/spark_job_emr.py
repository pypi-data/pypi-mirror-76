from pyspark import SparkContext
import sys
if __name__ == "__main__":
    sc = SparkContext(appName="WordCount")
    text_file = sc.textFile(sys.argv[1])
    counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    counts.saveAsTextFile(sys.argv[2])
    sc.stop()


