import pytest
from unittest.mock import AsyncMock,patch

@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()

    message.from_user = AsyncMock()
    message.from_user.id = 12345
    message.from_user.username="Max"
    message.reply = AsyncMock()
    with patch("app.handlers.user.set_user", new_callable=AsyncMock) as mock_set_user:
        from app.handlers.user import cmd_start
        await cmd_start(message)
        mock_set_user.assert_called_once_with(12345, "Max")
        message.reply.assert_called_once_with("Hello Max")
