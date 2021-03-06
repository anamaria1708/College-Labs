package mjaksic.distributed_system_client;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class SensorServer implements Runnable {
	private AtomicBoolean server_running_flag;
	private AtomicBoolean worker_running_flag;
	private AtomicInteger active_workers;

	private ExecutorService thread_pool;

	private ServerSocket server_socket;
	private int port;

	public SensorServer(AtomicBoolean server_running_flag, int number_of_threads, int max_backlog,
			int blocking_timeout) {
		this.server_running_flag = server_running_flag;
		this.worker_running_flag = this.CreateAtomicBoolean();
		this.active_workers = this.CreateAtomicInteger();

		this.thread_pool = this.CreateThreadPool(number_of_threads);

		this.server_socket = this.CreateServerSocketWithRandomPort(max_backlog);
		this.port = this.GetLocalPort();
		this.SetSocketBlockingTimeout(blocking_timeout);
	}

	private AtomicInteger CreateAtomicInteger() {
		System.out.println("Creating atomic integer");
		return new AtomicInteger(0);
	}

	private ExecutorService CreateThreadPool(int number_of_threads) {
		System.out.println("Creating thread pool");
		return Executors.newFixedThreadPool(number_of_threads);
	}

	private AtomicBoolean CreateAtomicBoolean() {
		System.out.println("Creating atomic boolean");
		return new AtomicBoolean(true);
	}

	private ServerSocket CreateServerSocketWithRandomPort(int max_backlog) {
		ServerSocket server_socket = null;
		try {
			server_socket = new ServerSocket(0, max_backlog);
			System.out.println("Created server socket");
		} catch (IOException e) {
			e.printStackTrace();
		}
		return server_socket;
	}

	private void SetSocketBlockingTimeout(int blocking_timeout) {
		try {
			this.server_socket.setSoTimeout(blocking_timeout);
			System.out.println("Set blocking timeout");
		} catch (SocketException e) {
			e.printStackTrace();
		}
	}

	private int GetLocalPort() {
		return this.server_socket.getLocalPort();
	}

	
	
	
	@Override
	public void run() {
		this.ListenForIncomingConnections();
		this.Shutdown();
	}

	private void ListenForIncomingConnections() {
		Socket socket;
		while (this.IsRunningFlagUp()) {
			socket = this.AcceptConnectionAndCreateSocket();
			this.MakeWorkerUsingSocket(socket);
		}
	}

	private boolean IsRunningFlagUp() {
		boolean flag = this.server_running_flag.get();
		System.out.println("Server running flag is " + flag);
		return flag;
	}

	private Socket AcceptConnectionAndCreateSocket() {
		System.out.println("Listening for a connection");
		Socket socket = null;
		try {
			socket = this.server_socket.accept();
			System.out.println("Connection accepted");
		} catch (IOException e) {
			System.out.println("Listening time expired");
		}
		return socket;
	}

	private void MakeWorkerUsingSocket(Socket socket) {
		if (this.IsSocket(socket)) {
			Worker worker = new Worker(socket, this.worker_running_flag, this.active_workers);
			this.IncrementActiveWorkers();
			this.ExecuteWorker(worker);
		}
	}

	private boolean IsSocket(Socket socket) {
		if (socket != null) {
			System.out.println("Socket exists");
			return true;
		}
		return false;
	}

	private void IncrementActiveWorkers() {
		this.active_workers.getAndIncrement();
		System.out.println("Incremented workers to " + this.active_workers.get());
	}

	private void ExecuteWorker(Worker worker) {
		this.thread_pool.execute(worker);
		System.out.println("Executed a worker");
	}

	
	
	public void Shutdown() {
		this.ShutdownWorkers();
		System.out.println("Shutdown has begun...");
		while (this.IsWorkersActive()) {
			this.Sleep(5000);
		}
		this.CloseServer();
		System.out.println("Shutdown successful");
	}

	private void ShutdownWorkers() {
		this.worker_running_flag.set(false);
	}

	private boolean IsWorkersActive() {
		int active_workers = this.GetActiveWorkers();
		if (active_workers > 0) {
			System.out.println("There are still " + active_workers + " active workers");
			return true;
		}
		return false;
	}

	private int GetActiveWorkers() {
		return this.active_workers.get();
	}

	private void Sleep(int miliseconds) {
		System.out.println("Sleeping...");
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	private void CloseServer() {
		System.out.println("Closing server...");
		this.CloseServerSocket();
		this.CloseThreadPool();
	}

	private void CloseServerSocket() {
		try {
			this.server_socket.close();
			System.out.println("Server socket closed");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void CloseThreadPool() {
		this.thread_pool.shutdown();
		System.out.println("Thread pool closed");
	}

}
