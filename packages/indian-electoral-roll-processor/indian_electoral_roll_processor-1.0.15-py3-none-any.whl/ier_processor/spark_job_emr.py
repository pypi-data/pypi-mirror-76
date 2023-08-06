import sys
from pyspark import SparkContext, SparkConf
from ier_processor.spark_job import PDFBatch

params = sys.argv
print("receive params", "\n".join(params))
batch = params[1] if len(params) > 1 else "Aldona"
action = params[2] if len(params) > 2 else "all"
debug = params[3] == 'True' if len(params) > 3 else True


# m5.xlarge has 4 vcps
# we have 5+ 1 instances
# cores is 20 = 5 * 4
print(f"batch:{batch} debug:{debug}")
#conf = SparkConf()
#conf.set("spark.executor.instances", 6)
#conf.set("spark.executor.cores", 2)
#conf.setAppName(f"PDFProcessing {batch}")

#sc = SparkContext(conf)
sc = SparkContext(appName=f"PDF Splitter debug:{debug}")
test_batch = PDFBatch(batch, debug=debug)


if action in ['all', 'extract_pdf_file_names']:
    print("extract_pdf_file_names")
    test_batch.extract_pdf_file_names(sc)
if action in ['all', 'make_pages']:
    print("make_pages")
    test_batch.make_pages(sc)
if action in ['all', 'extract_page_image_file_names']:
    print("extract_page_image_file_names")
    test_batch.extract_page_image_file_names(sc)
if action in ['all', 'make_records']:
    print("make_records")
    test_batch.make_records(sc)
if action in ['all', 'extract_record_image_file_names']:
    print("extract_record_image_file_names")
    test_batch.extract_record_image_file_names(sc)
if action in ['all', 'make_text_records']:
    print("make_text_records")
    test_batch.make_text_records(sc)
# separate section, and assembly from others

