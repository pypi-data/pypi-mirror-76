"""
Author      : Moshik Hershcovitch
Author      : David Ohana, Moshik Hershcovitch, Eran Raichstein
Author_email: david.ohana@ibm.com, moshikh@il.ibm.com, eranra@il.ibm.com
License     : MIT
"""

import kafka

from drain3.persistence_handler import PersistenceHandler


class KafkaPersistence(PersistenceHandler):
    def __init__(self, server_list, topic, snapshot_poll_timeout_sec=60):
        self.server_list = server_list
        self.topic = topic
        self.producer = kafka.KafkaProducer(bootstrap_servers=server_list)
        self.snapshot_poll_timeout_sec = snapshot_poll_timeout_sec

    def save_state(self, state):
        self.producer.send(self.topic, value=state)

    def load_state(self):
        consumer = kafka.KafkaConsumer(bootstrap_servers=self.server_list)
        partition = kafka.TopicPartition(self.topic, 0)
        consumer.assign([partition])
        end_offsets = consumer.end_offsets([partition])
        end_offset = list(end_offsets.values())[0]
        if end_offset > 0:
            consumer.seek(partition, end_offset - 1)
            snapshot_poll_timeout_ms = self.snapshot_poll_timeout_sec * 1000
            records = consumer.poll(snapshot_poll_timeout_ms)
            if not records:
                raise RuntimeError(f"No message received from Kafka during restore even though end_offset>0")
            last_msg = records[partition][0]
            state = last_msg.value
        else:
            state = None

        consumer.close()
        return state
