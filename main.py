import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import pyttsx3
import threading


def Extract_Text_From_PDF(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract text: {e}")
        return ""


engine = None
speech_thread = None


def text_to_speech(text):
    global engine
    if text:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  
        engine.setProperty('volume', 1)  

        def speak():
            engine.say(text)
            engine.runAndWait()
            
            stop_button.after(100, stop_button.pack_forget)

        
        global speech_thread
        speech_thread = threading.Thread(target=speak)
        speech_thread.start()

       
        stop_button.after(100, stop_button.pack)

    else:
        messagebox.showwarning("Warning", "No text to convert to speech!")


def stop_speech():
    global engine
    if engine:
        engine.stop()  
        stop_button.after(100, stop_button.pack_forget)


def Load_and_Convert_PDF():
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_file:
        text = Extract_Text_From_PDF(pdf_file)
        if text:
            text_to_speech(text)


root = tk.Tk()
root.title("PDF to Audiobook")
root.geometry("500x350")


load_button = tk.Button(root, text="Load PDF and Convert to Audiobook", command=Load_and_Convert_PDF)
load_button.pack(pady=50)


stop_button = tk.Button(root, text="Stop Audiobook", command=stop_speech)


root.mainloop()

