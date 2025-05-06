import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

# -----------------------------------------------------------------------------
#  Helper
# -----------------------------------------------------------------------------

def make_circle_image(img, size=(100, 100)):
    img = img.resize(size, Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, *size), fill=255)
    img.putalpha(mask)
    return img

# -----------------------------------------------------------------------------
#  Root window – Accueil
# -----------------------------------------------------------------------------

class Accueil(tk.Tk):
    """Application root: holds persistent state for Reglage and Profil."""

    def __init__(self):
        super().__init__()
        self.title("Accueil")
        self.geometry("500x400")

        # persistent state
        self.reglage = {"csv_path": "", "mem_val": 0, "filter_val": 0}
        self.profil = {
            "username": "Guo",
            "avatar_img": None,
            "maitrises": 150,
            "en_cours": 40,
            "non_appris": {"mots verts": 23, "mots bleu": 58, "mots rouge": 275, "mots noire": 136},
        }

        # references to child windows
        self._reglage_win = None
        self._profil_win = None
        self.jouer_windows = []

        # buttons
        tk.Button(self, text="Réglage", command=self.open_reglage).place(x=10, y=10)
        tk.Button(self, text="Jouer !",  command=self.open_jouer).place(x=200, y=180)
        tk.Button(self, text="Carte",   command=self.open_carte).place(x=200, y=240)
        tk.Button(self, text="Quitter", command=self.destroy).place(x=200, y=300)

        # mini avatar + Profil
        frame = tk.Frame(self, width=60, height=80)
        frame.place(x=400, y=10)
        self.avatar_canvas = tk.Canvas(frame, width=60, height=60, highlightthickness=0)
        self.avatar_canvas.pack()
        self.avatar_canvas.create_oval(0, 0, 60, 60, fill="white", outline="")
        self.avatar_canvas.bind("<Button-1>", self.open_profil)
        lbl = tk.Label(frame, text="Profil", cursor="hand2")
        lbl.pack(pady=(0,5)); lbl.bind("<Button-1>", self.open_profil)

    def open_reglage(self):
        if self._reglage_win and self._reglage_win.winfo_exists():
            self._reglage_win.lift(); return
        self._reglage_win = ReglageWindow(self)

    def open_profil(self, *_):
        if self._profil_win and self._profil_win.winfo_exists():
            self._profil_win.lift(); return
        self._profil_win = ProfilWindow(self)

    def open_jouer(self):
        JouerWindow(self)

    def open_carte(self):
        CarteWindow(self, progress=self.profil.get("progress", 0.0))

    def set_avatar(self, pil_img):
        self.profil["avatar_img"] = pil_img
        thumb = pil_img.resize((60, 60), Image.LANCZOS)
        self._thumb = ImageTk.PhotoImage(thumb)
        self.avatar_canvas.delete("all")
        self.avatar_canvas.create_image(30, 30, image=self._thumb)

    def broadcast_refresh(self):
        for w in list(self.jouer_windows):
            if w.winfo_exists(): w.update_stats()
            else: self.jouer_windows.remove(w)

# -----------------------------------------------------------------------------
#  ReglageWindow
# -----------------------------------------------------------------------------

