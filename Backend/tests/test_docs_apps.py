import unittest

from app.configs.docs_apps import create_backoffice_app, create_client_app


class DocsAppsTest(unittest.TestCase):
    def test_openapi_documents_keep_route_scopes_separate(self):
        client_schema = create_client_app().openapi()
        backoffice_schema = create_backoffice_app().openapi()

        self.assertFalse(
            any("/backoffice/" in path for path in client_schema["paths"])
        )
        self.assertTrue(
            all("/backoffice/" in path for path in backoffice_schema["paths"])
        )
        self.assertIn(
            "BearerAuth",
            backoffice_schema["components"]["securitySchemes"],
        )


if __name__ == "__main__":
    unittest.main()
