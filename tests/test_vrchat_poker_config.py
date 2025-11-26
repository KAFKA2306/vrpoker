"""Tests for VRChat Poker Agent configuration."""

import os
from unittest.mock import patch

import pytest

from poker_gto.environments.vrchat_poker import VRChatPokerEnvironment


@pytest.fixture
def mock_pamiq_vrchat():
    with (
        patch("poker_gto.environments.vrchat_poker.ImageSensor") as mock_sensor,
        patch("poker_gto.environments.vrchat_poker.Clicker") as mock_actuator,
    ):
        yield mock_sensor, mock_actuator


def test_init_default(mock_pamiq_vrchat):
    """Test initialization with default settings (no env var)."""
    mock_sensor_cls, mock_actuator_cls = mock_pamiq_vrchat

    # Ensure env var is unset
    if "VRCHAT_VIDEO_SOURCE" in os.environ:
        del os.environ["VRCHAT_VIDEO_SOURCE"]

    env = VRChatPokerEnvironment()

    # Should initialize ImageSensor with no args (default)
    mock_sensor_cls.assert_called_once_with()
    # Should initialize Clicker
    mock_actuator_cls.assert_called_once()
    assert env.image_sensor is not None
    assert env.actuator is not None


def test_init_with_video_source_url(mock_pamiq_vrchat):
    """Test initialization with video source URL."""
    mock_sensor_cls, mock_actuator_cls = mock_pamiq_vrchat

    test_url = "rtsp://192.168.1.100:8554/live"
    with patch.dict(os.environ, {"VRCHAT_VIDEO_SOURCE": test_url}):
        env = VRChatPokerEnvironment()

        # Should initialize ImageSensor with camera_index=test_url
        mock_sensor_cls.assert_called_once_with(camera_index=test_url)
        assert env.image_sensor is not None


def test_init_with_video_source_index(mock_pamiq_vrchat):
    """Test initialization with video source index."""
    mock_sensor_cls, mock_actuator_cls = mock_pamiq_vrchat

    with patch.dict(os.environ, {"VRCHAT_VIDEO_SOURCE": "1"}):
        env = VRChatPokerEnvironment()

        # Should initialize ImageSensor with camera_index=1
        mock_sensor_cls.assert_called_once_with(camera_index=1)
        assert env.image_sensor is not None
