import sys
from pyspark import SparkContext
from ier_processor.spark_job import PDFBatch

params = sys.argv
print("receive params", "\n".join(params))
batch = params[1]
sc = SparkContext(appName=f"PDFProcessing {batch}")

test_batch = PDFBatch(batch, debug=True)
test_batch.extract_pdf_file_names(sc)
test_batch.make_pages(sc)
test_batch.extract_page_image_file_names(sc)
test_batch.make_records(sc)
test_batch.extract_record_image_file_names(sc)
test_batch.make_text_records(sc)
# separate section, and assembly from others

