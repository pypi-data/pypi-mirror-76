import time
from kafka import KafkaConsumer


class KafkaListener:
    def __init__(self, **kwargs):
        """
        :param topic, kafka_ip, kafka_port, group_id
        """
        self.topic, self.kafka_ip, self.kafka_port, self.group_id = kwargs['topic'], kwargs['kafka_ip'], kwargs['kafka_port'], kwargs['group_id']
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers= f'{self.kafka_ip}:{self.kafka_port}', group_id = self.group_id)
        print('succeed in connecting to kafka')


    def connect(self):
        for _ in range(120):
            try:
                consumer = KafkaConsumer(self.topic, bootstrap_servers= f'{self.kafka_ip}:{self.kafka_port}', group_id = self.group_id)
                return consumer
            except BaseException:
                print('connection kafka failed, retrying ...')
                time.sleep(1)
    
    def __iter__(self):
        return self.consumer