import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
import pyttsx3
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import pygame
from langdetect import detect

# جميع لغات الكود (الأسماء والرموز)
all_languages = [
    ('Afrikaans', 'af'), ('Albanian', 'sq'), ('Amharic', 'am'), ('Arabic', 'ar'),
    ('Armenian', 'hy'), ('Azerbaijani', 'az'), ('Basque', 'eu'), ('Belarusian', 'be'),
    ('Bengali', 'bn'), ('Bosnian', 'bs'), ('Bulgarian', 'bg'), ('Catalan', 'ca'),
    ('Cebuano', 'ceb'), ('Chichewa', 'ny'), ('Chinese Simplified', 'zh-cn'),
    ('Chinese Traditional', 'zh-tw'), ('Corsican', 'co'), ('Croatian', 'hr'),
    ('Czech', 'cs'), ('Danish', 'da'), ('Dutch', 'nl'), ('English', 'en'),
    ('Esperanto', 'eo'), ('Estonian', 'et'), ('Filipino', 'tl'), ('Finnish', 'fi'),
    ('French', 'fr'), ('Frysk', 'fy'), ('Galician', 'gl'), ('Georgian', 'ka'),
    ('German', 'de'), ('Greek', 'el'), ('Gujarati', 'gu'), ('Haitian Creole', 'ht'),
    ('Hausa', 'ha'), ('Hawaiian', 'haw'), ('Hebrew', 'he'), ('Hindi', 'hi'),
    ('Hmong', 'hmn'), ('Hungarian', 'hu'), ('Icelandic', 'is'), ('Igbo', 'ig'),
    ('Indonesian', 'id'), ('Irish', 'ga'), ('Italian', 'it'), ('Japanese', 'ja'),
    ('Javanese', 'jw'), ('Kannada', 'kn'), ('Kazakh', 'kk'), ('Khmer', 'km'),
    ('Kinyarwanda', 'rw'), ('Korean', 'ko'), ('Kurdish (Kurmanji)', 'ku'),
    ('Kyrgyz', 'ky'), ('Lao', 'lo'), ('Latin', 'la'), ('Latvian', 'lv'),
    ('Lithuanian', 'lt'), ('Luxembourgish', 'lb'), ('Macedonian', 'mk'),
    ('Malagasy', 'mg'), ('Malay', 'ms'), ('Malayalam', 'ml'), ('Maltese', 'mt'),
    ('Maori', 'mi'), ('Marathi', 'mr'), ('Mongolian', 'mn'), ('Myanmar (Burmese)', 'my'),
    ('Nepali', 'ne'), ('Norwegian', 'no'), ('Odia', 'or'), ('Pashto', 'ps'),
    ('Persian', 'fa'), ('Polish', 'pl'), ('Portuguese', 'pt'), ('Punjabi', 'pa'),
    ('Romanian', 'ro'), ('Russian', 'ru'), ('Samoan', 'sm'), ('Scots Gaelic', 'gd'),
    ('Serbian', 'sr'), ('Sesotho', 'st'), ('Shona', 'sn'), ('Sindhi', 'sd'),
    ('Sinhala', 'si'), ('Slovak', 'sk'), ('Slovenian', 'sl'), ('Somali', 'so'),
    ('Spanish', 'es'), ('Sundanese', 'su'), ('Swahili', 'sw'), ('Swedish', 'sv'),
    ('Tajik', 'tg'), ('Tamil', 'ta'), ('Tatar', 'tt'), ('Telugu', 'te'),
    ('Thai', 'th'), ('Turkish', 'tr'), ('Ukrainian', 'uk'), ('Urdu', 'ur'),
    ('Uzbek', 'uz'), ('Vietnamese', 'vi'), ('Welsh', 'cy'), ('Xhosa', 'xh'),
    ('Yiddish', 'yi'), ('Yoruba', 'yo'), ('Zulu', 'zu')
]

# إعداد محرك الصوت
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# دالة نسخ وإعادة تسمية ملف mp3
def copy_and_rename_mp3(original_path, new_path, new_name):
    try:
        shutil.copyfile(original_path, new_path)
        base_dir = os.path.dirname(new_path)
        renamed_path = os.path.join(base_dir, new_name)

        if os.path.exists(renamed_path):
            os.remove(renamed_path)

        os.rename(new_path, renamed_path)
        os.remove(original_path)

    except Exception as e:
        print(f"Error occurred: {e}")

# دالة تشغيل الصوت
def play_mp3_pygame(mp3_path):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

# دالة تحويل النص إلى كلام
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# دالة ضبط اتجاه النص
def set_text_direction(entry_widget, text):
    try:
        language = detect(text)
        if language == 'ar':
            entry_widget.config(justify='right')
        else:
            entry_widget.config(justify='left')
    except:
        entry_widget.config(justify='left')  # الافتراضي

