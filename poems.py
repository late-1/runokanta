from datetime import datetime
import db


def get_all():
    sql = """
        SELECT p.id, p.title, p.content, p.published, p.user_id, u.username
        FROM poems p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.published DESC
    """
    return db.query(sql)


def get_poem(poem_id):
    sql = """
        SELECT p.id, p.title, p.content, p.published, p.user_id, u.username
        FROM poems p
        JOIN users u ON p.user_id = u.id
        WHERE p.id = ?
    """
    result = db.query(sql, [poem_id])
    return result[0] if result else None


def add_poem(title, content, user_id, category_value=None, theme_values=None):
    published = datetime.strftime(datetime.now(), '%d-%m-%Y')
    sql = "INSERT INTO poems (title, content, published, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, content, published, user_id])
    poem_id = db.last_insert_id()

    if category_value:
        add_category(poem_id, category_value)

    if theme_values:
        for theme in theme_values:
            add_theme(poem_id, theme)

    return poem_id


def get_user_poems(user_id):
    sql = """
        SELECT id, title, content, published
        FROM poems
        WHERE user_id = ?
        ORDER BY published DESC
    """
    return db.query(sql, [user_id])


def search_poems(query):
    sql = """
        SELECT p.id, p.title, p.content, p.published, p.user_id, u.username
        FROM poems p
        JOIN users u ON p.user_id = u.id
        WHERE p.title LIKE ? OR p.content LIKE ?
        ORDER BY p.published DESC
    """
    search_term = f"%{query}%"
    return db.query(sql, [search_term, search_term])


def add_category(poem_id, category_value):
    sql = "INSERT INTO category (poem_id, title, value) VALUES (?, ?, ?)"
    db.execute(sql, [poem_id, "category", category_value])


def add_theme(poem_id, theme_value):
    sql = "INSERT INTO themes (poem_id, title, value) VALUES (?, ?, ?)"
    db.execute(sql, [poem_id, "theme", theme_value])


def get_categories(poem_id):
    sql = "SELECT value FROM category WHERE poem_id = ?"
    return db.query(sql, [poem_id])


def get_themes(poem_id):
    sql = "SELECT value FROM themes WHERE poem_id = ?"
    return db.query(sql, [poem_id])


def add_review(poem_id, user_id, rating, comment):
    sql = "INSERT INTO reviews (poem_id, user_id, rating, comment) VALUES (?, ?, ?, ?)"
    db.execute(sql, [poem_id, user_id, rating, comment])


def get_reviews(poem_id):
    sql = """
        SELECT r.id, r.rating, r.comment, r.date, u.username
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.poem_id = ?
        ORDER BY r.date DESC
    """
    return db.query(sql, [poem_id])


def get_average_rating(poem_id):
    sql = "SELECT AVG(rating) as avg_rating FROM reviews WHERE poem_id = ?"
    result = db.query(sql, [poem_id])
    return result[0]['avg_rating'] if result and result[0]['avg_rating'] else None


def delete_poem(poem_id, user_id):
    sql = "SELECT user_id FROM poems WHERE id = ?"
    result = db.query(sql, [poem_id])

    if not result or result[0]['user_id'] != user_id:
        return False

    db.execute("DELETE FROM reviews WHERE poem_id = ?", [poem_id])
    db.execute("DELETE FROM category WHERE poem_id = ?", [poem_id])
    db.execute("DELETE FROM themes WHERE poem_id = ?", [poem_id])
    db.execute("DELETE FROM images WHERE poem_id = ?", [poem_id])

    db.execute("DELETE FROM poems WHERE id = ?", [poem_id])
    return True


def search_by_author(username):
    sql = """
        SELECT p.id, p.title, p.content, p.published, p.user_id, u.username
        FROM poems p
        JOIN users u ON p.user_id = u.id
        WHERE u.username LIKE ?
        ORDER BY p.published DESC
    """
    search_term = f"%{username}%"
    return db.query(sql, [search_term])


def get_all_categories():
    sql = "SELECT DISTINCT value FROM category ORDER BY value"
    return db.query(sql)


def get_all_themes():
    sql = "SELECT DISTINCT value FROM themes ORDER BY value"
    return db.query(sql)


def update_poem(poem_id, title, content):
    sql = "UPDATE poems SET title = ?, content = ? WHERE id = ?"
    db.execute(sql, [title, content, poem_id])


def update_category(poem_id, category_value):
    db.execute("DELETE FROM category WHERE poem_id = ?", [poem_id])
    if category_value:
        add_category(poem_id, category_value)


def update_themes(poem_id, theme_values):
    db.execute("DELETE FROM themes WHERE poem_id = ?", [poem_id])
    if theme_values:
        for theme in theme_values:
            add_theme(poem_id, theme)
            