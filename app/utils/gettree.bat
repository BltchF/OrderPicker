@echo off
chcp 65001
powershell -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; .\gettree.ps1"
pause