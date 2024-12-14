import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection

class TestModels(unittest.TestCase):

    def setUp(self):
        """Setup method to prepare the database before each test."""
        # Initialize the database and create tables
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # Clean the database tables to avoid duplicate entries
        self.cursor.execute('DELETE FROM articles')
        self.cursor.execute('DELETE FROM authors')
        self.cursor.execute('DELETE FROM magazines')

        # Commit changes to ensure the tables are clean
        self.conn.commit()

    def test_author_creation(self):
        # Create an author and insert it into the database
        author = Author(1, "John Doe")
        self.cursor.execute('INSERT INTO authors (id, name) VALUES (?, ?)', (author.id, author.name))
        self.conn.commit()

        # Fetch the author back from the database
        self.cursor.execute('SELECT * FROM authors WHERE id = ?', (author.id,))
        db_author = self.cursor.fetchone()

        # Assert that the author's name matches the inserted name
        self.assertEqual(db_author["name"], "John Doe")

    def test_article_creation(self):
        # Create an author and insert it into the database
        author = Author(1, "John Doe")
        self.cursor.execute('INSERT INTO authors (id, name) VALUES (?, ?)', (author.id, author.name))
        
        # Create a magazine and insert it into the database
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.cursor.execute('INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)', 
                            (magazine.id, magazine.name, magazine.category))
        
        # Create an article with the author and magazine's ids
        article = Article(1, "Test Article", "Content of the article", author.id, magazine.id)
        self.cursor.execute('INSERT INTO articles (id, title, content, author_id, magazine_id) VALUES (?, ?, ?, ?, ?)', 
                            (article.id, article.title, article.content, article.author_id, article.magazine_id))
        self.conn.commit()

        # Fetch the article back from the database
        self.cursor.execute('SELECT * FROM articles WHERE id = ?', (article.id,))
        db_article = self.cursor.fetchone()

        # Fetch the related author from the database
        self.cursor.execute('SELECT * FROM authors WHERE id = ?', (db_article["author_id"],))
        db_author = self.cursor.fetchone()

        # Assert that the article's title is correct
        self.assertEqual(db_article["title"], "Test Article")

        # Assert that the article's author is correctly associated
        self.assertEqual(db_author["name"], "John Doe")  # The author's name should be "John Doe"

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.cursor.execute('INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)', 
                            (magazine.id, magazine.name, magazine.category))
        self.conn.commit()

        # Fetch the magazine back from the database
        self.cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine.id,))
        db_magazine = self.cursor.fetchone()

        self.assertEqual(db_magazine["name"], "Tech Weekly")

    def tearDown(self):
        """Cleanup after each test."""
        self.cursor.execute('DELETE FROM articles')
        self.cursor.execute('DELETE FROM authors')
        self.cursor.execute('DELETE FROM magazines')
        self.conn.commit()
        # Close the database connection after each test
        self.conn.close()

if __name__ == "__main__":
    unittest.main()



