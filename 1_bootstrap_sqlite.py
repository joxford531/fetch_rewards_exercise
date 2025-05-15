import sqlite3
import datetime
import uuid
import random
from datetime import timedelta
from faker import Faker

fake = Faker()

database = 'rewards.db'
sql_table_statements = [
  "DROP TABLE IF EXISTS Roles;",
  "DROP TABLE IF EXISTS Sign_Up_Sources;",
  "DROP TABLE IF EXISTS US_States;",
  "DROP TABLE IF EXISTS Receipt_Statuses;",
  "DROP TABLE IF EXISTS Users;",
  "DROP TABLE IF EXISTS Brands;",
  "DROP TABLE IF EXISTS Items;",
  "DROP TABLE IF EXISTS Receipts;",
  "DROP TABLE IF EXISTS Receipt_Items;",

  """
    CREATE TABLE Roles (
      id INTEGER PRIMARY KEY NOT NULL,
      name VARCHAR(255) NOT NULL
    );
  """,

  """
    CREATE TABLE Sign_Up_Sources (
      id INTEGER PRIMARY KEY NOT NULL,
      name VARCHAR(255) NOT NULL
    );
  """,

  """
    CREATE TABLE US_States (
      id INTEGER PRIMARY KEY NOT NULL,
      abbreviation CHAR(2) NOT NULL,
      UNIQUE(abbreviation)
    );
  """,
  
  """
    CREATE TABLE Receipt_Statuses (
      id INTEGER PRIMARY KEY NOT NULL,
      status VARCHAR(255) NOT NULL,
      UNIQUE(status)
    );
  """,

  """
    CREATE TABLE Users (
      id INTEGER PRIMARY KEY NOT NULL,
      name VARCHAR(255) NOT NULL,
      active INTEGER NOT NULL,
      created_date INTEGER NOT NULL,
      last_login INTEGER,
      role_id INTEGER NOT NULL,
      FOREIGN KEY(role_id) REFERENCES Roles(id)
    );
  """,

  """
    CREATE TABLE Brands (
      id INTEGER PRIMARY KEY NOT NULL,
      name VARCHAR(255) NOT NULL,
      brand_code VARCHAR(255) NOT NULL,
      barcode VARCHAR(12) NOT NULL,
      category VARCHAR(255) NOT NULL,
      category_code VARCHAR(255),
      top_brand INTEGER NOT NULL,
      cpg_id VARCHAR(24) NOT NULL
    );
  """,

  """
    CREATE TABLE Items (
      id INTEGER PRIMARY KEY NOT NULL,
      description VARCHAR(255) NOT NULL,
      price VARCHAR(20) NOT NULL,
      partner_item_id VARCHAR(4) NOT NULL,
      brand_id INTEGER NOT NULL,
      FOREIGN KEY(brand_id) REFERENCES Brands(id)
    );
  """,

  """
    CREATE TABLE Receipts (
      id INTEGER PRIMARY KEY NOT NULL,
      bonus_points_earned INTEGER,
      purchase_date INTEGER NOT NULL,
      create_date INTEGER NOT NULL,
      date_scanned INTEGER NOT NULL,
      finished_date INTEGER,
      modify_date INTEGER,
      points_awarded_date INTEGER,      
      purchase_item_count INTEGER,
      total_spent VARCHAR(20),
      rewards_receipt_status_id INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      FOREIGN KEY(rewards_receipt_status_id) REFERENCES Receipt_Statuses(id),
      FOREIGN KEY(user_id) REFERENCES Users(id)
    );
  """,

  """
    CREATE TABLE Receipt_Items (
      receipt_id INTEGER NOT NULL,
      item_id INTEGER NOT NULL,
      barcode VARCHAR(12),
      final_price VARCHAR(20) NOT NULL,
      FOREIGN KEY (receipt_id) REFERENCES Receipts(id),
      FOREIGN KEY (item_id) REFERENCES Items(id)
    )
  """
]

sql_insert_statements = [
  """
    INSERT INTO Roles (Name) Values
    ("fetch-staff"),
    ("consumer");
  """,

  """
    INSERT INTO Sign_Up_Sources (Name) Values
    ("email");
  """,

  """
    INSERT INTO Receipt_Statuses (status) Values
    ("SUBMITTED"),
    ("FINISHED"),
    ("REJECTED");
  """
]

def bootstrap():
  try:
    create_tables(database, sql_table_statements, sql_insert_statements)
    seed_states(database)
    seed_users(database)
    seed_brands(database)
    seed_items(database)
    seed_receipts(database)

    print("DB update successful")
  except sqlite3.OperationalError as e:
    print(e)

def create_tables(database, table_statements, seed_statements):
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    
    for statement in table_statements:
      cursor.execute(statement)

    for statement in seed_statements:
      conn.execute(statement)

    conn.commit()

