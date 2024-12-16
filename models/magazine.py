from typing import List, TYPE_CHECKING
from database.connection import Connection

if TYPE_CHECKING:
    from models.article import Article
    from models.author import Author

class Magazine:
    def __init__(self, id: int, name: str):
        if not isinstance(id, int):
            raise ValueError("ID must be an integer.")
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        
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
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    def articles(self, connection: Connection) -> List["Article"]:
        """Fetch all articles published in this magazine."""
        query = "SELECT * FROM articles WHERE magazine_id = ?;"
        rows = connection.get_db_connection().execute(query, (self.id,)).fetchall()
        from models.article import Article  # Local import to avoid circular dependency
        return [Article(**dict(row)) for row in rows]

    def contributors(self, connection: Connection) -> List["Author"]:
        """Fetch all distinct authors who have contributed to this magazine."""
        query = """
            SELECT DISTINCT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?;
        """
        rows = connection.get_db_connection().execute(query, (self.id,)).fetchall()
        from models.author import Author  # Local import to avoid circular dependency
        return [Author(**dict(row)) for row in rows]

    def article_titles(self, connection: Connection) -> List[str]:
        """Fetch all article titles for this magazine."""
        query = "SELECT title FROM articles WHERE magazine_id = ?;"
        titles = connection.get_db_connection().execute(query, (self.id,)).fetchall()
        return [title[0] for title in titles]

    def contributing_authors(self, connection: Connection) -> List["Author"]:
        """Fetch authors with more than two articles in this magazine."""
        query = """
            SELECT authors.*, COUNT(articles.id) AS article_count 
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2;
        """
        rows = connection.get_db_connection().execute(query, (self.id,)).fetchall()
        from models.author import Author  # Local import to avoid circular dependency
        return [Author(**dict(row)) for row in rows]