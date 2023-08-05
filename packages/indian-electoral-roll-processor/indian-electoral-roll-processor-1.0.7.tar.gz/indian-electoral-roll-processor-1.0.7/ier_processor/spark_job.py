from datetime import datetime
from ier_processor.pdf_slicing import PDFSlicingMachine
from ier_processor.image_record_processing import ImageProcessor
import boto3
from urllib.parse import urlparse
import re


def strip_starting_slash(s):
    return re.sub('^/*', '', s)


class PDFBatch:

    BUCKET_BASE = "s3a://epicfiles"

    def __init__(self, name="Aldona", debug=True, local_spark=True):
        self.name = name
        self.debug = debug
        date_prefix = datetime.now().strftime('%Y%m%d_%H%M%s_')
        self.prefix = date_prefix if self.debug else ''
        self.local_spark = local_spark

    def proto(self):
        if self.local_spark:
            return 's3a'
        else:
            return 's3'

    @property
    def _pdf_files_all(self):
        return f'{PDFBatch.BUCKET_BASE}/GER_2020/{self.name}/*.pdf'

    @property
    def _pdf_files_sample(self):
        return f'{PDFBatch.BUCKET_BASE}/GER_2020/{self.name}/Part01.pdf'

    @property
    def pdf_files(self):
        if self.debug:
            return self._pdf_files_sample
        else:
            return self._pdf_files_all

    @property
    def pdf_file_names(self):
        return f'{PDFBatch.BUCKET_BASE}/{self.prefix}/pdf_file_names/'

    @property
    def page_images(self):
        return f'{PDFBatch.BUCKET_BASE}/{self.prefix}/page_images/'

    @property
    def page_image_names(self):
        return f'{PDFBatch.BUCKET_BASE}/{self.prefix}/page_image_names/'

    @property
    def record_images(self):
        return f'{PDFBatch.BUCKET_BASE}/{self.prefix}/record_images/'

    @property
    def record_image_names(self):
        return f'{PDFBatch.BUCKET_BASE}/{self.prefix}/record_image_names/'

    @property
    def text_records(self):
        return f'{PDFBatch.BUCKET_BASE}/{self.prefix}/text_records'

    def save_file_names_to(self, src_dir, dest_dir, global_spark_context):
        print(f'extracting file names from {src_dir} to {dest_dir}')

        print(f'deleting {dest_dir}')
        s3 = boto3.resource("s3")
        url_data = urlparse(dest_dir)
        bucket = s3.Bucket(url_data.netloc)
        key = strip_starting_slash(url_data.path)
        bucket.objects.filter(Prefix=key).delete()

        print(f'loading binary files from {src_dir}')
        binary_files = global_spark_context.binaryFiles(f'{src_dir}')
        file_names = binary_files.map(lambda binary_file_tuple: binary_file_tuple[0])
        file_names_count = file_names.count()

        print(f'saving list of {src_dir}::{file_names_count} to {dest_dir}')
        for file_name in file_names.take(100):
            print(f'                          {file_name}')
        file_names.saveAsTextFile(f'{dest_dir}/')
        file_names.unpersist()

    def extract_pdf_file_names(self, global_spark_context):
        try:
            self.save_file_names_to(self.pdf_files, self.pdf_file_names, global_spark_context)
        except Exception as e:
            pass

    def extract_page_image_file_names(self, global_spark_context):
        try:
            self.save_file_names_to(f'{self.page_images}/*/*/*/*/*.png', self.page_image_names, global_spark_context)
        except Exception as e:
            pass

    def extract_record_image_file_names(self, global_spark_context):
        try:
            self.save_file_names_to(f'{self.record_images}/*/*/*/*/*.png', self.record_image_names, global_spark_context)
        except Exception as e:
            pass

    def make_pages(self, global_spark_context):
        pdf_names = global_spark_context.textFile(f'{self.pdf_file_names}/*')
        print(f"                                          saving page images to {self.page_images}")
        limit = 1 if self.debug else None
        page_image_names = pdf_names.flatMap(lambda pdf_file: PDFSlicingMachine().split_whole_pdf_into_pages(pdf_file, self.page_images, limit=limit))
        print(page_image_names.count())
        for page_image in page_image_names.take(100):
            print(f"                {page_image}")

    def make_records(self, global_spark_context):
        page_image_names = global_spark_context.textFile(f'{self.page_image_names}/*')
        image_records = page_image_names.flatMap( lambda pdf_page: PDFSlicingMachine().split_pdf_page_image_into_record_images(pdf_page, self.record_images))
        print(image_records.count())

    def make_text_records(self, global_spark_context):
        record_image_names = global_spark_context.textFile(f'{self.record_image_names}/*')
        text_records = record_image_names.map(lambda record_image: ImageProcessor().process_image(record_image))
        print(f'extracted {text_records.count()} records')
        # text_records is a tuple record_type, record
        print(f'saving text records to {self.text_records}')
        text_records.map(lambda  x: "\t".join(x)).saveAsTextFile(self.text_records)

    def install_ier_package(self, global_spark_context):
        global_spark_context.install_pypi_package("indian-electoral-roll-processor")