def seed_states(database):
  mock_data_us_states = """
    INSERT INTO US_States (abbreviation) VALUES 
  """

  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    us_state_rows = []

    for _ in range(50):
      abbr = fake.unique.state_abbr(False, False)
      us_state_rows.append(f'("{abbr}"),')

    mock_data_us_states = mock_data_us_states + "".join(us_state_rows)[:-1] + ";"

    cursor.execute(mock_data_us_states)
    conn.commit()

def seed_users(database):
  mock_users = """
    INSERT INTO Users (name, active, created_date, role_id) VALUES
  """
  user_rows = []

  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    now = datetime.datetime.now() - timedelta(days=1)
    epoch = int(now.timestamp() * 1000)

    for _ in range(100):
      user = fake.unique.name()
      user_rows.append(f'("{user}", TRUE, {epoch}, 1),')

    mock_users = mock_users + "".join(user_rows)[:-1] + ";"

    cursor.execute(mock_users)
    conn.commit()

def seed_brands(database):
  mock_brands = """
    INSERT INTO Brands (name, brand_code, barcode, category, category_code, top_brand, cpg_id) VALUES
  """
  brand_rows = []

  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()

    for _ in range(100):
      name = fake.unique.company()
      brand_code = fake.unique.word().upper()
      barcode = fake.unique.ean(length=13)[:-1]
      category = fake.unique.word()
      category_code = fake.unique.word().upper()
      top_brand = str(fake.boolean()).upper()
      cpg_id = str(uuid.uuid4()).replace("-", "")[0:24]

      brand_rows.append(f'("{name}", "{brand_code}", "{barcode}", "{category}", \
        "{category_code}", {top_brand}, "{cpg_id}"),')

    mock_brands = mock_brands + "".join(brand_rows)[:-1] + ";"

    cursor.execute(mock_brands)
    conn.commit()

def seed_items(database):
  mock_items = """
    INSERT INTO Items (description, price, partner_item_id, brand_id) VALUES
  """
  item_rows = []

  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()

    for _ in range(1000):
      description = fake.text(max_nb_chars=20)
      price = fake.numerify(text='##.##')
      partner_item_id = str(random.randint(1, 12))
      brand_id = random.randint(1, 100)

      item_rows.append(f'("{description}", "{price}", "{partner_item_id}", {brand_id}),')

    mock_items = mock_items + "".join(item_rows)[:-1] + ";"

    cursor.execute(mock_items)
    conn.commit()

def seed_receipts(database):
  mock_receipts = """
    INSERT INTO Receipts (bonus_points_earned, purchase_date, create_date, date_scanned, finished_date, \
    modify_date, points_awarded_date, purchase_item_count, total_spent, \
    rewards_receipt_status_id, user_id) VALUES 
  """

  mock_receipt_items = """
    INSERT INTO Receipt_Items (receipt_id, item_id, barcode, final_price) VALUES 
  """

  receipt_rows = []
  receipt_item_rows = []

  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()

    for num in range(1, 10000):
      bonus_points_earned = random.randint(10, 100)

      purchase_date = fake.date_time_between(start_date='-26w', end_date='-4w')
      purchase_date_epoch = int(purchase_date.timestamp() * 1000)

      created_date = purchase_date + timedelta(weeks=1)
      created_date_epoch = int(created_date.timestamp() * 1000)

      date_scanned_epoch = created_date_epoch

      finished_date = created_date + timedelta(weeks=1)
      finished_date_epoch = int(finished_date.timestamp() * 1000)

      modified_date = finished_date + timedelta(days=1)
      modified_date_epoch = int(modified_date.timestamp() * 1000)

      points_awared_date_epoch = finished_date_epoch

      purchase_item_count = random.randint(1, 10)
      total_spent = str(round(random.random() * (100 + purchase_item_count), 2))
      rewards_receipt_status_id = random.randint(2,3)
      user_id = random.randint(1, 100)

      receipt_rows.append(f'({bonus_points_earned}, {purchase_date_epoch}, {created_date_epoch}, \
        {date_scanned_epoch}, {finished_date_epoch}, {modified_date_epoch}, {points_awared_date_epoch}, \
        {purchase_item_count}, "{total_spent}", {rewards_receipt_status_id}, {user_id}),')

      item_id = random.randint(1, 100)
      barcode = fake.unique.ean(length=13)[:-1]
      receipt_item_rows.append(f'({num}, {item_id}, "{barcode}", "{total_spent}"),')

    mock_receipts = mock_receipts + "".join(receipt_rows)[:-1] + ";"
    mock_receipt_items = mock_receipt_items + "".join(receipt_item_rows)[:-1] + ";"

    cursor.execute(mock_receipts)
    cursor.execute(mock_receipt_items)    
    conn.commit()

bootstrap()