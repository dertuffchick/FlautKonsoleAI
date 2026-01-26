#!/usr/bin/env python3
import os
import sys
import json
import requests
import platform
import argparse
import subprocess
import atexit
from datetime import datetime
from pathlib import Path

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    class Colors:
        MAGENTA = RED = CYAN = GREEN = YELLOW = BLUE = WHITE = RESET = BOLD = ""
    Fore = Back = Style = Colors()

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import TerminalFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

if platform.system() == "Windows":
    try:
        import pyreadline3 as readline
        READLINE_AVAILABLE = True
    except ImportError:
        READLINE_AVAILABLE = False
        print(f"{Fore.YELLOW}⚠️ Для улучшенного ввода установите: pip install pyreadline3{Style.RESET_ALL}")
else:
    try:
        import readline
        READLINE_AVAILABLE = True
    except ImportError:
        READLINE_AVAILABLE = False

API_KEY = "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"

class FlautKonsoleAi:
    def __init__(self):
        self.os_type = platform.system()
        self.history_file = Path.home() / ".flaut_history.json"
        self.session_history = []
        self.setup_directories()
        self.load_history()
        self.setup_readline()

    def setup_directories(self):
        self.history_file.parent.mkdir(exist_ok=True)

    def load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.session_history = json.load(f)
                    if len(self.session_history) > 100:
                        self.session_history = self.session_history[-100:]
            except:
                self.session_history = []

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_history[-100:], f, ensure_ascii=False, indent=2)
        except:
            pass

    def setup_readline(self):
        if READLINE_AVAILABLE and self.os_type != "Windows":
            histfile = os.path.join(os.path.expanduser("~"), ".flaut_python_history")
            try:
                readline.read_history_file(histfile)
                readline.set_history_length(1000)
            except FileNotFoundError:
                pass
            atexit.register(readline.write_history_file, histfile)

    def print_banner(self):
        os.system('cls' if self.os_type == 'Windows' else 'clear')
        
        banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}
    ███████╗██╗      █████╗ ██╗   ██╗████████╗
    ██╔════╝██║     ██╔══██╗██║   ██║╚══██╔══╝
    █████╗  ██║     ███████║██║   ██║   ██║   
    ██╔══╝  ██║     ██╔══██║██║   ██║   ██║   
    ██║     ███████╗██║  ██║╚██████╔╝   ██║   
    ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   
    
    ██╗  ██╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██╗     ███████╗
    ██║ ██╔╝██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██║     ██╔════╝
    █████╔╝ ██║   ██║██╔██╗ ██║███████╗██║   ██║██║     █████╗  
    ██╔═██╗ ██║   ██║██║╚██╗██║╚════██║██║   ██║██║     ██╔══╝  
    ██║  ██╗╚██████╔╝██║ ╚████║███████║╚██████╔╝███████╗███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝
    
    {Fore.RED}╔══════════════════════════════════════════════════════╗
    ║{Fore.CYAN}         FlautKonsoleAI • OpenRouter API           {Fore.RED}║
    ╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
        
        status = f"""
{Fore.BLUE}┌──────────────────────────────────────────────────────┐
│{Fore.GREEN}  ⚡ СИСТЕМА: {self.os_type:25}                  {Fore.BLUE}│
│{Fore.GREEN}  🤖 ИИ: OpenRouter GPT-3.5-Turbo             {Fore.BLUE}│
│{Fore.GREEN}  💾 ИСТОРИЯ: {len(self.session_history):22} записей  {Fore.BLUE}│
│{Fore.GREEN}  🕒 ВРЕМЯ: {datetime.now().strftime('%H:%M:%S'):23}          {Fore.BLUE}│
└──────────────────────────────────────────────────────┘{Style.RESET_ALL}
"""
        print(status)
        
        commands = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════╗
