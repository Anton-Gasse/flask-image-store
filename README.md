
# 🖼️ flask-image-storage

## 🔍 Overview

**flask-image-storage** is a lightweight, secure backend for temporary image storage. Uploaded images are encrypted on the server and assigned a unique hash for retrieval. Images expire after 5 minutes, ensuring privacy and efficient resource management. The service uses Flask for the API and PostgreSQL for database management.

## 🚀 Getting Started

### ⚡ Quick Start
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd flask-image-storage
   ```
2. Set the required environment variables:
   ```bash
   export POSTGRES_USER=<myuser>
   export POSTGRES_PASSWORD=<mypassword>
   ```
3. Start the service with Docker Compose:
   ```bash
   docker compose up
   ```
4. Add API-keys to the database [OPTIONAL]:
   ```bash
   #Inside your database in the docker database container:
   INSERT INTO api_key (api_key, name, timestamp) VALUES ('abcdefg', 'test_user', NOW()); 
   ```

### 🛠️ Development Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd flask-image-storage
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Start a PostgreSQL container:
   ```bash
   docker run -d --name my_postgres_container \
       -e POSTGRES_USER=<myuser> \
       -e POSTGRES_PASSWORD=<mypassword> \
       -e POSTGRES_DB=images \
       -p 5432:5432 postgres
   ```
4. Set the environment variables:
   ```bash
   export POSTGRES_USER=<myuser>
   export POSTGRES_PASSWORD=<mypassword>
   export HOST=<myhost>
   ```
5. Apply database migrations:
   ```bash
   flask db upgrade
   ```
6. Add API-keys to the database [OPTIONAL]:
   ```bash
   #Inside your database in the docker database container:
   INSERT INTO api_key (api_key, name, timestamp) VALUES ('abcdefg', 'test_user', NOW()); 
   ```

7. Start the development server:
   ```bash
   python3 app.py
   ```

## 🔗 API Endpoints

### 📤 `POST /upload`
- **Description**: Uploads an image, encrypts and stores it in the database, and returns a unique hash for retrieval. If there is no API-key in the database you don't have to provide one. Otherwise you have to add one to the request header. Also triggers cleanup of expired images.
- **Request Example**:
   ```bash
   # No API-key:
   curl -X POST -F "file=@test.jpg" http://127.0.0.1:5000/upload
   ```
   ```bash
   # With API-key:
   curl -X POST -F "file=@test.jpg" -H "api-key: abcdefg" http://127.0.0.1:5000/upload
   ```

### 📥 `GET /image/<image_hash>`
- **Description**: Retrieves an image by its unique hash. If the hash corresponds to an expired or non-existent image, an error is returned. Also triggers cleanup.
- **Usage Example**:
   ```bash
   curl http://127.0.0.1:5000/image/<image_hash>
   ```

### 🧹 `GET /cleanup`
- **Description**: Deletes all expired images from the database. This endpoint is called automatically during image uploads or retrievals.