# دالة الترجمة
def translate_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")

        from_lang = detect(query)
        selected_lang = lang_var.get()

        for lang_name, lang_code in all_languages:
            if lang_name == selected_lang:
                to_lang = lang_code
                break
        else:
            messagebox.showerror("Error", "Selected language is not available.")
            hide_loader()
            hide_listening_message()
            return

        translator = Translator(to_lang=to_lang)
        text_to_translate = translator.translate(query)
        text = text_to_translate

        tts = gTTS(text=text, lang=to_lang, slow=False)
        tts.save("audioCap.mp3")

        original_mp3_path = "audioCap.mp3"
        copy_mp3_path = "copy_audioCap.mp3"
        new_mp3_name = "new_audioCap.mp3"
        copy_and_rename_mp3(original_mp3_path, copy_mp3_path, new_mp3_name)

        mp3_path = "new_audioCap.mp3"
        play_mp3_pygame(mp3_path)

        result_var.set(text)
        set_text_direction(result_entry, text)  # ضبط الاتجاه بناءً على النص
        hide_loader()
        hide_listening_message()

    except Exception as e:
        hide_loader()
        hide_listening_message()
        messagebox.showerror("Error", f"Error: {e}")

def on_translate_button_click():
    translate_button.config(bg='#0f3460', fg='#ffffff', relief=tk.SUNKEN)
    show_listening_message()
    root.after(100, lambda: translate_button.config(bg='#0f3460', fg='#ffffff', relief=tk.RAISED))
    show_loader()
    root.after(100, translate_speech)

def show_loader():
    loader.pack(pady=20)

def hide_loader():
    loader.pack_forget()

def show_listening_message():
    listening_label.pack(pady=(20, 0), fill=tk.X)
    root.update()  # Ensure the UI updates to show the message

def hide_listening_message():
    listening_label.pack_forget()

def copy_text(entry):
    root.clipboard_clear()
    root.clipboard_append(entry.get())
    root.update()  # Important to ensure the clipboard is updated

# إعداد واجهة المستخدم
root = tk.Tk()
root.title("Audio Translation")
root.geometry("900x600")
root.configure(bg='#1a1a2e')

# عنوان
title_label = tk.Label(root, text="Audio Translation", font=('Arial', 26, 'bold'), bg='#1a1a2e', fg='#ffffff')
title_label.pack(pady=20)

# حاوية الإدخال
input_container = tk.Frame(root, bg='#1a1a2e')
input_container.pack(pady=20)

# الجانب الأيسر للإدخال
input_left = tk.Frame(input_container, bg='#0f3460', padx=15, pady=15)
input_left.pack(side=tk.LEFT, padx=10)

language_select_left = ttk.Combobox(input_left, values=["English (EN)"], state='readonly', font=('Arial', 14))
language_select_left.set("English (EN)")
language_select_left.pack(fill=tk.X)

text_entry = tk.Entry(input_left, font=('Verdana', 17), bg='#0f3460', fg='#000000', insertbackground='white', width=24)
text_entry.insert(0, "Speak to translate...")
text_entry.config(state='readonly')
text_entry.pack(pady=10)

# الجانب الأيمن للإدخال
input_right = tk.Frame(input_container, bg='#0f3460', padx=15, pady=15)
input_right.pack(side=tk.RIGHT, padx=10)

language_names = [lang[0] for lang in all_languages]
lang_var = tk.StringVar()
language_select_right = ttk.Combobox(input_right, textvariable=lang_var, values=language_names, state='readonly', font=('Arial', 14))
language_select_right.set("Select Language")
language_select_right.pack(fill=tk.X)

translated_text_entry = tk.Entry(input_right, font=('Verdana', 17), bg='#0f3460', fg='#000000', insertbackground='#0f3460', width=24)
translated_text_entry.insert(0, "Translation will appear here...")
translated_text_entry.config(state='readonly')
translated_text_entry.pack(pady=10)

# زر الترجمة
translate_button = tk.Button(root, text="Speak for Translation", font=('Arial', 16, 'bold'), bg='#0f3460', fg='#ffffff', relief=tk.RAISED, command=on_translate_button_click)
translate_button.pack(pady=20)

# لودر
loader = tk.Frame(root, bg='#1a1a2e')
loader.pack_forget()

# نتائج الترجمة
result_var = tk.StringVar()
result_label = tk.Label(root, text="Translation Result:", font=('Arial', 18), bg='#1a1a2e', fg='#ffffff')
result_label.pack(pady=5)

result_frame = tk.Frame(root, bg='#1a1a2e')
result_frame.pack(pady=5)

result_entry = tk.Entry(result_frame, textvariable=result_var, font=('Verdana', 16), bg='#0f3460', fg='#ffffff', insertbackground='white', readonlybackground='#0f3460', state='readonly')
result_entry.pack(side=tk.LEFT, padx=(0, 10))

copy_text_button_result = tk.Button(result_frame, text="Copy", command=lambda: copy_text(result_entry), font=('Verdana', 12), bg='#0f3460', fg='#ffffff')
copy_text_button_result.pack(side=tk.RIGHT)

# رسالة الاستماع
listening_label = tk.Label(root, text="Listening... Please wait...", font=('Verdana', 16), bg='#ffcc00', fg='#000000', relief=tk.RAISED, padx=10, pady=5)
listening_label.pack_forget()

root.mainloop()