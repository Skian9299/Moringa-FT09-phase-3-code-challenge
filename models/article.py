from typing import TYPE_CHECKING
from database.connection import Connection

if TYPE_CHECKING:
    from models.author import Author
    from models.magazine import Magazine

class Article:
    def __init__(self, id: int, title: str, content: str, author_id: int, magazine_id: int):
        if not isinstance(id, int):
            raise ValueError("ID must be an integer.")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        if not isinstance(content, str):
            raise ValueError("Content must be a string.")
        if not isinstance(author_id, int):
            raise ValueError("Author ID must be an integer.")
        if not isinstance(magazine_id, int):
            raise ValueError("Magazine ID must be an integer.")
        
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        raise AttributeError("Cannot change title after initialization.")

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str):
        raise AttributeError("Cannot change content after initialization.")

    @property
    def author(self) -> "Author":
        """Fetch the author associated with this article."""
        query = "SELECT * FROM authors WHERE id = ?;"
        result = Connection.get_db_connection().execute(query, (self._author_id,)).fetchone()
        if result:
            from models.author import Author  # Local import to avoid circular dependency
            return Author(**dict(result))
        return None

    @property
    def magazine(self) -> "Magazine":
        """Fetch the magazine associated with this article."""
        query = "SELECT * FROM magazines WHERE id = ?;"
        result = Connection.get_db_connection().execute(query, (self._magazine_id,)).fetchone()
        if result:
            from models.magazine import Magazine  # Local import to avoid circular dependency
            return Magazine(**dict(result))
        return None