Start-Process powershell -ArgumentList "uvicorn main:app --reload"
Start-Sleep -Seconds 2
Start-Process "chat.html"