class ReglageWindow(tk.Toplevel):
    FILTER_NAMES = ["vert","bleu","rouge","noire"]
    def __init__(self, master):
        super().__init__(master); self.master=master; self.title("Réglage")
        self.geometry("200x300")
        # CSV path
        self.csv_path = tk.StringVar(value=master.reglage["csv_path"])
        row = tk.Frame(self); row.pack(padx=10,pady=5,fill="x")
        tk.Label(row, textvariable=self.csv_path).pack(side="left")
        tk.Button(row, text="Upload CSV", command=self.upload_csv).pack(padx=5)
        # memory curve
        tk.Label(self, text="La courbe de mémoire").pack(anchor="w",padx=10)
        self.mem = tk.IntVar(value=master.reglage["mem_val"])
        r=tk.Frame(self); r.pack(padx=10,pady=5,fill="x")
        lbl=tk.Label(r,text=f"{self.mem.get()}%")
        tk.Scale(r,from_=0,to=100,orient="horizontal",variable=self.mem,
                 command=lambda v: lbl.config(text=f"{int(float(v))}%")).pack(side="left",fill="x",expand=True)
        lbl.pack(side="left",padx=5)
        # filter
        tk.Label(self,text="Filtre").pack(anchor="w",padx=10)
        self.filt=tk.IntVar(value=master.reglage["filter_val"])
        f=tk.Frame(self); f.pack(padx=10,pady=5,fill="x")
        flbl=tk.Label(f,text=self.FILTER_NAMES[self.filt.get()])
        tk.Scale(f,from_=0,to=3,orient="horizontal",variable=self.filt,
                 tickinterval=1,showvalue=False,
                 command=lambda v: flbl.config(text=self.FILTER_NAMES[int(float(v))])).pack(side="left",fill="x",expand=True)
        flbl.pack(side="left",padx=5)
        # buttons
        tk.Button(self,text="Sauvegarder",command=self.save).pack(pady=(10,5))
        tk.Button(self,text="Fermer",command=self.destroy).pack()
    def upload_csv(self):
        p=filedialog.askopenfilename(title="Choisissez CSV",filetypes=[("CSV","*.csv")])
        if p: self.csv_path.set(p)
    def save(self):
        self.master.reglage.update({"csv_path":self.csv_path.get(),
                                    "mem_val":self.mem.get(),
                                    "filter_val":self.filt.get()})
        self.master.broadcast_refresh()
        messagebox.showinfo("Réglage","Modifications sauvegardées ✅")

# -----------------------------------------------------------------------------
#  ProfilWindow
# -----------------------------------------------------------------------------

class ProfilWindow(tk.Toplevel):
    COLOR_MAP={"mots verts":"green","mots bleu":"blue","mots rouge":"red","mots noire":"black"}
    def __init__(self, master):
        super().__init__(master); self.master=master; self.title("Profil")
        data=master.profil
        # header
        hdr=tk.Frame(self); hdr.grid(row=0,column=0,padx=10,pady=10,sticky="w")
        self.av_can=tk.Canvas(hdr,width=100,height=100,highlightthickness=0)
        self.av_can.grid(row=0,column=0,rowspan=2)
        self.av_can.create_oval(0,0,100,100,fill="#eee",outline="")
        if data["avatar_img"]:
            self._av=ImageTk.PhotoImage(data["avatar_img"])
            self.av_can.create_image(50,50,image=self._av)
        tk.Button(hdr,text="Upload Avatar",command=self.upload_avatar).grid(row=2,column=0,pady=(10,0),sticky="w")
        tk.Label(hdr,text="Username:").grid(row=0,column=1,sticky="w",padx=(10,0))
        self.user=tk.StringVar(value=data["username"])
        tk.Entry(hdr,textvariable=self.user,width=20).grid(row=0,column=2,padx=(0,10))
        # stats read-only
        stats=tk.Frame(self); stats.grid(row=2,column=0,padx=10,pady=10)
        # Maîtrises
        lf1=tk.LabelFrame(stats,text="Maîtrises");lf1.grid(row=0,column=0,padx=5,pady=5)
        tk.Label(lf1,text=str(data["maitrises"])).pack(padx=10,pady=10)
        # En cours
        lf2=tk.LabelFrame(stats,text="En cours");lf2.grid(row=0,column=1,padx=5,pady=5)
        tk.Label(lf2,text=str(data["en_cours"])).pack(padx=10,pady=10)
        # Non appris
        lf3=tk.LabelFrame(stats,text="Non appris");lf3.grid(row=1,column=0,columnspan=2,padx=5,pady=5)
        for r,(lbl,cnt) in enumerate(data["non_appris"].items()):
            tk.Label(lf3,text=lbl,fg=self.COLOR_MAP.get(lbl)).grid(row=r,column=0,sticky="w",padx=5)
            tk.Label(lf3,text=str(cnt)).grid(row=r,column=1,sticky="e",padx=5)
        # buttons
        tk.Button(self,text="Sauvegarder",command=self.save).grid(row=3,column=0,pady=(5,10))
        tk.Button(self,text="Fermer",command=self.destroy).grid(row=4,column=0)
    def upload_avatar(self):
        p=filedialog.askopenfilename(title="Choisissez image",filetypes=[("Images","*.png *.jpg *.jpeg *.gif")])
        if not p: return
        img=make_circle_image(Image.open(p),size=(100,100))
        self._av=ImageTk.PhotoImage(img)
        self.av_can.delete("all");self.av_can.create_image(50,50,image=self._av)
        self.master.set_avatar(img)
    def save(self):
        self.master.profil.update({"username":self.user.get()})
        self.master.broadcast_refresh();messagebox.showinfo("Profil","Modifications sauvegardées ✅")

