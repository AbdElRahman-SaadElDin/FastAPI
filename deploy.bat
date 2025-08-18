@echo off
echo ========================================
echo Medical Reminder API - Vercel Deployment
echo ========================================
echo.

echo Checking if Vercel CLI is installed...
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Vercel CLI not found. Installing...
    npm install -g vercel
    if %errorlevel% neq 0 (
        echo Failed to install Vercel CLI. Please install Node.js first.
        pause
        exit /b 1
    )
)

echo.
echo Starting deployment...
echo.

vercel --prod

echo.
echo Deployment completed!
echo.
echo Your API is now live at the URL shown above.
echo You can access the API documentation at: https://your-domain.vercel.app/docs
echo.
pause 