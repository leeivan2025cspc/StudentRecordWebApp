import sqlite3
from typing import Optional, List, Dict
DB_PATH = 'students.db'

class StudentNode:
    def __init__(self, student_id: str, name: str, course: str, grade: str):
        self.id = student_id
        self.name = name
        self.course = course
        self.grade = grade
        self.next = None

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'course': self.course, 'grade': self.grade}

class StudentLinkedList:
    def __init__(self):
        self.head: Optional[StudentNode] = None

    def insert(self, student_id: str, name: str, course: str, grade: str):
        new_node = StudentNode(student_id, name, course, grade)
        new_node.next = self.head
        self.head = new_node

    def delete_by_id(self, student_id: str) -> bool:
        prev = None
        curr = self.head
        while curr:
            if curr.id == student_id:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True
            prev, curr = curr, curr.next
        return False

    def find_by_id(self, student_id: str) -> Optional[StudentNode]:
        curr = self.head
        while curr:
            if curr.id == student_id:
                return curr
            curr = curr.next
        return None

    def to_list(self) -> List[Dict]:
        arr = []
        curr = self.head
        while curr:
            arr.append(curr.to_dict())
            curr = curr.next
        return arr

    def load_from_list(self, arr: List[Dict]):
        self.head = None
        for record in reversed(arr):
            self.insert(record['id'], record['name'], record.get('course',''), record.get('grade',''))

    def sort_by_name(self):
        arr = self.to_list()
        arr.sort(key=lambda r: r['name'].lower())
        self.load_from_list(arr)

    def sort_by_id(self):
        arr = self.to_list()
        arr.sort(key=lambda r: r['id'])
        self.load_from_list(arr)

# SQLite helpers
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            course TEXT,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_all_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, course, grade FROM students')
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_student_to_db(record: Dict):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('REPLACE INTO students (id, name, course, grade) VALUES (?, ?, ?, ?)', (record['id'], record['name'], record.get('course',''), record.get('grade','')))
    conn.commit()
    conn.close()

def delete_student_from_db(student_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
