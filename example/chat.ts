import { spawn } from 'child_process';
import * as readline from 'readline';

/**
 * A TypeScript client that launches the tau Python module and performs a chat.
 */
class TauChatClient {
  private pythonProcess: ReturnType<typeof spawn>;
  private rl: readline.Interface;
  private isReady: boolean = false;

  constructor() {
    // Create readline interface for user input
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    // Spawn the Python process
    this.pythonProcess = spawn('uv', ['run', 'tau-chat', '-c', '../config.json'], {
      cwd: process.cwd(),
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: false,
    });

    // Handle Python process stdout
    this.pythonProcess.stdout?.on('data', (data: Buffer) => {
      const output = data.toString().trim();
      if (output) {
        console.log('\nAssistant: ', output);
        this.promptUser();
      } else {
        console.log('Empty stdout data received');
      }
    });

    // Handle Python process stderr
    this.pythonProcess.stderr?.on('data', (data: Buffer) => {
      const output = data.toString().trim();
      if (output) {
        // Only log debug/info messages, not errors
        if (!output.includes('ERROR')) {
          console.log('Debug: ', output);
        } else {
          console.error('Error: ', output);
        }
      }
    });

    // Handle Python process exit
    this.pythonProcess.on('close', (code: number | null) => {
      this.rl.close();
      process.exit(0);
    });

    // Set a small delay to ensure Python process is ready
    setTimeout(() => {
      this.isReady = true;
      console.log('Tau Chat Client');
      console.log('Type your message or \\q to quit');
      this.promptUser();
    }, 5000);
  }

  /**
   * Prompt the user for input
   */
  private promptUser(): void {
    if (!this.isReady) return;

    this.rl.question('You: ', (input: string) => {
      if (input.trim() === '\\q') {
        // Send quit command to Python process
        this.pythonProcess.stdin?.write('\\q\n');
        this.rl.close();
        setTimeout(() => process.exit(0), 500);
        return;
      }

      if (input.trim()) {
        // Send user input to Python process and ensure it's flushed
        if (this.pythonProcess.stdin?.writable) {
          this.pythonProcess.stdin.write(input + '\n', (error) => {
            if (error) {
              console.error('Error writing to stdin: ', error);
            }
          });
        }
      } else {
        this.promptUser();
      }
    });
  }
}

// Start the chat client
new TauChatClient();
