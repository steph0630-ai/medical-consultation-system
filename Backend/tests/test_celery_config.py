import unittest

from app.core.celery_app import celery_app


class CeleryConfigTest(unittest.TestCase):
    def test_business_and_scheduled_queues_are_registered(self):
        queue_names = {queue.name for queue in celery_app.conf.task_queues}
        self.assertEqual(queue_names, {"celery", "scheduled_tasks"})
        self.assertIn(
            "app.schedule.jobs.payment_callback",
            celery_app.conf.include,
        )
        self.assertIn(
            "app.schedule.jobs.report_interpret",
            celery_app.conf.include,
        )
        self.assertIn(
            "app.schedule.jobs.knowledge_embed",
            celery_app.conf.include,
        )


if __name__ == "__main__":
    unittest.main()
