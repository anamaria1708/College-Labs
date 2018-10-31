package mjaksic.distributed_system_client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class Worker implements Runnable {
	
	private Socket client_socket;
	private AtomicBoolean is_running;
	private AtomicInteger active_workers;

	private BufferedReader reader;
	private PrintWriter writer;

	public Worker(Socket client_socket, AtomicBoolean is_running, AtomicInteger active_workers) {
		this.client_socket = client_socket;
		this.is_running = is_running;
		this.active_workers = active_workers;

		this.reader = this.CreateReader();
		this.writer = this.CreateWriter();
	}

	private BufferedReader CreateReader() {
		InputStream stream = this.CreateInputStream();
		InputStreamReader stream_reader = new InputStreamReader(stream);
		BufferedReader reader = new BufferedReader(stream_reader);
		return reader;
	}

	private InputStream CreateInputStream() {
		InputStream stream = null;
		try {
			stream = this.client_socket.getInputStream();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return stream;
	}

	private PrintWriter CreateWriter() {
		OutputStream stream = this.CreateOutputStream();
		OutputStreamWriter stream_writer = new OutputStreamWriter(stream);
		PrintWriter writer = new PrintWriter(stream_writer, true);
		return writer;
	}

	private OutputStream CreateOutputStream() {
		OutputStream stream = null;
		try {
			stream = this.client_socket.getOutputStream();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return stream;
	}

	
	
	public void run() {
		String received_string;
		String uppercase_string;

		while (true) {
			received_string = this.Read();

			if (this.IsShutdownCommand(received_string)) {
				this.Write("Shutting down...");
				break;
			}

			uppercase_string = this.ToUpperCase(received_string);

			this.Write(uppercase_string);
		}
		this.Shutdown();

	}

	private String Read() {
		String received_string = null;
		try {
			received_string = this.reader.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return received_string;
	}

	private boolean IsShutdownCommand(String string) {
		if (string == null) {
			return true;
		}
		if (string.contains("shutdown")) {
			return true;
		}
		return false;
	}

	private void Write(String string) {
		this.writer.println(string);
	}

	private void Shutdown() {
		this.is_running.set(false);
		this.DecrementActiveWorkers();
	}

	private String ToUpperCase(String string) {
		return string.toUpperCase();
	}

	private void DecrementActiveWorkers() {
		this.active_workers.getAndDecrement();
	}
}