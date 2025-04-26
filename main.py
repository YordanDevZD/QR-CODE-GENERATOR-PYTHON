import qrcode
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import Font

class QRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador QR ")
        self.root.geometry("650x650")
        self.root.resizable(False, False)
        self.dark_mode = False
        
        # Fuentes personalizadas
        self.title_font = Font(family="Segoe UI", size=24, weight="bold")
        self.label_font = Font(family="Segoe UI", size=11)
        self.button_font = Font(family="Segoe UI", size=12, weight="bold")
        
        # Colores
        self.set_theme()
        
        # Marco principal
        self.main_frame = Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Título 
        self.title_frame = Frame(self.main_frame, bg=self.bg_color)
        self.title_frame.pack(pady=(0, 20))
        
        Label(self.title_frame, 
              text="Generador de QR", 
              font=self.title_font, 
              bg=self.bg_color, 
              fg=self.text_color).pack(side=LEFT)
        
        # Botón modo oscuro/claro
        self.theme_btn = Button(self.title_frame, 
                               text="☀️", 
                               command=self.toggle_theme,
                               font=("Arial", 14),
                               bg=self.bg_color,
                               fg=self.text_color,
                               bd=0,
                               activebackground=self.bg_color)
        self.theme_btn.pack(side=RIGHT, padx=10)
        
        # Campos del formulario
        self.create_form_field("Texto o URL:", "", "texto")
        self.create_form_field("Carpeta destino:", "", "ubicacion")
        self.create_form_field("Nombre archivo:", "", "nombre")
        
        # Tamaño con slider 
        self.size_frame = Frame(self.main_frame, bg=self.bg_color)
        self.size_frame.pack(fill=X, pady=15)
        
        Label(self.size_frame, 
              text="Tamaño QR (1-40):", 
              font=self.label_font, 
              bg=self.bg_color, 
              fg=self.text_color).pack(anchor=W)
        
        self.tamano = Scale(self.size_frame, 
                          from_=1, 
                          to=40, 
                          orient=HORIZONTAL,
                          length=300,
                          bg=self.bg_color,
                          fg=self.text_color,
                          highlightthickness=0,
                          troughcolor=self.accent_light,
                          activebackground=self.accent_color)
        self.tamano.set(10)
        self.tamano.pack(fill=X)
        
        # Botón generador 
        self.generate_btn = Button(self.main_frame,
                                 text="GENERAR CÓDIGO QR",
                                 command=self.generarQR,
                                 font=self.button_font,
                                 bg=self.accent_color,
                                 fg="white",
                                 bd=0,
                                 padx=30,
                                 pady=10,
                                 activebackground=self.accent_dark)
        self.generate_btn.pack(pady=30)
        
        # Footer
        Label(self.main_frame, 
              text="Creado por YordanDev", 
              font=("Segoe UI", 9), 
              bg=self.bg_color, 
              fg=self.text_color).pack(side=BOTTOM, pady=10)
    
    def set_theme(self):
        if self.dark_mode:
            self.bg_color = "#2E2E2E"
            self.card_color = "#3D3D3D"
            self.text_color = "#FFFFFF"
            self.accent_color = "#4CAF50"
            self.accent_dark = "#3E8E41"
            self.accent_light = "#81C784"
        else:
            self.bg_color = "#F5F5F5"
            self.card_color = "#FFFFFF"
            self.text_color = "#333333"
            self.accent_color = "#4285F4"
            self.accent_dark = "#3367D6"
            self.accent_light = "#D2E3FC"
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.theme_btn.config(text="🌙" if self.dark_mode else "☀️")
        
        # Actualizar todos los elementos
        widgets = [self.main_frame, self.title_frame, self.size_frame]
        for widget in widgets:
            widget.config(bg=self.bg_color)
            
        for child in self.main_frame.winfo_children():
            if isinstance(child, (Label, Frame)):
                try:
                    child.config(bg=self.bg_color, fg=self.text_color)
                except:
                    pass
        
        self.generate_btn.config(bg=self.accent_color, activebackground=self.accent_dark)
        self.tamano.config(bg=self.bg_color, fg=self.text_color, troughcolor=self.accent_light)
    
    def create_form_field(self, label_text, placeholder, field_name):
        frame = Frame(self.main_frame, bg=self.bg_color)
        frame.pack(fill=X, pady=8)
        
        Label(frame, 
              text=label_text, 
              font=self.label_font, 
              bg=self.bg_color, 
              fg=self.text_color).pack(anchor=W, pady=(0, 5))
        
        entry = Entry(frame, 
                     font=self.label_font, 
                     bg=self.card_color,
                     fg=self.text_color,
                     insertbackground=self.text_color,
                     relief=FLAT,
                     bd=2)
        entry.pack(fill=X, ipady=8)
        entry.insert(0, placeholder)
        
        # Efecto hover 
        entry.bind("<FocusIn>", lambda e: entry.config(bg="#E8F0FE" if not self.dark_mode else "#454545"))
        entry.bind("<FocusOut>", lambda e: entry.config(bg=self.card_color))
        
        setattr(self, field_name, entry)
    
    def generarQR(self):
        try:
            texto = self.texto.get()
            ubicacion = self.ubicacion.get()
            nombre = self.nombre.get()
            tamano = self.tamano.get()
            
            if not all([texto, ubicacion, nombre]):
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
                return
                
            qr = qrcode.QRCode(version=tamano, box_size=10, border=5)
            qr.add_data(texto)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            ruta_completa = f"{ubicacion}/{nombre}.png"
            img.save(ruta_completa)
            
            messagebox.showinfo("Éxito", f"QR generado exitosamente en:\n{ruta_completa}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el QR:\n{str(e)}")

if __name__ == "__main__":
    root = Tk()
    style = ttk.Style()
    style.theme_use("clam")
    
    app = QRGenerator(root)
    root.mainloop()
