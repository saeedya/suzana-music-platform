# Admin Setup

## Creating the first admin user

Use the `create_admin.py` script to create an admin user.

### Local development

```bash
cd backend
source venv/bin/activate
PYTHONPATH=. venv/bin/python app/core/create_admin.py
```

### Production (Railway)

**Option 1 — Railway CLI:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Run script in production environment
railway run --service suzana-music-platform python app/core/create_admin.py
```

**Option 2 — Railway dashboard:**

1. Go to railway.app
2. Open your project
3. Click on your service
4. Go to Settings → Deploy
5. Run command: python app/core/create_admin.py

**Option 3 — DigitalOcean (future production):**
```bash
# SSH into server
ssh root@your-server-ip

# Run script inside Docker container
docker exec -it backend python app/core/create_admin.py
```

## After creating admin

Admin can:
- Create, update, delete courses
- View all bookings
- Access admin-only endpoints

## Security notes

- Use a strong password (minimum 8 characters)
- Store the password in a password manager (e.g. Bitwarden)
- Never share admin credentials
- Change password immediately if compromised