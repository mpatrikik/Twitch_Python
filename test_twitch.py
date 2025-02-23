import unittest
from unittest.mock import patch, AsyncMock
import asyncio
from Twitch import main

class TestTwitch(unittest.IsolatedAsyncioTestCase):

    @patch('Twitch.close_app')
    @patch('Twitch.Twitch.get_streams', new_callable=AsyncMock)
    async def test_stream_end(self, mock_get_streams, mock_close_app):
        async def async_iterable():
            yield []

        mock_get_streams.return_value.__aiter__ = async_iterable
        with patch('builtins.input', return_value='test_channel'):
            await main()

        mock_get_streams.assert_called()
        mock_close_app.assert_called_with('chrome.exe')




    @patch('Twitch.close_app')
    @patch('Twitch.Twitch.get_streams', new_callable=AsyncMock)
    async def test_stream_start(self, mock_get_streams, mock_close_app):
        async def async_iterable():
            yield [{'user_login': 'test_channel', 'type': 'live'}]

        mock_get_streams.return_value.__aiter__ = async_iterable
        with patch('builtins.input', return_value='test_channel'):
            await main()

        mock_get_streams.assert_called()
        mock_close_app.assert_called_with('chrome.exe')


if __name__ == '__main__':
    asyncio.run(unittest.main(argv=['first-arg-is-ignored'], exit=False))