from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise ValueError("ID must be an integer.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def save(self):
        # Save the Magazine to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self.name, self.category))
        conn.commit()
        self.id = cursor.lastrowid  # Get the id of the newly created magazine
        conn.close()

    @classmethod
    def get_by_id(cls, magazine_id):
        # Fetch a magazine by ID
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
        magazine_data = cursor.fetchone()
        conn.close()
        if magazine_data:
            return cls(magazine_data[0], magazine_data[1], magazine_data[2])
        return None


