from typing import List, TYPE_CHECKING
from database.connection import Connection

if TYPE_CHECKING:
    from models.article import Article
    from models.magazine import Magazine

class Author:
    def __init__(self, id: int, name: str):
        if not isinstance(id, int):
            raise ValueError("ID must be an integer.")
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        raise AttributeError("Cannot change name after initialization.")

    def articles(self, connection: Connection) -> List["Article"]:
        """Fetch all articles by this author."""
        query = "SELECT * FROM articles WHERE author_id = ?;"
        rows = connection.get_db_connection().execute(query, (self.id,)).fetchall()
        from models.article import Article  # Local import to avoid circular dependency
        return [Article(**dict(row)) for row in rows]

    def magazines(self, connection: Connection) -> List["Magazine"]:
        """Fetch all distinct magazines associated with this author."""
        query = """
            SELECT DISTINCT m.* 
            FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?;
        """
        rows = connection.get_db_connection().execute(query, (self.id,)).fetchall()
        from models.magazine import Magazine  # Local import to avoid circular dependency
        return [Magazine(**dict(row)) for row in rows]