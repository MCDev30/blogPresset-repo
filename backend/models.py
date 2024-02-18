def create_user_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password BLOB NOT NULL,
            phone VARCHAR (255) NOT NULL,
            salt BLOB NOT NULL,
            token VARCHAR(2000) NOT NULL,
            active INT NOT NULL,
            code VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)


def bank_account_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Account (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            bank VARCHAR(255) NOT NULL,
            account_number VARCHAR(255) NOT NULL,
            iban VARCHAR(255) NOT NULL,
            bic VARCHAR(255) NOT NULL ,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  
        )
    """)


def create_cheque_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cheque (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            bank_name VARCHAR(255) NOT NULL,
            nom VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            montant VARCHAR(255) NOT NULL,
            objet VARCHAR(255),
            expire VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
