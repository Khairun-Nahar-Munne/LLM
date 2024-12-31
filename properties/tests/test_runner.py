from django.test.runner import DiscoverRunner

class NoDbTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        """Override database creation"""
        pass

    def teardown_databases(self, old_config, **kwargs):
        """Override database teardown"""
        pass