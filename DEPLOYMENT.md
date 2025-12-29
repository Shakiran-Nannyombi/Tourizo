# Deployment Guide for Tourizo on Render

This guide provides step-by-step instructions for deploying the Tourizo Flask application to Render with Supabase PostgreSQL.

## Prerequisites
- A GitHub or GitLab account with the Tourizo repository.
- A [Render](https://render.com/) account.
- A [Supabase](https://supabase.com/) account with a PostgreSQL database created.

## Deployment Steps

### 1. Set Up Supabase Database
1. Go to [Supabase Dashboard](https://supabase.com/dashboard).
2. Create a new project or use an existing one.
3. Navigate to **Project Settings** → **Database**.
4. Copy the **Connection String** (URI format):
   - Use the **Transaction Pooler** connection string (recommended for serverless/cloud deployments).
   - Format: `postgresql://postgres.yourproject:password@aws-0-region.pooler.supabase.com:6543/postgres`
5. **Important**: Replace `[YOUR-PASSWORD]` with your actual database password.

### 2. Create a Web Service on Render
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

### 3. Configure Environment Variables
Add the following **Environment Variables** in your Render Dashboard:
- `SECRET_KEY`: A long random string (generate with: `python3 -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL`: Your Supabase connection string from Step 1
- `FLASK_ENV`: `production`
- `PYTHON_VERSION`: `3.12.0`

> [!IMPORTANT]
> **Start Command**: Ensure your Render Start Command is set to `gunicorn wsgi:app`. Do NOT use `gunicorn app:app` as it will conflict with the `app/` directory and fail to start.

> [!TIP]
> **Database Persistence**: Unlike SQLite on Render's ephemeral filesystem, Supabase PostgreSQL provides **permanent data persistence** across deployments and restarts.

### 4. Deploy
1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Configure Supabase deployment"
   git push origin main
   ```
2. Render will automatically detect the push and start building.
3. Monitor the deployment logs for:
   - ✅ Database connection successful
   - ✅ Migrations running (`flask db upgrade`)
   - ✅ Demo data seeding
   - ✅ Application starting with Gunicorn

### 5. Post-Deployment: Verify Database
The `build.sh` script automatically:
- Runs database migrations to create all tables
- Seeds the database with demo data (tours, categories, users, etc.)

You can verify the tables were created by checking your Supabase **Table Editor**.

If you ever need to manually re-seed data, use the **Shell** tab in Render:
```bash
python create_admin.py
python scripts/seed_tours.py
python scripts/add_demo_bookings.py
python scripts/add_demo_reviews.py
python scripts/add_image_galleries.py
```

### 6. Admin Login
Once deployed, you can log in as admin:
- **URL**: `https://your-app-name.onrender.com/login`
- **Email**: `devkiran256@gmail.com`
- **Password**: `admin123` (Reset this after login!)

## Troubleshooting
- **Connection Refused**: Verify the `DATABASE_URL` is correctly set in Render Environment Variables.
- **"no such table" errors**: Ensure migrations ran successfully during build. Check Render logs for `flask db upgrade` output.
- **Network unreachable**: Ensure you're using the correct Supabase connection string (Transaction Pooler recommended).
- **Port 10000**: Render uses port 10000 by default; Gunicorn handles this automatically.
- **Static Files**: Ensure the `static/` folder is committed to your repository.

## Database Management
- **View Data**: Use Supabase Table Editor to browse and edit data.
- **Backups**: Supabase provides automatic backups (check your plan details).
- **Direct Access**: Use the Supabase SQL Editor for direct database queries.
