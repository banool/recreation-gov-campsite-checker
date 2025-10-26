import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class MonitoringService {
  constructor() {
    this.isRunning = false;
    this.config = null;
    this.checkCount = 0;
    this.lastCheckTime = null;
    this.intervalId = null;
    this.clients = []; // SSE clients
    this.lastResult = null;
  }

  /**
   * Start monitoring with the given configuration
   */
  startMonitoring(config) {
    if (this.isRunning) {
      throw new Error('Monitoring is already running');
    }

    this.isRunning = true;
    this.config = config;
    this.checkCount = 0;
    this.lastCheckTime = null;

    // Broadcast status update
    this.broadcastStatus('started');

    // Run first check immediately
    this.runCheck();

    // Schedule subsequent checks every 20 seconds
    this.intervalId = setInterval(() => {
      this.runCheck();
    }, 20000);

    return {
      success: true,
      message: 'Monitoring started',
    };
  }

  /**
   * Stop monitoring
   */
  stopMonitoring() {
    if (!this.isRunning) {
      return {
        success: false,
        message: 'Monitoring is not running',
      };
    }

    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    this.isRunning = false;
    this.broadcastStatus('stopped');

    return {
      success: true,
      message: 'Monitoring stopped',
    };
  }

  /**
   * Get current monitoring status
   */
  getStatus() {
    return {
      isRunning: this.isRunning,
      checkCount: this.checkCount,
      lastCheckTime: this.lastCheckTime,
      config: this.config,
      lastResult: this.lastResult,
    };
  }

  /**
   * Run a single check using the Python script
   */
  async runCheck() {
    if (!this.isRunning) {
      return;
    }

    this.checkCount++;
    const checkNumber = this.checkCount;

    // Broadcast checking status
    this.broadcastStatus('checking', { checkNumber });

    try {
      const result = await this.executePythonScript(this.config);
      this.lastCheckTime = new Date().toISOString();
      this.lastResult = result;

      // Check if the result indicates an error
      if (!result.success) {
        console.error('Check failed:', result.error);
        this.broadcastError(result.error, checkNumber);
        // Don't throw - let monitoring continue
        return result;
      }

      // Broadcast results
      this.broadcastResults(result, checkNumber);

      return result;
    } catch (error) {
      console.error('Error running check:', error);
      this.lastCheckTime = new Date().toISOString();
      this.broadcastError(error.message, checkNumber);
      // Don't throw - let monitoring continue
      return { success: false, error: error.message };
    }
  }

  /**
   * Execute the Python camping_runner.py script
   */
  executePythonScript(config) {
    return new Promise((resolve, reject) => {
      // Convert config to Python format
      const pythonConfig = {
        parks: config.parks,
        startDate: config.startDate,
        endDate: config.endDate,
        nights: config.nights || 1,
        weekendsOnly: config.weekendsOnly || false,
        campsiteType: config.campsiteType || null,
        campsiteIds: config.campsiteIds || [],
        excludedDates: config.excludedDates || [],
        exclusionFile: config.exclusionFile || null,
        emailNotifications: config.emailNotifications || false,
        debug: config.debug || false,
      };

      // Path to Python script
      const pythonScriptPath = path.join(
        __dirname,
        '../../python/camping_runner.py'
      );

      // Path to Python virtual environment
      const venvPythonPath = path.join(
        __dirname,
        '../../../myvenv/bin/python'
      );

      // Spawn Python process
      const pythonProcess = spawn(
        venvPythonPath,
        [pythonScriptPath, JSON.stringify(pythonConfig)],
        {
          cwd: path.join(__dirname, '../../python'),
        }
      );

      let stdout = '';
      let stderr = '';

      pythonProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
        // Log Python errors/warnings to console
        console.error('Python stderr:', data.toString());
      });

      pythonProcess.on('close', (code) => {
        try {
          const result = JSON.parse(stdout);
          // Even if Python exited with non-zero, try to parse the JSON error response
          resolve(result);
        } catch (error) {
          // If we can't parse JSON, create an error response
          resolve({
            success: false,
            error: `Failed to parse output (exit code ${code}): ${error.message}`,
            timestamp: new Date().toISOString(),
            rawOutput: stdout.substring(0, 500) // Include first 500 chars for debugging
          });
        }
      });

      pythonProcess.on('error', (error) => {
        reject(new Error(`Failed to start Python process: ${error.message}`));
      });
    });
  }

  /**
   * Add SSE client
   */
  addClient(res) {
    this.clients.push(res);

    // Send current status immediately
    if (this.isRunning) {
      this.sendToClient(res, 'status', {
        state: 'running',
        checkNumber: this.checkCount,
        timestamp: new Date().toISOString(),
      });

      // Send last result if available
      if (this.lastResult) {
        this.sendToClient(res, 'results', {
          ...this.lastResult,
          checkNumber: this.checkCount,
        });
      }
    } else {
      this.sendToClient(res, 'status', {
        state: 'stopped',
        timestamp: new Date().toISOString(),
      });
    }
  }

  /**
   * Remove SSE client
   */
  removeClient(res) {
    const index = this.clients.indexOf(res);
    if (index !== -1) {
      this.clients.splice(index, 1);
    }
  }

  /**
   * Broadcast status update to all connected clients
   */
  broadcastStatus(state, data = {}) {
    const message = {
      state,
      timestamp: new Date().toISOString(),
      ...data,
    };

    this.clients.forEach((client) => {
      this.sendToClient(client, 'status', message);
    });
  }

  /**
   * Broadcast results to all connected clients
   */
  broadcastResults(result, checkNumber) {
    const message = {
      ...result,
      checkNumber,
    };

    this.clients.forEach((client) => {
      this.sendToClient(client, 'results', message);
    });
  }

  /**
   * Broadcast error to all connected clients
   */
  broadcastError(error, checkNumber) {
    const message = {
      message: error,
      checkNumber: checkNumber || this.checkCount,
      timestamp: new Date().toISOString(),
    };

    this.clients.forEach((client) => {
      this.sendToClient(client, 'error', message);
    });
  }

  /**
   * Send message to a specific client
   */
  sendToClient(client, event, data) {
    try {
      client.write(`event: ${event}\n`);
      client.write(`data: ${JSON.stringify(data)}\n\n`);
    } catch (error) {
      console.error('Error sending to client:', error);
      this.removeClient(client);
    }
  }
}

// Singleton instance
const monitoringService = new MonitoringService();

export default monitoringService;

