import vaex
import boto3
from botocore.exceptions import ClientError
from abc import abstractmethod, ABC
import logging


class Scraper(ABC):
    def __init__(self, input_config: dict, output_datasets_columns: list, roulette_russe=None):
        output_dicts = []
        self.output_datasets = []
        for i in range(len(output_datasets_columns)):
            output_dicts.append(dict())
            for column in output_datasets_columns[i]:
                output_dicts[i][column] = []
            self.output_datasets.append(vaex.from_dict(output_dicts[i]))
        self.input_config = input_config
        self.roulette_russe = roulette_russe

    @abstractmethod
    def scrap(self):
        pass

    def to_csv(self, path, dataset_index):
        self.output_datasets[dataset_index].export_csv(path=path)

    def to_parquet(self, path, dataset_index):
        self.output_datasets[dataset_index].export_parquet(path=path)

    @abstractmethod
    def quality_check(self):
        pass

    def to_s3(self, aws_access_key_id: str, aws_secret_access_key: str, bucket_name: str, file_name: str, dataset_index: int):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3 = session.client('s3')
        self.to_parquet(file_name, dataset_index)
        try:
            s3.upload_file(file_name, bucket_name, file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True