import tkinter as tk

def print_widget_under_mouse(root):
    x,y = root.winfo_pointerxy()
    widget = root.winfo_containing(x,y)
    print("widget:", widget)
    root.after(1000, print_widget_under_mouse, root)

root = tk.Tk()
label_foo = tk.Label(root, text="Foo", name="label_foo")
label_bar = tk.Label(root, text="Bar", name="label_bar")
button = tk.Button(root, text="Button", name="button")

button.pack(side="bottom")
label_foo.pack(fill="both", expand=True)
label_bar.pack(fill="both", expand=True)

print_widget_under_mouse(root)

root.mainloop()