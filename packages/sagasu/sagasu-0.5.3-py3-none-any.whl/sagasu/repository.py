from pathlib import Path
from typing import List

import pandas as pd

from sagasu.model import Resource, TwitterResource, ScrapboxResource, DummyResource
from sagasu.util import CRAWLER_WORK_DIR


class Repository:
    def load(self) -> List[Resource]:
        raise NotImplementedError("")


class TwitterRepository(Repository):
    def load(self) -> List[TwitterResource]:
        dir_path = Path(f"{CRAWLER_WORK_DIR}/twitter/uri-sentence")
        uri_sentence_dfs = []
        for file in dir_path.iterdir():
            if not file.is_file():
                continue
            df = pd.read_csv(file, sep="\t")
            uri_sentence_dfs.append(df)
        uri_sentence_df = pd.concat(uri_sentence_dfs).reset_index()

        dir_path = Path(f"{CRAWLER_WORK_DIR}/twitter/uri-media")
        uri_media_dfs = []
        for file in dir_path.iterdir():
            if not file.is_file():
                continue
            df = pd.read_csv(file, sep="\t")
            uri_media_dfs.append(df)
        uri_media_df = pd.concat(uri_media_dfs).reset_index()

        df = pd.merge(uri_sentence_df, uri_media_df)
        # media_url1  media_url2  media_url3  media_url4  media_caption1
        resources = [
            TwitterResource(
                uri=r[1].uri,
                sentence=r[1].sentence,
                image_urls=[
                    r[1].media_url1,
                    r[1].media_url2,
                    r[1].media_url3,
                    r[1].media_url4,
                ],
                image_captions=[
                    r[1].media_caption1,
                    r[1].media_caption2,
                    r[1].media_caption3,
                    r[1].media_caption4,
                ],
                source_model=None,
            )
            for r in df.iterrows()
        ]

        return resources


class ScrapboxRepository(Repository):
    def load(self) -> List[ScrapboxResource]:
        dir_path = Path(f"{CRAWLER_WORK_DIR}/scrapbox/uri-sentence")
        uri_sentence_dfs = []
        for file in dir_path.iterdir():
            if not file.is_file():
                continue
            df = pd.read_csv(file, sep="\t")
            uri_sentence_dfs.append(df)
        uri_sentence_df = pd.concat(uri_sentence_dfs).reset_index()

        dir_path = Path(f"{CRAWLER_WORK_DIR}/scrapbox/uri-media")
        uri_media_dfs = []
        for file in dir_path.iterdir():
            if not file.is_file():
                continue
            df = pd.read_csv(file, sep="\t")
            uri_media_dfs.append(df)
        uri_media_df = pd.concat(uri_media_dfs).reset_index()

        df = pd.merge(uri_sentence_df, uri_media_df)
        # media_url1  media_url2  media_url3  media_url4  media_caption1
        resources = [
            ScrapboxResource(
                uri=r[1].uri,
                sentence=r[1].sentence,
                image_urls=[
                    r[1].media_url1,
                    r[1].media_url2,
                    r[1].media_url3,
                    r[1].media_url4,
                ],
                image_captions=[
                    r[1].media_caption1,
                    r[1].media_caption2,
                    r[1].media_caption3,
                    r[1].media_caption4,
                ],
                source_model=None,
            )
            for r in df.iterrows()
        ]

        return resources


class DummyRepository(Repository):
    def load(self) -> List[Resource]:
        return [
            DummyResource(uri="dummy", sentence="dummy", source_model=None),
            DummyResource(
                uri="dummy2", sentence="this is a dummy resource", source_model=None
            ),
        ]