# -----------------------------------------------------------------------------
#  JouerWindow
# -----------------------------------------------------------------------------

class JouerWindow(tk.Toplevel):
    COLORS=["vert","bleu","rouge","noire"]
    def __init__(self, master):
        super().__init__(master);self.master=master;self.title("Jouer");self.geometry("600x500")
        master.jouer_windows.append(self)
        frame=tk.Frame(self,height=250,bg="white",relief=tk.RAISED,borderwidth=2)
        frame.pack(fill=tk.BOTH,expand=True,padx=20,pady=20)
        bottom=tk.Frame(self);bottom.pack(fill=tk.BOTH,expand=True)
        stats=tk.Frame(bottom);stats.pack()
        self.m=tk.StringVar();self.e=tk.StringVar();self.n=tk.StringVar()
        for var in (self.m,self.e,self.n): tk.Label(stats,textvariable=var,font=("Arial",12)).pack(pady=5)
        btnf=tk.Frame(bottom);btnf.pack();
        for txt in ("Je sais pas","Rest ici","Avancer"): tk.Button(btnf,text=txt,width=15).pack(side=tk.LEFT,padx=10)
        if master._reglage_win: master._reglage_win.filt.trace_add("write",lambda *_:self.update_stats())
        self.update_stats()
    def calculate_non_appris(self):
        """Sum 'non appris' counts up to the current filter, correctly including 'mots verts'."""
        f_val = self.master.reglage["filter_val"]
        # map color to exact dict key
        key_map = {
            "vert":  "mots verts",
            "bleu":  "mots bleu",
            "rouge": "mots rouge",
            "noire": "mots noire",
        }
        selected = self.COLORS[:f_val + 1]
        return sum(
            self.master.profil["non_appris"].get(key_map[color], 0)
            for color in selected
        )

    def update_stats(self):
        p=self.master.profil
        self.m.set(f"Maîtrisées: {p['maitrises']}")
        self.e.set(f"En cours: {p['en_cours']}")
        self.n.set(f"Non appris: {self.calculate_non_appris()}")
    def destroy(self):
        if self in self.master.jouer_windows: self.master.jouer_windows.remove(self)
        super().destroy()

# -----------------------------------------------------------------------------
#  CarteWindow 
# -----------------------------------------------------------------------------

class CarteWindow(tk.Toplevel):
    def __init__(self, master=None, progress=0.0):
        super().__init__(master);self.title("Carte");self.progress=progress
        img=Image.open("carte.jpg");ow,oh=img.size
        sw,sh=self.winfo_screenwidth()*0.9,self.winfo_screenheight()*0.9
        if ow>sw or oh>sh: img=img.resize((int(ow*min(sw/ow,sh/oh)),int(oh*min(sw/ow,sh/oh))),Image.LANCZOS)
        w,h=img.size; self.geometry(f"{w}x{h+80}")
        cvs=tk.Canvas(self,width=w,height=h);cvs.pack()
        self._bg=ImageTk.PhotoImage(img);cvs.create_image(0,0,anchor="nw",image=self._bg)
        cvs.create_line(291,135,348,378,fill="red",width=2)
        mx=291+(348-291)*(1-progress);my=135+(378-135)*(1-progress)
        cvs.create_oval(mx-6,my-6,mx+6,my+6,fill="red",outline="")
        cvs.create_text(mx,my-10,text="Vous êtes ici !",font=("Arial",12,"bold"),fill="red")
        tk.Label(self,text=f"Progrès: {int(progress*100)} %").pack(pady=(5,0))
        tk.Button(self,text="Fermer",command=self.destroy).pack(pady=5)

if __name__ == "__main__":
    Accueil().mainloop()
