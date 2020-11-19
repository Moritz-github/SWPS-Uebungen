package me.mo;

import java.io.File;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class UI {
	public static void main(String[] args) {
		ArrayList<String> words = new ArrayList<String>();
		try {
			File f = new File("C:/Users/Motop/Desktop/MEGAsync/Coding/Java/Köllö/Programs/Eclipse_Workspace/Hangman/src/me/mo/words.txt");
			Scanner reader = new Scanner(f);
			while(reader.hasNextLine()) {
				words.add(reader.nextLine());
			}
			reader.close();
		} catch(Exception e){
			e.printStackTrace();
		}
		Random r = new Random();
		HangMan hm = new HangMan(words.get(r.nextInt(words.size())), 7);
	}
}
