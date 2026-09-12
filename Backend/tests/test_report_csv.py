import unittest

from app.api.backoffice.v1.report import _parse_report_csv


class ReportCsvTest(unittest.TestCase):
    def test_parse_report_csv(self):
        raw = "项目名称,缩写,结果,单位,参考范围,状态,检验结论\n白细胞,WBC,8.2,10^9/L,4-10,正常,未见明显异常\n".encode()
        self.assertEqual(
            _parse_report_csv(raw),
            {
                "items": [
                    {
                        "name": "白细胞",
                        "code": "WBC",
                        "value": "8.2",
                        "unit": "10^9/L",
                        "reference_range": "4-10",
                        "status": "normal",
                    }
                ],
                "conclusion": "未见明显异常",
            },
        )


if __name__ == "__main__":
    unittest.main()
