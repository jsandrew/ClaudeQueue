# Claude Queue

Automatically feed tasks to Claude Code and handle quota limits. This tool helps you maintain a continuous workflow with Claude Code by managing a queue of tasks and automatically retrying when quota limits are reached.

## Features

- 📋 Queue-based task management using a simple markdown file
- ⏰ Automatic 15-minute check intervals for continuous processing
- 🔄 Smart quota limit handling with automatic retry

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jsandrew/ClaudeQueue.git
cd ClaudeQueue
```

2. Make the script executable:
```bash
chmod +x claude_queue.py
```

## Usage

### Basic Usage

1. Create a `queue.md` file in your project directory with your tasks:
```markdown
# Tasks
- Fix the login form validation bug
- Add unit tests for the user service
- Update the API documentation
- Refactor the database connection module
```

2. Start Claude Code in a terminal window

3. In another terminal, run Claude Queue:
```bash
./claude_queue.py /path/to/your/project
```

4. When prompted, switch focus to your Claude Code terminal window

5. The script will automatically:
   - Send the initial queue to Claude
   - Check the queue every 15 minutes
   - Continue processing until interrupted

## How It Works

1. **Queue Management**: Tasks are stored in a `queue.md` markdown file that Claude can read and update
2. **Automation**: Uses macOS keyboard automation (AppleScript/cliclick) to send messages to Claude Code
3. **Continuous Processing**: Checks the queue every 15 minutes to ensure continuous task processing
4. **Smart Retries**: Detects quota limit messages and automatically waits before retrying
5. **Logging**: All operations are logged to `claude_queue.log` for tracking and debugging

## Requirements

- Python 3.6+
- macOS (for keyboard automation)
- Claude Code CLI installed and running

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
