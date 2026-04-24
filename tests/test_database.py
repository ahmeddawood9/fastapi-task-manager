from unittest.mock import MagicMock, patch
from app.database import get_db

def test_get_db():
    mock_session = MagicMock()
    with patch("app.database.SessionLocal", return_value=mock_session):
        db_gen = get_db()
        db = next(db_gen)
        assert db == mock_session
        try:
            next(db_gen)
        except StopIteration:
            pass
        mock_session.close.assert_called_once()