║{Fore.RED}                    🎮 КОМАНДЫ:                       {Fore.MAGENTA}║
║{Fore.CYAN}    /clear   {Fore.YELLOW}- очистить терминал              {Fore.MAGENTA}║
║{Fore.CYAN}    /history {Fore.YELLOW}- показать историю              {Fore.MAGENTA}║
║{Fore.CYAN}    /save    {Fore.YELLOW}- сохранить историю             {Fore.MAGENTA}║
║{Fore.CYAN}    /status  {Fore.YELLOW}- диагностика системы           {Fore.MAGENTA}║
║{Fore.CYAN}    /new     {Fore.YELLOW}- новый диалог                  {Fore.MAGENTA}║
║{Fore.CYAN}    /file    {Fore.YELLOW}- работа с файлами              {Fore.MAGENTA}║
║{Fore.CYAN}    /cmd     {Fore.YELLOW}- выполнить команду ОС          {Fore.MAGENTA}║
║{Fore.CYAN}    /exit    {Fore.YELLOW}- завершить сессию              {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(commands)
        
        print(f"{Fore.RED}{'═'*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}💬 ВВЕДИТЕ ЗАПРОС ИЛИ КОМАНДУ...{Style.RESET_ALL}")
        print(f"{Fore.RED}{'═'*60}{Style.RESET_ALL}\n")

    def ask_openrouter(self, prompt: str) -> str:
        print(f"{Fore.CYAN}[OpenRouter] Обработка...{Style.RESET_ALL}", end=" ", flush=True)
        
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://flautai.com",
                "X-Title": "FlautKonsoleAI"
            }
            
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1500,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result["choices"]:
                    print(f"{Fore.GREEN}✅{Style.RESET_ALL}")
                    return result["choices"][0]["message"]["content"]
            
            print(f"{Fore.RED}❌ Код: {response.status_code}{Style.RESET_ALL}")
            return self.fallback_response(prompt)
            
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}❌ Таймаут{Style.RESET_ALL}")
            return "Ошибка: превышено время ожидания ответа от API."
        except Exception as e:
            print(f"{Fore.RED}❌ Ошибка: {str(e)[:50]}{Style.RESET_ALL}")
            return self.fallback_response(prompt)

    def fallback_response(self, prompt: str) -> str:
        responses = {
            "привет": f"{Fore.GREEN}🤖 Привет! Я FlautKonsoleAI!{Style.RESET_ALL}",
            "как дела": f"{Fore.GREEN}🌟 Всё отлично! Работаю на полную!{Style.RESET_ALL}",
            "кто ты": f"{Fore.GREEN}⚡ Я - FlautKonsoleAI! ИИ-ассистент в консоли!{Style.RESET_ALL}",
            "помощь": f"{Fore.CYAN}📖 КОМАНДЫ: /clear, /history, /save, /status, /new, /file, /cmd, /exit{Style.RESET_ALL}",
        }
        
        prompt_lower = prompt.lower()
        for key in responses:
            if key in prompt_lower:
                return responses[key]
        
        import random
        fallback = [
            f"🤖 Я получил ваш запрос: '{prompt[:50]}...'",
            f"💾 Сохраняю запрос для дальнейшего анализа...",
            f"⚡ Принято! Обрабатываю информацию...",
            f"✨ Интересный вопрос! К сожалению, API временно недоступен.",
            f"🌐 Пытаюсь подключиться к ИИ... Временные технические проблемы."
        ]
        return random.choice(fallback)

    def process_command(self, command: str):
        cmd = command.lower().strip()
        
        if cmd == "/exit":
            return False, None
        
        elif cmd == "/clear":
            self.print_banner()
            return True, None
        
        elif cmd == "/history":
            if not self.session_history:
                return True, f"{Fore.YELLOW}📭 История пуста{Style.RESET_ALL}"
            
            output = [f"{Fore.MAGENTA}📜 ИСТОРИЯ ДИАЛОГА:{Style.RESET_ALL}"]
            for i, msg in enumerate(self.session_history[-10:], 1):
                time = datetime.fromisoformat(msg.get("time", "")).strftime("%H:%M") if msg.get("time") else "--:--"
                icon = "👤" if msg["role"] == "user" else "🤖"
                color = Fore.CYAN if msg["role"] == "user" else Fore.GREEN
                text = msg["content"][:40] + "..." if len(msg["content"]) > 40 else msg["content"]
                output.append(f"{color}{i:2d}. [{time}] {icon} {text}{Style.RESET_ALL}")
            
            return True, "\n".join(output)
        
        elif cmd == "/save":
            self.save_history()
            return True, f"{Fore.GREEN}✅ История сохранена{Style.RESET_ALL}"
        
        elif cmd == "/status":
            status_info = [
                f"{Fore.MAGENTA}📊 ДИАГНОСТИКА:{Style.RESET_ALL}",
                f"{Fore.CYAN}🖥️  ОС: {self.os_type}{Style.RESET_ALL}",
                f"{Fore.CYAN}🤖 API: OpenRouter GPT-3.5-Turbo{Style.RESET_ALL}",
                f"{Fore.CYAN}💾 Сообщений: {len(self.session_history)}{Style.RESET_ALL}",
                f"{Fore.CYAN}⏰ Время: {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}",
                f"{Fore.CYAN}📁 Файл истории: {self.history_file}{Style.RESET_ALL}"
            ]
            return True, "\n".join(status_info)
        
        elif cmd == "/new":
            self.session_history = []
            return True, f"{Fore.GREEN}✅ Новый диалог начат{Style.RESET_ALL}"
        
        elif cmd.startswith("/file "):
            return self.handle_file_command(command[6:])
        
        elif cmd.startswith("/cmd "):
            return self.handle_system_command(command[5:])
        
        elif cmd.startswith("/"):
            return True, f"{Fore.RED}❌ Неизвестная команда{Style.RESET_ALL}"
        
        return None, None

    def handle_file_command(self, arg: str):
        args = arg.strip().split()
        if not args:
            return True, f"{Fore.YELLOW}Использование: /file read <путь> или /file write <путь> <текст>{Style.RESET_ALL}"
        
        action = args[0].lower()
        
        if action == "read" and len(args) > 1:
            path = args[1]
            try:
                if path == "~":
                    path = str(Path.home())
                elif path.startswith("~/"):
                    path = str(Path.home() / path[2:])
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return True, f"{Fore.GREEN}📖 Файл {path}:\n{Fore.CYAN}{content}{Style.RESET_ALL}"
            except Exception as e:
                return True, f"{Fore.RED}❌ Ошибка чтения: {e}{Style.RESET_ALL}"
        
        elif action == "write" and len(args) > 2:
            path = args[1]
            text = " ".join(args[2:])
            try:
                if path == "~":
                    path = str(Path.home())
                elif path.startswith("~/"):
                    path = str(Path.home() / path[2:])
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
                    return True, f"{Fore.GREEN}✅ Файл сохранен: {path}{Style.RESET_ALL}"
            except Exception as e:
                return True, f"{Fore.RED}❌ Ошибка записи: {e}{Style.RESET_ALL}"
        
        return True, f"{Fore.YELLOW}Использование: /file read <путь> или /file write <путь> <текст>{Style.RESET_ALL}"

    def handle_system_command(self, cmd: str):
        if not cmd:
            return True, f"{Fore.YELLOW}Введите команду для выполнения{Style.RESET_ALL}"
        
        print(f"{Fore.YELLOW}⚠️ Выполнить команду ОС: {cmd} ? (y/n): {Style.RESET_ALL}", end="")
        confirm = input().lower().strip()
        
        if confirm != 'y':
            return True, f"{Fore.YELLOW}❌ Команда отменена{Style.RESET_ALL}"
        
        try:
            if self.os_type == "Windows":
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            output = f"{Fore.GREEN}✅ Команда выполнена{Style.RESET_ALL}\n"
            if result.stdout:
                output += f"{Fore.CYAN}STDOUT:\n{result.stdout}{Style.RESET_ALL}"
            if result.stderr:
                output += f"{Fore.RED}STDERR:\n{result.stderr}{Style.RESET_ALL}"
            if result.returncode != 0:
                output += f"{Fore.YELLOW}Код возврата: {result.returncode}{Style.RESET_ALL}"
            
            return True, output
        except subprocess.TimeoutExpired:
            return True, f"{Fore.RED}❌ Таймаут выполнения команды{Style.RESET_ALL}"
        except Exception as e:
            return True, f"{Fore.RED}❌ Ошибка выполнения: {e}{Style.RESET_ALL}"

    def highlight_code(self, text: str) -> str:
        if not PYGMENTS_AVAILABLE:
            return text
        
        lines = text.split('\n')
        highlighted_lines = []
        in_code_block = False
        current_lang = ""
        code_block = []
        
        for line in lines:
            if line.strip().startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    current_lang = line.strip()[3:].strip()
                    if not current_lang:
                        current_lang = "text"
                else:
                    try:
                        lexer = get_lexer_by_name(current_lang)
                        highlighted = highlight('\n'.join(code_block), lexer, TerminalFormatter())
                        highlighted_lines.append(highlighted.rstrip('\n'))
                    except:
                        highlighted_lines.extend(code_block)
                    
                    in_code_block = False
                    code_block = []
                    current_lang = ""
            elif in_code_block:
                code_block.append(line)
            else:
                highlighted_lines.append(line)
        
        if in_code_block and code_block:
            try:
                lexer = get_lexer_by_name(current_lang)
                highlighted = highlight('\n'.join(code_block), lexer, TerminalFormatter())
                highlighted_lines.append(highlighted.rstrip('\n'))
            except:
                highlighted_lines.extend(code_block)
        
        return '\n'.join(highlighted_lines)

    def interactive_mode(self):
        self.print_banner()
        
        while True:
            try:
                user_input = input(f"\n{Fore.MAGENTA}⚡ ВВОД: {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                cmd_result, cmd_output = self.process_command(user_input)
                
                if cmd_result is False:
                    print(f"{Fore.GREEN}👋 Завершение сессии...{Style.RESET_ALL}")
                    break
                elif cmd_result is True and cmd_output:
                    print(f"\n{cmd_output}")
                    continue
                elif cmd_result is None:
                    self.session_history.append({
                        "role": "user",
                        "content": user_input,
                        "time": datetime.now().isoformat()
                    })
                    
                    response = self.ask_openrouter(user_input)
                    highlighted_response = self.highlight_code(response)
                    
                    print(f"\n{Fore.RED}🤖 ИИ: {Style.RESET_ALL}{highlighted_response}")
                    
                    self.session_history.append({
                        "role": "assistant",
                        "content": response,
                        "time": datetime.now().isoformat()
                    })
                    
                    if len(self.session_history) % 3 == 0:
                        self.save_history()
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⚠️ Прервано{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Ошибка: {str(e)[:50]}{Style.RESET_ALL}")
        
        self.save_history()
        print(f"\n{Fore.MAGENTA}{'═'*60}{Style.RESET_ALL}")
        print(f"{Fore.RED}🤖 FlautKonsoleAI • OpenRouter API{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'═'*60}{Style.RESET_ALL}")

    def single_query(self, query: str):
        print(f"{Fore.CYAN}Запрос: {query}{Style.RESET_ALL}\n")
        
        response = self.ask_openrouter(query)
        highlighted_response = self.highlight_code(response)
        
        print(f"{Fore.GREEN}Ответ:{Style.RESET_ALL}\n{highlighted_response}\n")
        
        self.session_history.append({
            "role": "user",
            "content": query,
            "time": datetime.now().isoformat()
        })
        self.session_history.append({
            "role": "assistant",
            "content": response,
            "time": datetime.now().isoformat()
        })
        
        self.save_history()

def check_dependencies():
    missing = []
    
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    try:
        import colorama
    except ImportError:
        missing.append("colorama")
    
    if missing:
        print(f"{Fore.RED}❌ Отсутствуют зависимости:{Style.RESET_ALL}")
        for dep in missing:
            print(f"   - {dep}")
        print(f"\n{Fore.YELLOW}📦 Установите: pip install {' '.join(missing)}{Style.RESET_ALL}")
        return False
    
    return True

def main():
    if not check_dependencies():
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="FlautKonsoleAI - консольный ИИ ассистент")
    parser.add_argument("-q", "--query", help="Выполнить одиночный запрос")
    
    args = parser.parse_args()
    
    ai = FlautKonsoleAi()
    
    if args.query:
        ai.single_query(args.query)
    else:
        ai.interactive_mode()

if __name__ == "__main__":
    main()