import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import json
import os

class DiaryApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Mein Tagebuch")
        self.root.geometry("700x600")
        self.root.configure(bg="#002a53")
        
        # فایل ذخیره‌سازی
        self.data_file = "my_diary.json"
        self.entries = self.load_entries()
        
        # متغیرهای وضعیت
        self.current_mood = tk.StringVar(value="Okay")
        
        self.setup_ui()
        self.display_today()
    
    def setup_ui(self):
        # فریم بالایی (تاریخ و وضعیت)
        top_frame = tk.Frame(self.root, bg="#002a53", padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        # برچسب تاریخ
        self.date_label = tk.Label(top_frame, text="Wie fühlst du dich heute?",font=("Comic Sans MS", 14)

,
                                   fg='white', bg="#002a53")
        self.date_label.pack(side=tk.LEFT)
        
        # انتخاب حالت روز
        mood_frame = tk.Frame(top_frame, bg="#002a53")
        mood_frame.pack(side=tk.RIGHT)
        
        tk.Label(mood_frame, text="Wie fühlst du dich heute?", font=("Comic Sans MS", 12),
                fg='white', bg="#002a53").pack(side=tk.LEFT)
        
        moods = ["Ausgezeichnet", "Gut", "Okay", "Schlecht", "Sehr schlecht"]
        self.mood_combo = ttk.Combobox(mood_frame, values=moods, textvariable=self.current_mood,
                                       width=15, state="readonly")
        self.mood_combo.pack(side=tk.LEFT, padx=5)
        
        # فریم میانی (محل نوشتن خاطره)
        middle_frame = tk.Frame(self.root, bg='#ecf0f1', padx=10, pady=10)
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(middle_frame, text="Na, alles klar?", font=("Comic Sans MS", 14),
                bg='#ecf0f1', fg='#2c3e50').pack(anchor=tk.W)
        
        self.text_area = scrolledtext.ScrolledText(middle_frame, wrap=tk.WORD,
                                                   font=('Vazir', 11), height=15,
                                                   bg='white', fg='#2c3e50')
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # فریم پایینی (دکمه‌ها)
        bottom_frame = tk.Frame(self.root, bg="#002a53", padx=10, pady=10)
        bottom_frame.pack(fill=tk.X)
        
        # دکمه‌ها در یک ردیف
        btn_frame = tk.Frame(bottom_frame, bg="#002a53")
        btn_frame.pack()
        
        tk.Button(btn_frame, text="Heutigen Entrag speichern", command=self.save_today,
                 font=("Comic Sans MS", 12), bg="#00a85f", fg='white',
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📖 Frühere Einträge ansehen", command=self.view_history,
                 font=("Comic Sans MS", 12), bg="#4995ff", fg='white',
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Heutigen Eintrag löschen", command=self.clear_today,
                 font=("Comic Sans MS", 12), bg="crimson", fg='white',
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # نوار وضعیت
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W, font=("Comic Sans MS", 14), bg='#bdc3c7')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def get_today_key(self):
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_today_display(self):
        return datetime.now().strftime("%A - %d %B %Y")
    
    def display_today(self):
        today_key = self.get_today_key()
        self.date_label.config(text=f"📅 {self.get_today_display()}")
        
        if today_key in self.entries:
            # نمایش خاطره امروز اگر وجود دارد
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, self.entries[today_key]['text'])
            self.current_mood.set(self.entries[today_key]['mood'])
            self.status_bar.config(text=f"📖 Die heutige Erinnerung wurde gelöscht - {self.entries[today_key]['time']}")
        else:
            self.text_area.delete(1.0, tk.END)
            self.current_mood.set("Okay")
            self.status_bar.config(text="Du hast noch nichts geschreiben ):")
    
    def save_today(self):
        today_key = self.get_today_key()
        diary_text = self.text_area.get(1.0, tk.END).strip()
        
        if not diary_text:
            messagebox.showwarning("Warnung", "schreibt etwas!")
            return
        
        self.entries[today_key] = {
            'text': diary_text,
            'mood': self.current_mood.get(),
            'time': datetime.now().strftime("%H:%M:%S"),
            'date_fa': self.get_today_display()
        }
        
        self.save_entries()
        self.status_bar.config(text=f"✅ Erinnerung vom {self.get_today_display()} gespeichert!")
        messagebox.showinfo("Fertig", "Erinnerung gespeichert!")
    
    def clear_today(self):
        if messagebox.askyesno("Bestätigen", "Möchtest du die Erinnerung von heute wirklich löschen?"):
            today_key = self.get_today_key()
            if today_key in self.entries:
                del self.entries[today_key]
                self.save_entries()
            self.text_area.delete(1.0, tk.END)
            self.current_mood.set("Okay")
            self.status_bar.config(text="Die heutige Erinnerung wurde gelöscht!")
    
    def view_history(self):
        if not self.entries:
            messagebox.showinfo("Nachricht", "Es wurde noch keine Erinnerung!")
            return
        
        # پنجره جدید برای نمایش تاریخچه
        history_win = tk.Toplevel(self.root)
        history_win.title("📚 Erinnerungsverlauf")
        history_win.geometry("600x500")
        history_win.configure(bg='#ecf0f1')
        
        tk.Label(history_win, text="Tagesliste:", font=('Vazir', 12, 'bold'),
                bg='#ecf0f1').pack(pady=5)
        
        # لیست باکس برای انتخاب روز
        listbox_frame = tk.Frame(history_win, bg='#ecf0f1')
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                            font=('Vazir', 10), height=10)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # مرتب‌سازی برعکس (جدیدترین اول)
        sorted_dates = sorted(self.entries.keys(), reverse=True)
        for date in sorted_dates:
            entry = self.entries[date]
            display_text = f"{entry['date_fa']} - {entry['mood']}"
            listbox.insert(tk.END, display_text)
        
        # متن نمایش خاطره
        tk.Label(history_win, text="Erinnerungstext:", font=('Vazir', 10, 'bold'),
                bg='#ecf0f1').pack(pady=(10,0))
        
        history_text = scrolledtext.ScrolledText(history_win, wrap=tk.WORD,
                                                font=('Vazir', 10), height=12)
        history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def show_entry(event):
            selection = listbox.curselection()
            if selection:
                date = sorted_dates[selection[0]]
                entry = self.entries[date]
                history_text.delete(1.0, tk.END)
                history_text.insert(1.0, f"Vibe: {entry['mood']}\n")
                history_text.insert(tk.END, f"Hour: {entry['time']}\n")
                history_text.insert(tk.END, f"{'='*40}\n\n")
                history_text.insert(tk.END, entry['text'])
        
        listbox.bind('<<ListboxSelect>>', show_entry)
        
        # دکمه بستن
        tk.Button(history_win, text="Schließen", command=history_win.destroy,
                 bg='#3498db', fg='white', font=('Vazir', 10)).pack(pady=10)
    
    def load_entries(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_entries(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
