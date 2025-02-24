import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
from Twitch import main

class TestTwitch(unittest.IsolatedAsyncioTestCase):

    @patch('Twitch.close_app')
    @patch('Twitch.Twitch.get_streams', new_callable=AsyncMock)
    @patch('asyncio.sleep', new_callable=AsyncMock)
    #@patch('tkinter.messagebox.askyesno', new_callable=MagicMock)
    #@patch('os.system')
    async def test_stream_end_with_shutdown(self, mock_sleep, mock_get_streams, mock_close_app):
        mock_get_streams.side_effect = [
            [{'user_login': 'testchannel', 'type': 'live'}],
            []
        ]
        #mock_askyesno.return_value = True
        with patch('builtins.input', side_effect=['testchannel', 'n']):
            await main()
        mock_get_streams.assert_called()
        mock_close_app.assert_called_once_with("chrome.exe")
        #mock_askyesno.assert_called_once_with("End of stream", "Want to shut down the PC?")
        #mock_system.assert_called_once_with("shutdown /s /t 5")



    @patch('Twitch.close_app')
    @patch('Twitch.Twitch.get_streams', new_callable=AsyncMock)
    @patch('asyncio.sleep', new_callable=AsyncMock)
    #@patch('tkinter.messagebox.askyesno', new_callable=MagicMock)
    #@patch('os.system')
    async def test_stream_end_without_shutdown(self, mock_sleep, mock_get_streams, mock_close_app):
        mock_get_streams.side_effect = [
            [{'user_login': 'testchannel', 'type': 'live'}],
            []
        ]
        #mock_askyesno.return_value = False
        with patch('builtins.input', side_effect=['testchannel', 'n']):
            await main()
        mock_get_streams.assert_called()
        mock_close_app.assert_called_once_with("chrome.exe")
        #mock_askyesno.assert_called_once_with("End of stream", "Want to shut down the PC?")
        #mock_system.assert_not_called()



    @patch('Twitch.close_app')
    @patch('Twitch.Twitch.get_streams', new_callable=AsyncMock)
    async def test_stream_start(self, mock_get_streams, mock_close_app):
        async def async_iterable():
            yield [{'user_login': 'testchannel', 'type': 'live'}]
        mock_get_streams.return_value.__aiter__ = async_iterable
        mock_get_streams.side_effect = None
        with patch('builtins.input', return_value='testchannel'):
            await main()
        mock_get_streams.assert_called()
        mock_close_app.assert_not_called()


if __name__ == '__main__':
    asyncio.run(unittest.main(argv=['first-arg-is-ignored'], exit=False))