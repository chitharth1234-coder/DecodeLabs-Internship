import java.util.Scanner;

public class Chatbot {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String userInput;

        System.out.println("Bot: Hi! I'm a simple chatbot. Type 'bye' to exit.");

        while (true) {
            System.out.print("You: ");
            userInput = scanner.nextLine().trim().toLowerCase();

            if (userInput.equals("hi") || userInput.equals("hello") || userInput.equals("hey")) {
                System.out.println("Bot: Hello there! How can I help you?");
            }
            else if (userInput.equals("how are you")) {
                System.out.println("Bot: I'm just a bot, but I'm doing great!");
            }
            else if (userInput.equals("your name") || userInput.equals("who are you")) {
                System.out.println("Bot: I'm ChatBot 1.0, nice to meet you!");
            }
            else if (userInput.equals("bye") || userInput.equals("exit") || userInput.equals("quit")) {
                System.out.println("Bot: Goodbye! Have a great day!");
                break;
            }
            else {
                System.out.println("Bot: Sorry, I didn't understand that. Try again?");
            }
        }

        scanner.close();
    }
}