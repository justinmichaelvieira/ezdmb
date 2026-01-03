"""
LoggingUtility_test.py
Tests for the LoggingUtility module
"""
import os
import logging
import tempfile
# import pytest
from unittest.mock import patch, MagicMock
from ezdmb.Controller.LoggingUtility import setupLogging


class TestSetupLogging:
    """Tests for setupLogging function"""

    def test_setup_logging_creates_file_handler(self):
        """Test that setupLogging creates a file handler"""
        with tempfile.TemporaryDirectory():
            with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler') as mock_file_handler:
                with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler'):
                    with patch('builtins.open', create=True):
                        # Call setupLogging
                        mock_logger = MagicMock()
                        with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                            setupLogging()

                            # Verify FileHandler was called
                            mock_file_handler.assert_called_once()

    def test_setup_logging_creates_stream_handler(self):
        """Test that setupLogging creates a stream handler for console output"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler'):
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler') as mock_stream_handler:
                mock_logger = MagicMock()
                with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                    setupLogging()

                    # Verify StreamHandler was called
                    mock_stream_handler.assert_called_once()

    def test_setup_logging_sets_debug_level_on_logger(self):
        """Test that setupLogging sets DEBUG level on main logger"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler'):
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler'):
                mock_logger = MagicMock()
                with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                    setupLogging()

                    # Verify setLevel was called with DEBUG
                    mock_logger.setLevel.assert_called_once_with(logging.DEBUG)

    def test_setup_logging_sets_debug_level_on_file_handler(self):
        """Test that setupLogging sets DEBUG level on file handler"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler') as mock_file_handler_class:
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler'):
                mock_file_handler = MagicMock()
                mock_file_handler_class.return_value = mock_file_handler

                mock_logger = MagicMock()
                with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                    setupLogging()

                    # Verify file handler setLevel was called with DEBUG
                    mock_file_handler.setLevel.assert_called_once_with(logging.DEBUG)

    def test_setup_logging_sets_debug_level_on_stream_handler(self):
        """Test that setupLogging sets DEBUG level on stream handler"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler'):
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler') as mock_stream_handler_class:
                mock_stream_handler = MagicMock()
                mock_stream_handler_class.return_value = mock_stream_handler

                mock_logger = MagicMock()
                with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                    setupLogging()

                    # Verify stream handler setLevel was called with DEBUG
                    mock_stream_handler.setLevel.assert_called_once_with(logging.DEBUG)

    def test_setup_logging_creates_formatter(self):
        """Test that setupLogging creates a formatter"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler'):
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler'):
                with patch('ezdmb.Controller.LoggingUtility.logging.Formatter') as mock_formatter:
                    mock_logger = MagicMock()
                    with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                        setupLogging()

                        # Verify Formatter was called
                        mock_formatter.assert_called_once()
                        # Check that format string includes expected components
                        formatter_call = mock_formatter.call_args[0][0]
                        assert "%(asctime)s" in formatter_call
                        assert "%(levelname)s" in formatter_call
                        assert "%(message)s" in formatter_call

    def test_setup_logging_sets_formatter_on_file_handler(self):
        """Test that setupLogging sets formatter on file handler"""
        mock_formatter = MagicMock()

        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler') as mock_file_handler_class:
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler'):
                with patch('ezdmb.Controller.LoggingUtility.logging.Formatter', return_value=mock_formatter):
                    mock_file_handler = MagicMock()
                    mock_file_handler_class.return_value = mock_file_handler

                    mock_logger = MagicMock()
                    with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                        setupLogging()

                        # Verify setFormatter was called on file handler
                        mock_file_handler.setFormatter.assert_called_once_with(mock_formatter)

    def test_setup_logging_sets_formatter_on_stream_handler(self):
        """Test that setupLogging sets formatter on stream handler"""
        mock_formatter = MagicMock()

        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler'):
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler') as mock_stream_handler_class:
                with patch('ezdmb.Controller.LoggingUtility.logging.Formatter', return_value=mock_formatter):
                    mock_stream_handler = MagicMock()
                    mock_stream_handler_class.return_value = mock_stream_handler

                    mock_logger = MagicMock()
                    with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                        setupLogging()

                        # Verify setFormatter was called on stream handler
                        mock_stream_handler.setFormatter.assert_called_once_with(mock_formatter)

    def test_setup_logging_adds_file_handler_to_logger(self):
        """Test that setupLogging adds file handler to logger"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler') as mock_file_handler_class:
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler'):
                with patch('ezdmb.Controller.LoggingUtility.logging.Formatter'):
                    mock_file_handler = MagicMock()
                    mock_file_handler_class.return_value = mock_file_handler

                    mock_logger = MagicMock()
                    with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                        setupLogging()

                        # Verify addHandler was called with file handler
                        assert mock_logger.addHandler.call_count >= 1
                        calls = mock_logger.addHandler.call_args_list
                        assert any(call[0][0] == mock_file_handler for call in calls)

    def test_setup_logging_adds_stream_handler_to_logger(self):
        """Test that setupLogging adds stream handler to logger"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler'):
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler') as mock_stream_handler_class:
                with patch('ezdmb.Controller.LoggingUtility.logging.Formatter'):
                    mock_stream_handler = MagicMock()
                    mock_stream_handler_class.return_value = mock_stream_handler

                    mock_logger = MagicMock()
                    with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                        setupLogging()

                        # Verify addHandler was called with stream handler
                        assert mock_logger.addHandler.call_count >= 1
                        calls = mock_logger.addHandler.call_args_list
                        assert any(call[0][0] == mock_stream_handler for call in calls)

    def test_setup_logging_idempotent(self):
        """Test that setupLogging can be called multiple times safely"""
        with patch('ezdmb.Controller.LoggingUtility.logging.FileHandler'):
            with patch('ezdmb.Controller.LoggingUtility.logging.StreamHandler'):
                mock_logger = MagicMock()
                with patch('ezdmb.Controller.LoggingUtility.logger', mock_logger):
                    # Call setupLogging multiple times
                    setupLogging()
                    setupLogging()
                    setupLogging()

                    # Verify it was called successfully each time
                    assert mock_logger.setLevel.call_count == 3


class TestLoggingIntegration:
    """Integration tests for logging"""

    def test_logging_writes_to_file(self):
        """Test that logging actually writes to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, 'test_log.txt')

            # Create a logger and set it up
            test_logger = logging.getLogger('test_logger')
            test_logger.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            test_logger.addHandler(file_handler)

            # Log a message
            test_message = "Test log message"
            test_logger.debug(test_message)

            # Close the handler to flush
            file_handler.close()

            # Read the file and verify message was logged
            with open(log_file, 'r') as f:
                content = f.read()
                assert test_message in content

    def test_logging_includes_timestamp(self):
        """Test that log messages include timestamps"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, 'test_log.txt')

            test_logger = logging.getLogger('test_logger_timestamp')
            test_logger.setLevel(logging.DEBUG)
            test_logger.handlers = []  # Clear existing handlers

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            test_logger.addHandler(file_handler)

            # Log a message
            test_logger.debug("Test message with timestamp")
            file_handler.close()

            # Read the file and verify timestamp is present
            with open(log_file, 'r') as f:
                content = f.read()
                # Check for typical timestamp format (year-month-day)
                assert any(char.isdigit() for char in content)
                assert "DEBUG" in content

    def test_logging_includes_level(self):
        """Test that log messages include log level"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, 'test_log.txt')

            test_logger = logging.getLogger('test_logger_level')
            test_logger.setLevel(logging.DEBUG)
            test_logger.handlers = []

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            test_logger.addHandler(file_handler)

            # Log messages at different levels
            test_logger.debug("Debug message")
            test_logger.info("Info message")
            file_handler.close()

            # Read the file and verify levels are present
            with open(log_file, 'r') as f:
                content = f.read()
                assert "DEBUG" in content
                assert "INFO" in content
