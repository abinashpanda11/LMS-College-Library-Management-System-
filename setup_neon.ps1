$ErrorActionPreference = "Stop"

$cs = "postgresql://neondb_owner:npg_cmdWD0z3FhHC@ep-lucky-glitter-b5h5j8om-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require"
$uri = "https://ep-lucky-glitter-b5h5j8om-pooler.c-7.us-east-2.aws.neon.tech/sql"

$headers = @{
    "Neon-Connection-String" = $cs
    "Content-Type"           = "application/json"
}

function Run-NeonQuery([string]$sql) {
    $body = @{ query = $sql } | ConvertTo-Json
    $res = Invoke-RestMethod -Uri $uri -Method Post -Headers $headers -Body $body
    return $res
}

function Get-WerkzeugHash([string]$password) {
    $salt = "8899aabbccddeeff"
    $saltBytes = [System.Text.Encoding]::UTF8.GetBytes($salt)
    $iterations = 260000
    $pbkdf2 = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($password, $saltBytes, $iterations, [System.Security.Cryptography.HashAlgorithmName]::SHA256)
    $hashBytes = $pbkdf2.GetBytes(32)
    $hashHex = [System.BitConverter]::ToString($hashBytes).Replace("-", "").ToLower()
    return "pbkdf2:sha256:$iterations`$$salt`$$hashHex"
}

Write-Output "=========================================="
Write-Output "   SETTING UP NEON DATABASE SCHEMAS       "
Write-Output "=========================================="

# 1. CREATE USER TABLE
Write-Output "1. Creating 'user' table..."
$createUserSql = @"
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(500) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    full_name VARCHAR(100),
    dob DATE,
    registration_number VARCHAR(20) UNIQUE,
    section VARCHAR(10),
    semester INTEGER,
    photo_filename VARCHAR(500),
    is_blocked BOOLEAN DEFAULT FALSE,
    mobile_number VARCHAR(20),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"@
Run-NeonQuery $createUserSql | Out-Null
Write-Output "   -> 'user' table created successfully."

# 2. CREATE BOOK TABLE
Write-Output "2. Creating 'book' table..."
$createBookSql = @"
CREATE TABLE IF NOT EXISTS book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    category VARCHAR(50),
    quantity INTEGER DEFAULT 1,
    available INTEGER DEFAULT 1,
    misplaced INTEGER DEFAULT 0
);
"@
Run-NeonQuery $createBookSql | Out-Null
Write-Output "   -> 'book' table created successfully."

# 3. CREATE TRANSACTION TABLE
Write-Output "3. Creating 'transaction' table..."
$createTransactionSql = @"
CREATE TABLE IF NOT EXISTS transaction (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES book(id) ON DELETE CASCADE,
    issue_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP WITHOUT TIME ZONE,
    due_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'issued',
    fine_paid BOOLEAN DEFAULT FALSE,
    payment_id VARCHAR(50)
);
"@
Run-NeonQuery $createTransactionSql | Out-Null
Write-Output "   -> 'transaction' table created successfully."

# 4. SEED ADMIN USER
Write-Output "4. Seeding default admin user..."
$adminHash = Get-WerkzeugHash "admin123"
$seedAdminSql = @"
INSERT INTO "user" (username, email, password_hash, role, full_name)
VALUES ('admin', 'admin@library.com', '$adminHash', 'admin', 'System Administrator')
ON CONFLICT (username) DO UPDATE 
SET password_hash = '$adminHash', role = 'admin', email = 'admin@library.com';
"@
Run-NeonQuery $seedAdminSql | Out-Null
Write-Output "   -> Admin user 'admin' seeded with password 'admin123'."

# 5. SEED SAMPLE STUDENT USER
Write-Output "5. Seeding sample student user..."
$studentHash = Get-WerkzeugHash "student123"
$seedStudentSql = @"
INSERT INTO "user" (username, email, password_hash, role, full_name, registration_number, section, semester, mobile_number)
VALUES ('student', 'student@library.com', '$studentHash', 'student', 'Sample Student', 'REG1001', '1A1', 1, '+1234567890')
ON CONFLICT (username) DO NOTHING;
"@
Run-NeonQuery $seedStudentSql | Out-Null
Write-Output "   -> Student user 'student' seeded."

# 6. SEED SAMPLE BOOKS
Write-Output "6. Seeding initial books..."
$seedBooksSql = @"
INSERT INTO book (title, author, isbn, category, quantity, available, misplaced)
VALUES 
    ('Clean Code', 'Robert C. Martin', '9780132350884', 'Computers', 5, 5, 0),
    ('The Pragmatic Programmer', 'Andrew Hunt & David Thomas', '9780201616224', 'Computers', 3, 3, 0),
    ('Introduction to Algorithms', 'Thomas H. Cormen', '9780262033848', 'Education', 4, 4, 0),
    ('Design Patterns', 'Erich Gamma et al.', '9780201633610', 'Technology', 2, 2, 0)
ON CONFLICT (isbn) DO NOTHING;
"@
Run-NeonQuery $seedBooksSql | Out-Null
Write-Output "   -> Books seeded successfully."

# 7. VERIFY ALL TABLES IN NEON
Write-Output "`n=========================================="
Write-Output "   VERIFYING DATABASE TABLES IN NEON      "
Write-Output "=========================================="
$tablesRes = Run-NeonQuery "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
Write-Output "Tables in Neon DB:"
$tablesRes.rows | ForEach-Object { Write-Output " - $($_.table_name)" }

# 8. VERIFY USERS
Write-Output "`nUsers in 'user' table:"
$usersRes = Run-NeonQuery "SELECT id, username, email, role, full_name FROM ""user"";"
$usersRes.rows | ForEach-Object { Write-Output " - ID: $($_.id) | User: $($_.username) | Email: $($_.email) | Role: $($_.role)" }

# 9. VERIFY BOOKS
Write-Output "`nBooks in 'book' table:"
$booksRes = Run-NeonQuery "SELECT id, title, author, isbn, available FROM book;"
$booksRes.rows | ForEach-Object { Write-Output " - ID: $($_.id) | Title: $($_.title) | ISBN: $($_.isbn) | Avail: $($_.available)" }

Write-Output "`n=========================================="
Write-Output "   ALL OPERATIONS COMPLETED SUCCESSFULLY! "
Write-Output "=========================================="
