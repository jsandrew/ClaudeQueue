# Claude Queue

Automatically feed tasks to Claude Code and handle quota limits. This tool helps you maintain a continuous workflow with Claude Code by managing a queue of tasks and automatically retrying when quota limits are reached.

## Features

- 📋 Queue-based task management using a simple markdown file
- ⏰ Automatic 15-minute check intervals for continuous processing
- 🔄 Smart quota limit handling with automatic retry
- 📝 Comprehensive logging of all operations
- 🖥️ macOS keyboard automation for seamless integration

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ClaudeQueue.git
cd ClaudeQueue
```

2. Make the script executable:
```bash
chmod +x claude_queue.py
```

3. (Optional) Install cliclick for better keyboard automation:
```bash
brew install cliclick
```

## Usage

### Basic Usage

1. Create a `queue.md` file in your project directory with your tasks:
```markdown
# Tasks

- [ ] Fix the login form validation bug
- [ ] Add unit tests for the user service
- [ ] Update the API documentation
- [ ] Refactor the database connection module
```

2. Start Claude Code in a terminal window

3. In another terminal, run Claude Queue:
```bash
./claude_queue.py
```

4. When prompted, switch focus to your Claude Code terminal window

5. The script will automatically:
   - Send the initial queue to Claude
   - Check the queue every 15 minutes
   - Continue processing until interrupted

### Running from a Different Directory

You can specify a repository path as an argument:
```bash
./claude_queue.py /path/to/your/project
```

### Example Workflow

1. Create your task queue:
```markdown
# Development Queue

## High Priority
- [ ] Fix critical security vulnerability in auth module
- [ ] Update dependencies to latest versions

## Medium Priority  
- [ ] Implement new user profile feature
- [ ] Add integration tests for payment system

## Low Priority
- [ ] Refactor legacy code in utils module
- [ ] Update coding style guide documentation
```

2. Start the queue processor:
```bash
./claude_queue.py
```

3. Claude Code will:
   - Read the queue.md file
   - Start working on tasks
   - Remove completed items from the queue
   - Add new tasks if issues are discovered during implementation

4. Monitor progress in the `claude_queue.log` file:
```bash
tail -f claude_queue.log
```

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
- (Optional) cliclick for improved keyboard automation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for use with [Claude Code](https://claude.ai/code) by Anthropic
- Inspired by the need for continuous AI-assisted development workflows

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the logs in `claude_queue.log` for debugging