# CodeAlpha Task 1 – Simple URL Shortener

## Project Overview
The Simple URL Shortener is a backend web application developed using Python and Flask. It converts long URLs into short, unique URLs and redirects users to the original URL when the short URL is accessed.

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS

## Features
- Generate unique 6-character short codes.
- Store original URLs and short codes in an SQLite database.
- Redirect short URLs to their original destinations.
- REST API endpoint for creating short URLs.
- Validate submitted URLs.
- Display generated short URLs on a simple web page.

## Project Structure
```text
CodeAlpha_URLShortener/
│
├── app.py
├── requirements.txt
├── view_data.py
├── database.db
└── templates/
    └── index.html
```

## Installation and Setup

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
python app.py
```

6. Open the browser:

```text
http://127.0.0.1:5000/
```

## API Endpoint

### Create Short URL

- **Method:** POST
- **Endpoint:** `/api/shorten`
- **Content-Type:** application/json

Request body:

```json
{
  "original_url": "https://www.google.com"
}
```

Successful response: `201 Created`

```json
{
  "original_url": "https://www.google.com",
  "short_code": "oTTUAS",
  "short_url": "http://127.0.0.1:5000/oTTUAS"
}
```

The short code and short URL in this example are illustrative. Actual generated codes are unique.

### Redirect to Original URL

- **Method:** GET
- **Endpoint:** `/<short_code>`

Example:

```text
http://127.0.0.1:5000/oTTUAS
```

This redirects the user to the original URL.

## Database
SQLite is used to store URL information in the `urls` table.

The table contains:
- `id`
- `original_url`
- `short_code`

## Developer
CodeAlpha Internship – Python Backend Development

## Conclusion
This project demonstrates backend development using Flask, database integration with SQLite, URL validation, unique short code generation, and HTTP redirection.