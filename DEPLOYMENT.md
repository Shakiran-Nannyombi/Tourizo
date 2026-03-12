# Deployment Guide for Tourizo on Render

This guide provides step-by-step instructions for deploying the Tourizo Flask application to Render with SQLite.

## Prerequisites
- A GitHub or GitLab account with the Tourizo repository.
- A [Render](https://render.com/) account.

## Deployment Steps

### 1. Create a Web Service on Render
The easiest way is to use the provided `render.yaml` Blueprint:
1. Click **New** and select **Blueprint**.
2. Connect your GitHub repository.
3. Render will detect the `render.yaml` file and automatically configure the Web Service.
4. Click **Apply**.

**Manual Setup (Alternative):**
1. Click **New** and select **Web Service**.
2. Connect your repository.
3. **Environment**: `Python`
4. **Build Command**: `./build.sh`
5. **Start Command**: `gunicorn wsgi:app`

### 2. Configure Environment Variables
Add the following **Environment Variables** in your Render Dashboard:
- `SECRET_KEY`: A long random string (generate with: `python3 -c "import secrets; print(secrets.token_hex(32))"`)
- `FLASK_ENV`: `production`
- `PYTHON_VERSION`: `3.12.0`

> [!IMPORTANT]
> **Start Command**: Ensure your Render Start Command is set to `gunicorn wsgi:app`. Do NOT use `gunicorn app:app` as it will conflict with the `app/` directory and fail to start.

> [!TIP]
> **Database**: SQLite is used by default. Data persists in the `instance/` directory across deployments.

### 3. Deploy
1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Configure SQLite deployment"
   git push origin main
   ```
2. Render will automatically detect the push and start building.
3. Monitor the deployment logs for:
   - ✅ Database migrations running (`flask db upgrade`)
   - ✅ Demo data seeding
   - ✅ Application starting with Gunicorn

### 4. Post-Deployment: Verify Database
The `build.sh` script automatically:
- Runs database migrations to create all tables
- Seeds the database with demo data (tours, categories, users, etc.)

### 5. Admin Login
Once deployed, you can log in as admin:
- **URL**: `https://your-app-name.onrender.com/login`
- **Email**: `devkiran256@gmail.com`
- **Password**: `admin123` (Reset this after login!)

## Troubleshooting
- **"no such table" errors**: Ensure migrations ran successfully during build. Check Render logs for `flask db upgrade` output.
- **Port 10000**: Render uses port 10000 by default; Gunicorn handles this automatically.
- **Static Files**: Ensure the `static/` folder is committed to your repository.

## Database Management
- **View Data**: Download the SQLite database file from Render's file system or use the Render Shell to inspect it.
- **Direct Access**: Use the Render Shell tab to run database queries or scripts.
- **Backups**: Ensure the `instance/` directory is included in your version control or backed up regularly.
