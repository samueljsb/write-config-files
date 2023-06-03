from __future__ import annotations

from pytest import CaptureFixture

from write_config_files.logging import StdErrColorLogger
from write_config_files.logging import StdErrLogger


class TestStdErrLogger:
    def test_debug(self, capfd: CaptureFixture[str]):
        StdErrLogger().debug('some message')

        captured = capfd.readouterr()
        assert captured.out == ''
        assert captured.err == 'some message\n'

    def test_info(self, capfd: CaptureFixture[str]):
        StdErrLogger().info('some message')

        captured = capfd.readouterr()
        assert captured.out == ''
        assert captured.err == 'some message\n'

    def test_warn(self, capfd: CaptureFixture[str]):
        StdErrLogger().warn('some message')

        captured = capfd.readouterr()
        assert captured.out == ''
        assert captured.err == 'some message\n'


class TestStdErrColorLogger:
    def test_debug(self, capfd: CaptureFixture[str]):
        StdErrColorLogger().debug('some message')

        captured = capfd.readouterr()
        assert captured.out == ''
        assert captured.err == '\033[2msome message\033[0m\n'

    def test_info(self, capfd: CaptureFixture[str]):
        StdErrColorLogger().info('some message')

        captured = capfd.readouterr()
        assert captured.out == ''
        assert captured.err == '\033[0msome message\033[0m\n'

    def test_warn(self, capfd: CaptureFixture[str]):
        StdErrColorLogger().warn('some message')

        captured = capfd.readouterr()
        assert captured.out == ''
        assert captured.err == '\033[93msome message\033[0m\n'
