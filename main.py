import requests
import time
import configparser
import os
from pystyle import Colors, Colorate

def format_message(prefix, message):
    cologreen_prefix = Colorate.Color(Colors.green, f"  [{Colors.white}!{Colors.green}]")
    return f"{cologreen_prefix}{Colors.reset} {message}"

def load_config():
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    
    if not os.path.exists(config_file):
        print(format_message("!", "Config file not found, creating new one..."))
        token = input(f"   {Colors.green}┌───({Colors.reset}{os.getenv('COMPUTERNAME', 'unknown')}{Colors.green})\n   └──$ {Colors.reset}Enter your Discord token: ")
        interval = input(f"{Colors.green}   └──$ {Colors.reset}Enter the rotation interval (in seconds): ")
        guild_ids = input(f"{Colors.green}   └──$ {Colors.reset}Enter server IDs (comma-separated): ")
        config['SETTINGS'] = {
            'token': token.strip(),
            'interval': interval.strip(),
            'guild_ids': guild_ids.strip()
        }
        
        with open(config_file, 'w') as f:
            config.write(f)
        print(format_message("!", "Configuration saved to config.ini"))
    else:
        config.read(config_file)
        
        if 'SETTINGS' not in config or not all(key in config['SETTINGS'] for key in ['token', 'interval', 'guild_ids']):
            print(format_message("!", "Incomplete configuration, please fill in the details..."))
            token = input(f"   {Colors.green}┌───({Colors.reset}{os.getenv('COMPUTERNAME', 'unknown')}{Colors.green})\n   └──$ {Colors.reset}Enter your Discord token: ")
            interval = input(f"{Colors.green}   └──$ {Colors.reset}Enter the rotation interval (in seconds): ")
            guild_ids = input(f"{Colors.green}   └──$ {Colors.reset}Enter server IDs (comma-separated): ")
            
            config['SETTINGS'] = {
                'token': token.strip(),
                'interval': interval.strip(),
                'guild_ids': guild_ids.strip()
            }
            
            with open(config_file, 'w') as f:
                config.write(f)
            print(format_message("!", "Configuration updated in config.ini"))
    
    return config['SETTINGS']['token'], float(config['SETTINGS']['interval']), config['SETTINGS']['guild_ids'].split(',')

def change_clan(token, guild_id):
    url = "https://discord.com/api/v9/users/@me/clan"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "identity_guild_id": guild_id,
        "identity_enabled": True
    }
    
    try:
        response = requests.put(url, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'clan' in data and data['clan']['identity_guild_id'] == guild_id:
                return True, data['clan']['tag']
            else:
                return False, "Clan not updated"
        else:
            return False, f"API Error: {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = """
          ▄████  ██░ ██    ▄▄▄█████▓ ▄▄▄        ▄████  ██▀███   ▒█████  ▄▄▄█████▓ ▄▄▄     ▄▄▄█████▓▓█████ 
         ██▒ ▀█▒▓██░ ██▒   ▓  ██▒ ▓▒▒████▄     ██▒ ▀█▒▓██ ▒ ██▒▒██▒  ██▒▓  ██▒ ▓▒▒████▄   ▓  ██▒ ▓▒▓█   ▀ 
        ▒██░▄▄▄░▒██▀▀██░   ▒ ▓██░ ▒░▒██  ▀█▄  ▒██░▄▄▄░▓██ ░▄█ ▒▒██░  ██▒▒ ▓██░ ▒░▒██  ▀█▄ ▒ ▓██░ ▒░▒███   
        ░▓█  ██▓░▓█ ░██    ░ ▓██▓ ░ ░██▄▄▄▄██ ░▓█  ██▓▒██▀▀█▄  ▒██   ██░░ ▓██▓ ░ ░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄ 
        ░▒▓███▀▒░▓█▒░██▓     ▒██▒ ░  ▓█   ▓██▒░▒▓███▀▒░██▓ ▒██▒░ ████▓▒░  ▒██▒ ░  ▓█   ▓██▒ ▒██▒ ░ ░▒████▒
         ░▒   ▒  ▒ ░░▒░▒     ▒ ░░    ▒▒   ▓▒█░ ░▒   ▒ ░ ▒▓ ░▒▓░░ ▒░▒░▒░   ▒ ░░    ▒▒   ▓▒█░ ▒ ░░   ░░ ▒░ ░
          ░   ░  ▒ ░▒░ ░       ░      ▒   ▒▒ ░  ░   ░   ░▒ ░ ▒░  ░ ▒ ▒░     ░      ▒   ▒▒ ░   ░     ░ ░  ░
        ░ ░   ░  ░  ░░ ░     ░        ░   ▒   ░ ░   ░   ░░   ░ ░ ░ ░ ▒    ░        ░   ▒    ░         ░   
              ░  ░  ░  ░                  ░  ░      ░    ░         ░ ░                 ░  ░           ░  
    """
    print(Colorate.Vertical(Colors.green_to_white, banner))
    print(format_message("!", "Made by NightKikko for discord.gg/guildshub"))
    
    token, interval, guild_ids = load_config()
    guild_ids = [gid.strip() for gid in guild_ids if gid.strip()]
    
    if not guild_ids:
        print(format_message("!", "No valid server IDs provided. Exiting."))
        return
    
    print(format_message("!", f"Loaded {len(guild_ids)} servers. Interval: {interval}s"))
    
    while True:
        for guild_id in guild_ids:
            success, message = change_clan(token, guild_id)
            if success:
                print(format_message("!", f"Tag changed to {message} (ID: {guild_id})"))
            else:
                print(format_message("!", message))
            time.sleep(interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(format_message("!", "Clan rotator stopped by user."))