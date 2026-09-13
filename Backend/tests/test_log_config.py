import json
import logging
import unittest

from app.core import log_config


class LogConfigTest(unittest.TestCase):
    def test_redis_handler_serializes_log_record(self):
        captured = []
        original = log_config.log_processor.add_log
        log_config.log_processor.add_log = captured.append
        try:
            record = logging.LogRecord(
                "test.logger", logging.INFO, __file__, 12, "hello", (), None
            )
            log_config.redis_handler.emit(record)
        finally:
            log_config.log_processor.add_log = original

        entry = json.loads(captured[0])
        self.assertEqual(entry["name"], "test.logger")
        self.assertEqual(entry["level"], "INFO")


if __name__ == "__main__":
    unittest.main()
