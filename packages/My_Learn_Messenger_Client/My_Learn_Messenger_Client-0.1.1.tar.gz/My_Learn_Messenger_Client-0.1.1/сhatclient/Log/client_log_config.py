import logging
import os
import sys

sys.path.append('../../')

# создаём формировщик логов (formatter):
client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')

# создаём потоки вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(client_formatter)
steam.setLevel(logging.ERROR)
log_file = logging.FileHandler(path, encoding='utf8')
log_file.setFormatter(client_formatter)

# создаём регистратор и настраиваем его
client_log = logging.getLogger('client_log')
client_log.addHandler(steam)
client_log.addHandler(log_file)
client_log.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    client_log.critical('Test critical event')
    client_log.error('Test error ivent')
    client_log.debug('Test debug ivent')
    client_log.info('Test info ivent')