import unittest
from unittest.mock import patch, AsyncMock
import asyncio
from Twitch import main

class TestTwitch(unittest.IsolatedAsyncioTestCase):

    @patch('Twitch.close_app')
    @patch('Twitch.Twitch.get_streams')
    async def test_stream_end(self, mock_get_streams, mock_close_app):
        async def mock_get_streams_impl(*args, **kwargs):
            yield []

        mock_get_streams.side_effect = mock_get_streams_impl
        with patch('builtins.input', return_value='test_channel'):
            await main()

        mock_get_streams.assert_called()
        mock_close_app.assert_called_with("chrome.exe")




    @patch('Twitch.close_app')
    @patch('Twitch.Twitch.get_streams')
    async def test_stream_start(self, mock_get_streams, mock_close_app):
        async def mock_get_streams_impl(*args, **kwargs):
            yield []

        mock_get_streams.side_effect = mock_get_streams_impl
        with patch('builtins.input', return_value='test_channel'):
            await main()

        mock_get_streams.assert_called()
        mock_close_app.assert_not_called()


if __name__ == '__main__':
    asyncio.run(unittest.main(argv=['first-arg-is-ignored'], exit=False))