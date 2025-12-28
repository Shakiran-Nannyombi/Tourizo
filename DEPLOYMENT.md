# Deployment Guide for Tourizo on Render

This guide provides step-by-step instructions for deploying the Tourizo Flask application to Render.

## Prerequisites
- A GitHub or GitLab account with the Tourizo repository.
- A [Render](https://render.com/) account.

## Deployment Steps

### 1. Configure the Application
Using SQLite on Render is simple because you don't need to provision a separate database. However, there are important persistence caveats.

> [!WARNING]
> **Data Persistence**: Render's filesystem is ephemeral on Free plans. This means any changes to your SQLite database (new users, bookings, etc.) will be **DELETED** whenever the application restarts or redeploys.

> [!TIP]
> To keep your data across restarts, you would normally need a **Render Disk** (Paid plan). For the free plan, it's best to use this for demonstrations or static sites where data is seeded during build.

### 2. Create a Web Service
The easiest way is to use the provided `render.yaml` Blueprint:
1. Click **New** and select **Blueprint**.
2. Connect your GitHub repository.
3. Render will detect the `render.yaml` file and automatically configure the Web Service with the correct build and start commands.
4. Click **Apply**.

**Manual Setup (Alternative):**
1. Click **New** and select **Web Service**.
2. Connect your repository.
3. **Environment**: `Python`
4. **Build Command**: `./build.sh`
5. **Start Command**: `gunicorn run:app`
6. Add the following **Environment Variables**:
   - `SECRET_KEY`: A long random string.
   - `FLASK_ENV`: `production`
   - `PYTHON_VERSION`: `3.12.0`

### 3. Post-Deployment: Database Initialization
By default, the `build.sh` script automatically seeds the database with demo data during every deployment. This ensures your app is ready to use immediately.

If you ever need to manually reset or re-populate the data, you can go to the **Shell** tab of your Web Service in Render and run:
```bash
python create_admin.py
python scripts/seed_tours.py
python scripts/add_demo_bookings.py
python scripts/add_demo_reviews.py
python scripts/add_image_galleries.py
```

### 4. Admin Login
Once the data is imported, you can log in as admin:
- **URL**: `https://your-app-name.onrender.com/login`
- **Email**: `devkiran256@gmail.com`
- **Password**: `admin123` (Reset this after login!)

## Troubleshooting
- **Connection Refused**: Ensure the `DATABASE_URL` is correctly set and the PostgreSQL service is active.
- **Port 10000**: Render uses port 10000 by default; Gunicorn handles this automatically.
- **Static Files**: Ensure the `static/` folder is committed to your repository.
