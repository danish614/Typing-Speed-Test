import threading
import tkinter as tk
from tkinter import messagebox
import speedtest
import math
import pyperclip 


def to_mbps(bits_per_second):
    if bits_per_second is None:
        return "N/A"
    mbps = bits_per_second / 1_000_000.0
    return f"{mbps:.2f} Mbps"

class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        root.title("Internet Speed Test")
        root.geometry("520x360")
        root.configure(bg="#0f1724")

        header = tk.Label(root, text="Internet Speed Test", font=("Segoe UI", 20, "bold"),
                          fg="#00dae6", bg="#0f1724")
        header.pack(pady=(16,8))

        self.info_label = tk.Label(root, text="Click 'Start Test' to measure your connection.",
                                   font=("Segoe UI", 10), fg="#cbd5e1", bg="#0f1724")
        self.info_label.pack(pady=(0,12))

        frame = tk.Frame(root, bg="#0f1724")
        frame.pack(pady=6, padx=12, fill="x")

        self.ping_var = tk.StringVar(value="Ping: -")
        self.dl_var   = tk.StringVar(value="Download: -")
        self.ul_var   = tk.StringVar(value="Upload: -")
        self.srv_var  = tk.StringVar(value="Server: -")

        lbl_ping = tk.Label(frame, textvariable=self.ping_var, font=("Segoe UI", 13), fg="#f0f9ff", bg="#0f1724")
        lbl_ping.pack(anchor="w", pady=4)
        lbl_dl = tk.Label(frame, textvariable=self.dl_var, font=("Segoe UI", 13, "bold"), fg="#7efc6e", bg="#0f1724")
        lbl_dl.pack(anchor="w", pady=4)
        lbl_ul = tk.Label(frame, textvariable=self.ul_var, font=("Segoe UI", 13, "bold"), fg="#ffd166", bg="#0f1724")
        lbl_ul.pack(anchor="w", pady=4)
        lbl_srv = tk.Label(frame, textvariable=self.srv_var, font=("Segoe UI", 11), fg="#cbd5e1", bg="#0f1724")
        lbl_srv.pack(anchor="w", pady=6)

    
        btn_frame = tk.Frame(root, bg="#0f1724")
        btn_frame.pack(pady=(12,4))

        self.start_btn = tk.Button(btn_frame, text="Start Test ▶", command=self.start_test,
                                   bg="#00dae6", fg="#001219", font=("Segoe UI", 11, "bold"), width=14)
        self.start_btn.grid(row=0, column=0, padx=8)

        self.copy_btn = tk.Button(btn_frame, text="Copy Results", command=self.copy_results,
                                  bg="#94a3b8", fg="#001219", font=("Segoe UI", 11), width=12)
        self.copy_btn.grid(row=0, column=1, padx=8)

        self.clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_results,
                                   bg="#ef4444", fg="white", font=("Segoe UI", 11), width=10)
        self.clear_btn.grid(row=0, column=2, padx=8)

        
        self.status = tk.Label(root, text="", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f1724", wraplength=480, justify="left")
        self.status.pack(pady=(8,0))

        
        self.latest = {}

    def start_test(self):
    
        self.start_btn.config(state="disabled", text="Testing...")
        self.status.config(text="Initializing speed test (finding best server)...")
        t = threading.Thread(target=self._run_speedtest, daemon=True)
        t.start()

    def _run_speedtest(self):
        try:
            st = speedtest.Speedtest()
            st.get_servers()          
            best = st.get_best_server()  
            server_info = f"{best['sponsor']} ({best['name']}, {best.get('country','')})"
        
            self._set_status("Measuring download speed...")
            dl = st.download()
            self._set_status("Measuring upload speed...")
            ul = st.upload()
            ping = best.get('latency') or st.results.ping

            
            self.latest = {"ping": ping, "download": dl, "upload": ul, "server": server_info}

            
            self.root.after(0, lambda: self._show_results(ping, dl, ul, server_info))
        except Exception as e:
            self.root.after(0, lambda: self._handle_error(e))

    def _show_results(self, ping, dl, ul, server_info):
        self.ping_var.set(f"Ping: {ping:.2f} ms")
        self.dl_var.set(f"Download: {to_mbps(dl)}")
        self.ul_var.set(f"Upload: {to_mbps(ul)}")
        self.srv_var.set(f"Server: {server_info}")
        self.status.config(text="Test completed.")
        self.start_btn.config(state="normal", text="Start Test ▶")

    def _handle_error(self, exc):
        self.status.config(text=f"Error: {exc}")
        messagebox.showerror("Speed Test Error", f"Could not complete the test:\n{exc}")
        self.start_btn.config(state="normal", text="Start Test ▶")

    def _set_status(self, txt):
        self.root.after(0, lambda: self.status.config(text=txt))

    def copy_results(self):
        if not self.latest:
            messagebox.showinfo("Info", "No results to copy. Run a test first.")
            return
        text = (f"Ping: {self.latest['ping']:.2f} ms\n"
                f"Download: {to_mbps(self.latest['download'])}\n"
                f"Upload: {to_mbps(self.latest['upload'])}\n"
                f"Server: {self.latest['server']}")
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "Results copied to clipboard.")
        except Exception:
        
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Results copied to clipboard (tkinter).")

    def clear_results(self):
        self.ping_var.set("Ping: -")
        self.dl_var.set("Download: -")
        self.ul_var.set("Upload: -")
        self.srv_var.set("Server: -")
        self.status.config(text="")
        self.latest = {}

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()


