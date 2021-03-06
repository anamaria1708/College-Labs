package mjaksic.distributed_system_client.measurements;

import java.util.List;

public class MeasurementSimulator {
	
	private static final String file_name = "Measurements.csv";
	private static final List<Measurement> measurements = MeasurementsReader.ReadFilesAsList(file_name);

	public static Measurement GetMeasurementBasedOnTime(int seconds) {
		int index = MeasurementSimulator.CalculateIndex(seconds);
		return measurements.get(index);
	}
	
	private static int CalculateIndex(int seconds) {
		return seconds % 100;
	}

}
