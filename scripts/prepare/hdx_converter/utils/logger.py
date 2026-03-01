# utils/logger.py
import logging
from pathlib import Path
from ..models.config import ConverterConfig

class HDXLogger:
    def __init__(self, config: ConverterConfig):
        self.config = config
        self.logger = logging.getLogger('HDXConverter')
        self.setup_logging()
    
    def setup_logging(self):
        self.logger.setLevel(getattr(logging, self.config.log_level))
        self.logger.handlers.clear()  # Очищаем существующие обработчики
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Файловый обработчик
        log_file = self.config.output_dir / self.config.log_file
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)  # В файл пишем все уровни
        
        # Консольный обработчик - только для ERROR и CRITICAL
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.ERROR)  # В консоль только ERROR и выше
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.propagate = False
    
    def get_logger(self):
        return self.logger
    
    def close(self):
        for handler in self.logger.handlers:
            handler.close()