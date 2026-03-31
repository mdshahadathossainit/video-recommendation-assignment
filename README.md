
# 🚀 Video Recommendation Engine (FastAPI & Content-Based Filtering)

A high-performance, asynchronous backend service built with FastAPI that provides personalized video recommendations. The system utilizes a hybrid approach, combining Popularity-Based filtering (for new users) and Content-Based filtering (based on user interaction history).

****


# 📸 Project Showcase
<div align="center">
<h3>🔍 Interactive API Documentation (Swagger UI)</h3>
<img src="https://imgur.com/vzxXzxy.png" width="800" alt="Swagger UI">
<p><i>The system automatically generates interactive documentation for all endpoints.</i></p>

<table style="width:100%">
<tr>
<td align="center"><b>📊 Personalized Recommendations</b></td>
<td align="center"><b>💓 System Health Check</b></td>
</tr>
<tr>
<td><img src="https://imgur.com/2GaWRjA.png" width="400" alt="Recommendations"></td>
<td><img src="https://imgur.com/EJsaUd6.png" width="400" alt="Health Check"></td>
</tr>
<tr>
<td align="center"><b>🛠️ API Data Schemas</b></td>
<td align="center"><b>📩 Interaction Models</b></td>
</tr>
<tr>
<td><img src="https://imgur.com/cGCoGd3.png" width="400" alt="Schemas"></td>
<td><img src="https://imgur.com/zbeSIfi.png" width="400" alt="Interactions"></td>
</tr>
</table>

<h3>📐 Data Validation Architecture</h3>
<img src="https://imgur.com/ZrQVY8A.png" width="800" alt="Validation">
</div>



---

## ✨ Project Highlights

This engine is built on a modern **FastAPI** stack, prioritizing scalability and asynchronous performance.

| Feature | Technologies Used | Description |
| :--- | :--- | :--- |
| **Backend API** | `FastAPI`, `Uvicorn`, `Pydantic` | Delivers extremely fast, non-blocking API endpoints. |
| **Data Persistence**| `SQLAlchemy 2.0+`, `Alembic` | Robust ORM for schema migration and database management. |
| **Data Source** | `YouTube Data API` | Fetches fresh, relevant video metadata from a large public source. |
| **Core Logic** | Custom Python Logic | Implements a **Hybrid** strategy: Popularity-Based (Cold Start) and Content-Based Filtering. |

---

## 🎯 Recommendation Strategy

The core value of this system lies in its ability to adapt its logic based on user history, effectively solving the "Cold Start" problem.

### 1. Popularity-Based (Cold Start Fallback)
* **Target:** New users or users with zero watch history.
* **Logic:** Defaults to showing the overall most-viewed and popular videos across all categories, ensuring immediate engagement.

### 2. Content-Based Filtering (Personalized Feed)
* **Target:** Established users with recorded interactions.
* **Logic:** Tracks user activity (`/interactions`) to identify their **top preferred video categories**. Recommendations are then filtered to prioritize content within those preferred categories.

---

## 🛠️ Setup and Installation

### 1. Prerequisites
Ensure you have **Python (3.10+)** and **pip** installed.

### 2. Environment and Dependencies

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# 2. Install required packages
pip install -r requirements.txt 
````

### 3\. Configuration

Create a **`.env`** file in the project root to store sensitive data and settings:

```env
# .env file

# Required for data fetching
YOUTUBE_API_KEY="<YOUR_YOUTUBE_API_KEY>"

# Database URL (Example for SQLite)
DATABASE_URL="sqlite+aiosqlite:///./sql_app.db" 

# Categories to fetch (e.g., Music, Entertainment, Gaming)
YOUTUBE_CATEGORY_IDS="10,24,20" 
```

### 4\. Database Setup

Use **Alembic** to initialize the database schema and create necessary tables:

```bash
alembic upgrade head
```

### 5\. Running the Application

Launch the server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API documentation (Swagger UI) will be accessible at `http://127.0.0.1:8000/docs`.

-----

## 🛣️ API Endpoints

Test the core functionality using `curl` commands or Postman (Postman Collection link can be provided here).

### A. Data Ingestion

Feeds the database with video metadata. **(Run this first\!)**

| Method | URL | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/youtube/fetch` | Fetches new videos based on configured categories. |

### B. User Interaction Tracking

Records a user's action to enable Content-Based Filtering.

| Method | URL | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/interactions` | Logs a user's `WATCHED` event for a video. |

**Example Body (JSON):**

```json
{
    "username": "test_user", 
    "youtube_id": "s3pDMUWlA6I", 
    "interaction_type": "WATCHED"
}
```

### C. Get Recommendations (Core Feature)

Retrieves the personalized video feed.

| Method | URL | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/recommendations?username=<username>` | Returns personalized or popular video recommendations. |

**Testing Logic:**

1.  Query with a new username (e.g., `?username=new_guest`) to see **Popularity-Based** results.
2.  Query with a known username (e.g., `?username=test_user` after running the interaction API) to see **Content-Based** results.

-----



## 🧑‍💻 Author 

  * **GitHub Repository:** `https://github.com/mdshahadathossainit/video-recommendation-assignment`
  * **Author:** `Md Shahadat Hossain`
    * Portfolio: mdshahadathossainit.github.io

  * **Date:** 27-sep-2025
<!-- end list -->

```
```
