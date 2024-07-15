import PyPDF2
import spacy
import sqlite3
from spacy.lang.en.stop_words import STOP_WORDS

# Step 1: Extract Text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Step 2: Enhanced Entity Extraction
def extract_entities_and_relationships(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = set()
    relationships = set()
    for ent in doc.ents:
        if ent.text.lower() not in STOP_WORDS and ent.label_ not in ["DATE", "TIME"]:  # Filter out stop words and dates
            # Check if the entity contains alphabetic characters and is not just symbols or numbers
            if any(char.isalpha() for char in ent.text):
                entities.add((ent.text, ent.label_))
    for sent in doc.sents:
        entities_in_sent = [ent.text for ent in sent.ents if (ent.text.lower(), ent.label_) in entities]
        for ent in entities_in_sent:
            for token in sent:
                if token.dep_ in ('nsubj', 'dobj') and token.head.pos_ == 'VERB' and token.text in entities_in_sent:
                    relationships.add((ent, token.head.text, token.text))
    return entities, relationships

# Step 3: SQLite Database Class
class SQLiteDB:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS entities
                                 (id INTEGER PRIMARY KEY, name TEXT, label TEXT)''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS relationships
                                 (id INTEGER PRIMARY KEY, entity1 TEXT, relationship TEXT, entity2 TEXT)''')

    def insert_entity(self, entity, label):
        with self.conn:
            self.conn.execute("INSERT INTO entities (name, label) VALUES (?, ?)", (entity, label))

    def insert_relationship(self, entity1, relationship, entity2):
        with self.conn:
            self.conn.execute("INSERT INTO relationships (entity1, relationship, entity2) VALUES (?, ?, ?)",
                              (entity1, relationship, entity2))

    def close(self):
        self.conn.close()

# Main Process
def main(pdf_path, db_name):
    pdf_text = extract_text_from_pdf(pdf_path)
    entities, relationships = extract_entities_and_relationships(pdf_text)

    # Connect to the SQLite database
    db = SQLiteDB(db_name)

    # Insert entities into the database (remove duplicates)
    existing_entities = set()
    for entity, label in entities:
        if (entity.lower(), label) not in existing_entities:
            db.insert_entity(entity, label)
            existing_entities.add((entity.lower(), label))

    # Insert relationships into the database
    for ent1, rel, ent2 in relationships:
        db.insert_relationship(ent1, rel, ent2)

    db.close()

# Running the main process
if __name__ == "__main__":
    main("c://Users//Nandan//Downloads//exter.pdf", "knowledge_graph1.db")
