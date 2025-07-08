#!/usr/bin/env python3
"""
Claude Queue - Automatically feed tasks to Claude Code and handle quota limits
"""

import os
import re
import time
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

class ClaudeQueue:
    def __init__(self, repo_path=None):
        if repo_path:
            self.repo_path = Path(repo_path)
            self.queue_file = self.repo_path / "queue.md"
            self.log_file = self.repo_path / "claude_queue.log"
        else:
            self.repo_path = Path.cwd()
            self.queue_file = Path("queue.md")
            self.log_file = Path("claude_queue.log")
        
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, "a") as f:
            f.write(log_message + "\n")
    
    def read_queue(self):
        """Read and return the queue markdown content"""
        if not self.queue_file.exists():
            self.log(f"Queue file {self.queue_file} not found!")
            return None
        
        with open(self.queue_file, "r") as f:
            content = f.read()
        
        return content
    
    def send_to_claude(self, message):
        """Send message to Claude using keyboard automation"""
        try:
            # Copy message to clipboard
            subprocess.run(["pbcopy"], input=message, text=True, check=True)
            
            # Give user time to focus Claude terminal
            if not hasattr(self, '_first_run'):
                print("Focus your Claude Code terminal window now...")
                time.sleep(5)
                self._first_run = True
            
            # Use keyboard automation to paste
            # First try with osascript key events
            script = '''
            tell application "System Events"
                key code 9 using command down
                delay 0.1
                key code 36
            end tell
            '''
            
            subprocess.run(["osascript", "-e", script], check=True)
            
            self.log(f"Sent to Claude: {message[:50]}...")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"Error with osascript: {e}")
            # Fallback: try cliclick if available
            try:
                subprocess.run(["cliclick", "kp:cmd+v"], check=True)
                subprocess.run(["cliclick", "kp:return"], check=True)
                self.log(f"Sent to Claude via cliclick: {message[:50]}...")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.log("cliclick not available, install with: brew install cliclick")
                return False
        except Exception as e:
            self.log(f"Error in send_to_claude: {e}")
            return False
    
    def parse_quota_reset_time(self, claude_output):
        """Parse Claude's quota reset message and return wait time in seconds"""
        # Look for patterns like "limits reset in 2 hours" or "quota resets at 14:30"
        patterns = [
            r"limits reset in (\d+) hours?",
            r"quota resets? in (\d+) hours?",
            r"try again in (\d+) hours?",
            r"limits reset in (\d+) minutes?",
            r"quota resets? in (\d+) minutes?",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, claude_output, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                if "hour" in pattern:
                    return value * 3600  # Convert hours to seconds
                elif "minute" in pattern:
                    return value * 60   # Convert minutes to seconds
        
        # Default to 3 hours if we can't parse
        self.log("Could not parse quota reset time, defaulting to 3 hours")
        return 3 * 3600
    
    def wait_for_quota_reset(self, wait_seconds):
        """Wait until quota resets"""
        reset_time = datetime.now() + timedelta(seconds=wait_seconds)
        self.log(f"Waiting until {reset_time.strftime('%H:%M:%S')} for quota reset...")
        
        while datetime.now() < reset_time:
            remaining = (reset_time - datetime.now()).total_seconds()
            if remaining > 0:
                time.sleep(min(60, remaining))  # Sleep in 1-minute intervals
    
    def run(self):
        """Main execution loop"""
        self.log("Starting Claude Queue...")
        
        # Read the queue
        queue_content = self.read_queue()
        if not queue_content:
            return
        
        # Process queue content into numbered tasks
        tasks = []
        for line_num, line in enumerate(queue_content.strip().split('\n'), 1):
            line = line.strip()
            if line:
                tasks.append(f"{line_num}. {line}")
        
        # Create simple message
        initial_message = f"Process these tasks one by one: {'; '.join(tasks)}"
        if not self.send_to_claude(initial_message):
            self.log("Failed to send initial queue to Claude")
            return
        
        self.log("Queue sent to Claude. Starting 15-minute check loop...")
        
        # Automated hourly check loop
        while True:
            try:
                # Wait 15 minutes
                self.log("Waiting 15 minutes before next check...")
                time.sleep(900)  # 15 minutes = 900 seconds
                
                # Check if Claude has items left in queue
                self.log("Checking if Claude has remaining tasks...")
                if not self.send_to_claude("Do you have any remaining tasks in your queue? Please respond with only 'yes' or 'no'."):
                    self.log("Failed to send status check to Claude")
                    continue
                
                # Wait a moment for Claude to respond, then ask user
                time.sleep(5)
                
                # Get user input about Claude's response
                claude_response = input("\\nWhat did Claude respond? (yes/no/q to quit): ").strip().lower()
                
                if claude_response == 'q':
                    self.log("Exiting Claude Queue")
                    break
                elif claude_response == 'no':
                    self.log("Claude reports no remaining tasks. Shutting down.")
                    break
                elif claude_response == 'yes':
                    self.log("Claude has remaining tasks. Sending continue command...")
                    if not self.send_to_claude("continue"):
                        self.log("Failed to send continue command")
                        break
                    self.log("Sent 'continue' command to Claude")
                else:
                    self.log("Invalid response. Assuming tasks remain and continuing...")
                    if not self.send_to_claude("continue"):
                        self.log("Failed to send continue command")
                        break
                
            except KeyboardInterrupt:
                self.log("Interrupted by user")
                break
            except Exception as e:
                self.log(f"Error in main loop: {e}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    """Main entry point"""
    repo_path = None
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    
    queue = ClaudeQueue(repo_path)
    
    try:
        queue.run()
    except KeyboardInterrupt:
        print("\\nShutting down...")

if __name__ == "__main__":
    main()