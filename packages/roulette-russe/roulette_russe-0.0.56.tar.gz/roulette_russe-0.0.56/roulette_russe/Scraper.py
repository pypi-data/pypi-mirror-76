import pandas as pd
import boto3
from botocore.exceptions import ClientError
from abc import abstractmethod, ABC
import logging
import os


class Scraper(ABC):
    def __init__(self, input_config: dict, output_datasets: list, roulette_russe=None):
        self.output_datasets = dict()
        for i in range(len(output_datasets)):
            self.output_datasets[output_datasets[i]] = pd.DataFrame()
        self.input_config = input_config
        self.roulette_russe = roulette_russe

    def get_mobile_user_agent(self):
        if self.roulette_russe is None:
            return 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        return self.roulette_russe.getRandomMobileUserAgent()

    def get_laptop_user_agent(self):
        if self.roulette_russe is None:
            return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        return self.roulette_russe.getRandomLaptopUserAgent()

    def get_proxies(self):
        if self.roulette_russe is None:
            return {}
        else:
            return {
                "http": self.roulette_russe.getProxyConnectionString(),
                "https": self.roulette_russe.getProxyConnectionString(),
            }

    @abstractmethod
    def scrap(self):
        pass

    def to_csv(self, path, dataset_index):
        self.output_datasets[dataset_index].to_csv(path, index=False)

    def to_parquet(self, path, dataset_index):
        self.output_datasets[dataset_index].to_parquet(path, index=False)

    @abstractmethod
    def quality_check(self):
        pass

    def to_s3(self, aws_access_key_id: str, aws_secret_access_key: str, bucket_name: str, file_name: str, dataset_index: int):
        local_file_name = file_name.split('/')[len(file_name.split('/'))-1]
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3 = session.client('s3')
        self.to_parquet(local_file_name, dataset_index)
        try:
            s3.upload_file(local_file_name, bucket_name, file_name)
            os.remove(local_file_name)
        except ClientError as e:
            logging.error(e)
            os.remove(local_file_name)
            return False
        return True