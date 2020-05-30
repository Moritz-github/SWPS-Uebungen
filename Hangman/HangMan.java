package me.mo;

import java.util.Scanner;

public class HangMan {
	String word;
	int mistakes_left;

	char[] guessed;

	boolean won = false;

	public HangMan(String word, int tries, boolean autoAsk) {
		this.word = word;
		this.mistakes_left = tries;

		guessed = new char[word.length()];

		update_render();

		if (autoAsk) {
			while (this.mistakes_left > 0 && !won) {
				askUserForChar();
			}
		}
	}

	public void askUserForChar() {
		Scanner sc = new Scanner(System.in);
		char pick = sc.next().charAt(0);
		this.guess(pick);
	}

	public void guess(char guessed_char) {
		boolean correct = false;
		for (int i = 0; i < this.word.length(); i++) {
			if (Character.toLowerCase(guessed_char) == Character.toLowerCase(this.word.charAt(i)) &&
					Character.toLowerCase(this.guessed[i]) != Character.toLowerCase(guessed_char)) {
				this.guessed[i] = this.word.charAt(i);
				correct = true;
			}
		}
		
		if (!correct) {
			if (mistakes_left > 0) {
				mistakes_left -= 1;
			} else {
				mistakes_left = 0;
			}
		}

		if (String.valueOf(this.guessed).equals(this.word)) {
			this.won = true;
		}
		update_render();
	}

	private void update_render() {
		for (int i = 0; i < this.guessed.length; i++) {
			if (this.guessed[i] == 0) {
				System.out.print("_");
			} else {
				System.out.print(this.guessed[i]);
			}
		}
		System.out.println("\nYou have " + this.mistakes_left + " mistakes left!");

		if (this.won) {
			System.out.println("Congrats!! You won :)");
		}
	}
}
