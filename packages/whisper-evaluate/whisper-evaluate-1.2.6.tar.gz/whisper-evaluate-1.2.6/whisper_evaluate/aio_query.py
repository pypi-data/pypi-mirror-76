import csv
import json
import aiohttp
import asyncio
import time
from tqdm import tqdm
from whisper_evaluate.utils import logging


class WhisperQuery(object):

    def __init__(self, url: str, source_file: str, target_file: str, semaphore: int = 500):
        """Initial configuration
        url: serving url to request
        source_file: the file of query
        target_file: the file of results
        semaphore: maximum concurrency
        """
        self.url = url
        self.source_file = source_file
        self.target_file = target_file
        self.semaphore = asyncio.Semaphore(semaphore)
        self.results = []

    def query_rows(self):
        with open(self.source_file, 'r', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                yield row

    def run(self):
        start_time = time.time()
        logging.info("Whisper text detection query start.")
        tasks = [asyncio.ensure_future(self.__post(row=row)) for row in self.query_rows()]
        with tqdm(total=len(tasks)) as pbar:
            for task in tasks:
                task.add_done_callback(lambda _: pbar.update(1))
            loop = asyncio.get_event_loop()
            self.results = loop.run_until_complete(asyncio.gather(*tasks))
            loop.close()
        logging.info("Complete stand test query, cost {} seconds.".format(int(time.time() - start_time)))
        logging.info("Start to write target file..")
        self.__save()

    def __save(self):
        with open(self.target_file, 'w', encoding='utf-8') as f:
            w_csv = csv.writer(f)
            w_csv.writerow(["example", "label", "type", "result_json"])
            w_csv.writerows(self.results)

    async def __post(self, row: list) -> list:
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json={"inputs": [row[0]]}) as response:
                    return row + [await response.json()]

