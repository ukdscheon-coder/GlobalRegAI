@echo off
title GlobalRegAI — Stop

echo  [GlobalRegAI] Stopping services...
docker compose down
echo  All services stopped.
pause
