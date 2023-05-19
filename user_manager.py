# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Class for Acquiring User Data ~~~~~~~~~~~~~~~~~~~~~~~~~~
class UserManager:

    def acquire_user(self):
        """A method that acquires a new user."""
        print("🛫 Welcome to Tamara's Flight Search Program 🛬")
        print("Thank you for using it.")
        first_name = input("What is your first name?\n")
        last_name = input("What is your last name?\n")

        while True:
            email_1 = input("What is your email?\n")
            email_2 = input("Verify your email address by inputting it again\n")
            if email_1 == email_2:
                print("Congratulations! You've joined the very EXCLUSIVE club 😉\n")
                return first_name, last_name, email_1
