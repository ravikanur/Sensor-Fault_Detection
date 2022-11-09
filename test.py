from sensor.logger import logging
from dataclasses import dataclass

@dataclass
class Test:
    logging.info('sample message')
    height: int
    name: str = 'Ravi'
    age: int = 0
    

if __name__ == "__main__":
    test = Test(20)
    logging.info(test.name)