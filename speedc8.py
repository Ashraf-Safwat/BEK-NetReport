import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import speedtest
from datetime import datetime, timedelta
import threading
import time

class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Test Application")
        self.center_window(self.root, 400, 300)

        # Welcome Screen
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(fill='both', expand=True)

        self.info_label = tk.Label(self.welcome_frame, text="Welcome to the Speed Test Application!\n\n"
                                                            "This application runs periodic speed tests and logs the results.\n"
                                                            "You can specify the interval (in minutes) and duration (in hours)\n"
                                                            "for the tests. The results will be saved to a CSV file.",
                                   justify=tk.LEFT)
        self.info_label.pack(pady=10)

        self.interval_label = tk.Label(self.welcome_frame, text="Interval (minutes):")
        self.interval_label.pack()
        self.interval_entry = tk.Entry(self.welcome_frame)
        self.interval_entry.pack()

        self.duration_label = tk.Label(self.welcome_frame, text="Duration (hours):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(self.welcome_frame)
        self.duration_entry.pack()

        self.start_button = tk.Button(self.welcome_frame, text="Start", command=self.start_tests, bg="blue", fg="white")
        self.start_button.pack(pady=20)

        # Results Screen
        self.results_frame = tk.Frame(self.root)

        self.server_label = tk.Label(self.results_frame, text="Server: N/A")
        self.server_label.pack()
        self.time_label = tk.Label(self.results_frame, text="Time: N/A")
        self.time_label.pack()
        self.counter_label = tk.Label(self.results_frame, text="Total tests run: 0")
        self.counter_label.pack()

        self.progress_label = tk.Label(self.results_frame, text="Speed test progress")
        self.progress_label.pack()

        self.progress_bar = tk.Label(self.results_frame, text="", bg="blue", width=20)
        self.progress_bar.pack(pady=10)

        self.show_csv_button = tk.Button(self.results_frame, text="Show CSV", command=self.show_csv, bg="green", fg="white")
        self.show_csv_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.generate_report_button = tk.Button(self.results_frame, text="Generate Report", command=self.generate_report, bg="blue", fg="white")
        self.generate_report_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.end_test_button = tk.Button(self.results_frame, text="End Test", command=self.end_test, bg="red", fg="white")
        self.end_test_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.test_running = False
        self.test_counter = 0
        self.test_start_time = None
        self.interval = None
        self.duration = None
        self.results = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def start_tests(self):
        try:
            self.interval = int(self.interval_entry.get())
            self.duration = int(self.duration_entry.get())
            self.test_start_time = datetime.now()
            self.test_end_time = self.test_start_time + timedelta(hours=self.duration)
            self.test_running = True

            self.welcome_frame.pack_forget()
            self.results_frame.pack(fill='both', expand=True)
            self.center_window(self.root, 400, 300)

            self.run_tests()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for interval and duration.")

    def run_tests(self):
        def run():
            while self.test_running and datetime.now() < self.test_end_time:
                self.run_speedtest()
                time.sleep(self.interval * 60)
            self.test_running = False

        threading.Thread(target=run).start()

    def run_speedtest(self):
        self.update_progress("Running...")
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        st.results.share()

        result = st.results.dict()
        self.results.append(result)

        self.test_counter += 1
        self.update_results(result)
        self.save_to_csv(result)
        self.update_progress("")

    def update_results(self, result):
        self.server_label.config(text=f"Server: {result['server']['name']}")
        self.time_label.config(text=f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.counter_label.config(text=f"Total tests run: {self.test_counter}")

    def save_to_csv(self, result):
        df = pd.DataFrame(self.results)
        df.to_csv("speedtest_results.csv", index=False)
        print("Speedtest result added to CSV file.")

    def show_csv(self):
        df = pd.read_csv("speedtest_results.csv")
        print(df)

    def generate_report(self):
        df = pd.read_csv("speedtest_results.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        avg_download = df['download'].mean()
        avg_upload = df['upload'].mean()
        avg_latency = df['ping'].mean()

        with PdfPages('speedtest_report.pdf') as pdf:
            plt.figure(figsize=(10, 6))

            plt.subplot(2, 1, 1)
            plt.plot(df.index, df['download'], label='Download Speed')
            plt.plot(df.index, df['upload'], label='Upload Speed')
            plt.ylabel('Speed (Mbps)')
            plt.title('Download and Upload Speed Over Time')
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(df.index, df['ping'], label='Latency')
            plt.ylabel('Latency (ms)')
            plt.title('Latency Over Time')
            plt.legend()

            plt.tight_layout()
            pdf.savefig()
            plt.close()

        print("PDF report generated.")

    def update_progress(self, status):
        self.progress_bar.config(text=status)

    def end_test(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to stop the test and exit?"):
            self.test_running = False
            self.root.quit()

    def on_closing(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to stop the test and exit?"):
            self.test_running = False
            self.root.quit()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()
