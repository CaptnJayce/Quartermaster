def assistant_name():
    print("What would you like your assistant to be called?")
    name = input("Enter: ")

def custom_prompt():
    print("Would you like to add a prompt?")
    prompt_check = input("Enter: ")
    if prompt_check.lower() != "yes":
        print("1")

def music_control():
    print("Will you use Spotify for music?")
    music_check = input("Enter: ")
    if music_check.lower() != "yes":
        print("1")