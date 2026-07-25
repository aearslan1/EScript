# EScript 🚀

Hey there! Welcome to **EScript**—a custom programming language interpreter built entirely from scratch in Python. 

The main goal of this project is to explore how programming languages actually work under the hood. It takes code written with Turkish-based syntax and brings it to life through a full compiler pipeline: tokenizing the text, parsing it into a tree, and executing it step by step.

---

## 🌟 Inside (v1.0.0 Release)

This repository marks the **v1.0.0** milestone! Here is what EScript offers right now:

* 🔤 **Turkish Syntax:** Write logical controls, loops, and print statements using natural Turkish keywords.
* 📦 **Dynamic Data Types:** Supports integers (`tamsayı`), floats (`ondalık`), strings (`metin`), booleans (`mantıksal`), and lists (`liste`).
* 🔀 **Control Flow & Loops:** Make decisions using `eğer` / `değilse` and repeat actions with simple `döngü` blocks.
* ⚙️ **Custom Engine:** Built from the ground up without heavy external parser generators.

---

## 🛠️ How It Works Under the Hood

EScript doesn't just run magic; it processes your code through three core stages:

1. **Lexer (`lexer.py`):** Reads the raw script and breaks it down into meaningful tokens (keywords, numbers, operators).
2. **Parser (`parser.py`):** Takes those tokens and builds an Abstract Syntax Tree (AST) based on grammar rules.
3. **Interpreter (`interpreter.py`):** Walks through the AST, executes instructions, and keeps track of variables.

---

## 📝 Syntax Cheat Sheet

### Core Keywords & Operations

| Keyword | What it does |
| :--- | :--- |
| `yap` | Declare or assign a variable |
| `yaz` | Print to console |
| `giriş` | Get user input |
| `ekle`, `çıkar` | Basic addition and subtraction |
| `çarp`, `böl`, `mod` | Multiplication, division, and modulo |
| `eğer`, `değilse` | Conditional statements (`if` / `else`) |
| `döngü`, `while` | Loop execution blocks |
| `kır` | Break out of a loop |
| `krş` | Evaluate comparison statements |
| `and`, `or`, `not`, `xor` | Logical operations |

> 💡 **Tip:** Any line starting with `#` is treated as a comment and completely ignored.

---

## 💻 Quick Code Example (`testNotepad.txt`)

Here is a quick look at how EScript looks in action:

```text
# Variable declaration
yap < tamsayı < counter = 10
yaz < "Current value: ", counter < "\n"

# Comparison and conditional check
krş < (counter > 5) < is_greater

eğer is_greater {
    yaz < "The number is greater than 5!" < "\n"
} değilse {
    yaz < "The number is 5 or smaller." < "\n"
}

# Simple loop
döngü 3 {
    yaz < "EScript is running fine..." < "\n"
}
