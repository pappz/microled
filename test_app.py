from unittest import TestCase
import app


class TestApp(TestCase):
    def test_push(self):
        app.on_wake_up()
        pass
