from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from ier_processor.spark_job import PDFBatch


def init_local_sc():
    spark_conf = SparkConf()
    SparkSession.builder.config(conf=spark_conf)
    spark = SparkSession.builder.master("local").getOrCreate()
    spark_context = spark.sparkContext
    AWS_ACCESS_KEY = 'AKIAYX2DMZI4G6GH3G6I'
    AWS_SECRET_KEY_ID = 'lHKq3Ok2WY2mkeoOPzeFYIokGK026wEjyZJswSP0'
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY)
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_KEY_ID)

    spark_context._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.ap-south-1.amazonaws.com")
    spark_context._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")

    spark_context._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider",
                                      "org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider")
    spark_context.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")
    return spark_context

global_spark_context = init_local_sc()

def test_spark_job():
    test_batch = PDFBatch("Aldona", debug=True)
    #test_batch.install_ier_package(global_spark_context)
    print("extracting file names")
    test_batch.extract_pdf_file_names(global_spark_context)
    print("making pages")
    test_batch.make_pages(global_spark_context)
    print("extracting file names")
    test_batch.extract_page_image_file_names(global_spark_context)
    print("making records")
    test_batch.make_records(global_spark_context, debug=True)
    print("extracting file names")
    test_batch.extract_record_image_file_names(global_spark_context)
    print("making text records")
    test_batch.make_text_records(global_spark_context)
