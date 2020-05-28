package me;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Exercise1 {
	static int avg(int[] input) {
		int total = 0;
		for(int i = 0; i < input.length; i++) {
			total += input[i];
		}
		return (int) (total / input.length);
	}
	static int avg(int[][] input) {
		int total = 0;
		for(int i = 0; i < input.length; i++) {
			total += avg(input[i]);
		}
		return (int) (total/input.length);
	}
	
	static Path p = Paths.get("measurements.txt");
	
	static boolean outputToFile = false;
	
	public static void main(String[] args) {
		// this redirects the console output to measurements.txt
		if (outputToFile) {
			PrintStream out;
			try {
				out = new PrintStream(new FileOutputStream("measurements.txt"));
				System.setOut(out);
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
		}
		
		int[][] temp = new int[14][10];
		// fills the array
		for(int day = 0; day < temp.length; day++) {
			for(int datapoint = 0; datapoint < temp[day].length; datapoint++) {
				temp[day][datapoint] = (int) (20 + 16 * Math.random());
			}
		}
		
		// prints the array
		for(int[] day : temp) {
			for(int datapoint : day) {
				System.out.print(datapoint + "  ");
			}
			System.out.println("- Durchschnitts-Temperatur: " + avg(day));
		}
		System.out.println("Gesamt-Durchsnitts-Temperatur: " + avg(temp));

		DateTimeFormatter date = DateTimeFormatter.ofPattern("dd.MM.yyyy");
		DateTimeFormatter time = DateTimeFormatter.ofPattern("HH:mm:ss");
		LocalDateTime now = LocalDateTime.now();
		System.out.println("Erstellt am " + date.format(now) + " um " + time.format(now));
		System.out.println("Unter " + System.getProperty("os.name") + " Version " + System.getProperty("os.version"));
	}
}
