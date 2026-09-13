import unittest

from app.services.common.thread_pool import ThreadPoolService


class ThreadPoolServiceTest(unittest.TestCase):
    def test_shutdown_releases_executor(self):
        service = ThreadPoolService(max_workers=1)
        self.assertEqual(service.get_executor().submit(lambda: 1).result(), 1)
        service.shutdown()
        with self.assertRaises(RuntimeError):
            service.get_executor().submit(lambda: 2)


if __name__ == "__main__":
    unittest.main()
