import unittest

from app.services.backoffice.department import DepartmentService


class DepartmentServiceTest(unittest.TestCase):
    def test_parse_markdown_departments(self):
        content = "前置说明\n## 内科\n常见内科疾病\n\n## 外科\n外科诊疗"
        self.assertEqual(
            DepartmentService.parse_markdown(content),
            [
                {"name": "内科", "description": "常见内科疾病"},
                {"name": "外科", "description": "外科诊疗"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
