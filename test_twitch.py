import unittest
from unittest.mock import patch, AsyncMock
import asyncio
from Twitch import main

class TestTwitch(unittest.IsolatedAsyncioTestCase):

    @patch('twitch.close_app')
    @patch('twitchAPI.Twitch.get_streams', new_callable=AsyncMock)
    async def test_stream_end(self, mock_get_streams, mock_close_app):
        mock_get_streams.return_value = []
        with patch('builtins.input', return_value='test_channel'):
            await main()
        mock_get_streams.assert_called()
        mock_close_app.assert_called_with('chrome.exe')

    @patch('twitch.close_app')
    @patch('twitchAPI.Twitch.get_streams', new_callable=AsyncMock)
    async def test_stream_start(self, mock_get_streams, mock_close_app):
        mock_get_streams.return_value = [{'user_login': 'test_channel', 'type': 'live'}]
        with patch('builtins.input', return_value='test_channel'):
            await main()
        mock_get_streams.assert_called()
        mock_close_app.assert_not_called()


if __name__ == '__main__':
    asyncio.run(unittest.main(argv=['first-arg-is-ignored'], exit=False))