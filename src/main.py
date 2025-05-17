from textnode import *
print("hello world")

def main():
    node = TextNode("Hello, world!", TextType.BOLD, url="https://www.me.com")
    print(node)
if __name__ == "__main__":
    main()

