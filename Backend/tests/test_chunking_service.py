import unittest

from app.services.common.chunking_service import chunk_document


class ChunkingServiceTest(unittest.TestCase):
    def test_markdown_heading_is_preserved_as_metadata(self):
        chunks = chunk_document("# 分诊指引\n## 呼吸系统\n咳嗽伴发热建议呼吸科。", "指引.md", "分诊指引")
        self.assertEqual(chunks[0]["metadata"]["source"], "指引.md")
        self.assertEqual(chunks[0]["metadata"]["source_type"], "分诊指引")
        self.assertEqual(chunks[0]["metadata"]["section_title"], "分诊指引 / 呼吸系统")


if __name__ == "__main__":
    unittest.main()
