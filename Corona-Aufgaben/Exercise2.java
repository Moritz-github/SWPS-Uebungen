package me;

import java.time.LocalDate;
import java.util.ArrayList;
import java.text.DateFormatSymbols;

public class Exercise2 {
	public static void main(String[] args) {
		// reads the arguments
		int year = Integer.parseInt(args[0]);
		int month = Integer.parseInt(args[1]);
		
		// initializes a days arraylist where every day of the month is one element
		ArrayList<LocalDate> days = new ArrayList<LocalDate>();
		days.add(LocalDate.of(year, month, 1));
		while(days.get(days.size() -1).getMonthValue() == month) {
			days.add(days.get(days.size()-1).plusDays(1));
		}
		days.remove(days.size()-1);

		// prints basic info and headline
		String monthName = new DateFormatSymbols().getMonths()[month-1];
		System.out.println("Kalender für " + monthName + " " + year);
		System.out.println("Wo\tMo\tDi\tMi\tDo\tFr\tSa\tSo");
		
		// prints the correct number of tabulators so the loop starts at the right indentaion
		System.out.print((int)(days.get(0).getDayOfYear()/7 + 1));
		for(int i = 0; i < days.get(0).getDayOfWeek().getValue(); i++) {
			System.out.print("\t");
		}
		
		// prints the days
		for(int i = 0; i < days.size(); i++) {
			System.out.print(days.get(i).getDayOfMonth() + "\t");
			if (days.get(i).getDayOfWeek().getValue() == 7) {
				System.out.println("");
				System.out.print((int)((days.get(i).getDayOfYear()/7) + 2) + "\t");
			}
		}
	}
}
