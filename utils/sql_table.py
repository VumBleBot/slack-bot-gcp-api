import logging
from logging import Logger

import sqlalchemy
from sqlalchemy import VARCHAR, Column, Float, Integer, MetaData, String, Table
from sqlalchemy.engine import Engine


class SQLAlchemyVumblebotStore:
    default_input_table_name: str = "user_input"
    default_feedback_table_name: str = "user_feedback"

    engine: Engine
    metadata: MetaData

    @classmethod
    def build_user_input_table(cls, metadata: MetaData, table_name: str) -> Table:
        return sqlalchemy.Table(
            table_name,
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("team_id", VARCHAR(15), nullable=False),
            Column("channel_id", VARCHAR(15)),  # DM
            Column("user_id", VARCHAR(15), nullable=False),
            Column("user_score", Float, nullable=False),
            Column("user_label", VARCHAR(15), nullable=False),
            Column("event_ts", VARCHAR(20), nullable=False),
            Column("user_input", VARCHAR(1000), nullable=False),
            Column("md_contents", VARCHAR(300), nullable=False),
        )

    @classmethod
    def build_user_feedback_table(cls, metadata: MetaData, table_name: str) -> Table:
        return sqlalchemy.Table(
            table_name,
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("user_id", String(30), nullable=False),
            Column("thread_ts", VARCHAR(20), nullable=False),
            Column("list_idx", Integer, nullable=False),
            Column("type", Integer, nullable=False),
        )

    def __init__(
        self,
        engine: Engine,
        logger: Logger = logging.getLogger(__name__),
        input_table_name: str = default_input_table_name,
        feedback_table_name: str = default_feedback_table_name,
    ):

        self._logger = logger
        self.metadata = sqlalchemy.MetaData()
        self.user_input = self.build_user_input_table(
            metadata=self.metadata, table_name=input_table_name
        )
        self.user_feedback = self.build_user_feedback_table(
            metadata=self.metadata, table_name=feedback_table_name
        )

        self.engine = engine

    @property
    def logger(self) -> Logger:
        if self._logger is None:
            self._logger = logging.getLogger(__name__)
        return self._logger

    def create_tables(self):
        self.metadata.create_all(self.engine, tables=None, checkfirst=True)

    def save_user_input(self, user):
        record = {
            "team_id": user.team_id,
            "channel_id": user.channel,
            "user_id": user.user_id,
            "user_score": user.score,
            "user_label": user.emotion,
            "event_ts": user.event_ts,
            "user_input": user.input,
            "md_contents": ",".join(
                [
                    f"{content['artist']},{content['song_name']}"
                    for content in user.contents[:5]
                ]
            ),
        }

        try:
            with self.engine.begin() as conn:
                conn.execute(self.user_input.insert(), record)
        except Exception as e:
            message = f"Failed to insert user_input, record: {record} error: {e}"
            self.logger.warning(message)

    def _parsing_list_idx(self, body):
        reco_idx = 8
        block_id = body["message"]["blocks"][reco_idx]["block_id"]

        selected_value = body["state"]["values"][block_id]["reco_static_select"][
            "selected_option"
        ]["value"]

        for idx, content in enumerate(
            body["message"]["blocks"][reco_idx]["accessory"]["options"]
        ):
            if selected_value == content["value"]:
                return idx

    def save_user_feedback(self, body: dict, typ: int):
        list_idx = self._parsing_list_idx(body)
        record = {
            "user_id": body["user"]["id"],
            "thread_ts": body["message"]["thread_ts"],
            "list_idx": list_idx,
            "type": typ,
        }

        try:
            with self.engine.begin() as conn:
                conn.execute(self.user_feedback.insert(), record)
        except Exception as e:
            message = f"Failed to insert user_feedback, Error: {e}"
            self.logger.warning(message)

    def init_tables(self):
        if self.user_input.exists(self.engine):
            self.user_input.drop(self.engine)

        if self.user_feedback.exists(self.engine):
            self.user_feedback.drop(self.engine)

        self.metadata.create_all(self.engine, tables=None, checkfirst=True)
