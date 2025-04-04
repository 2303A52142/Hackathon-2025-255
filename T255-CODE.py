import tkinter as tk
from tkinter import ttk, scrolledtext
import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

class BlockchainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Demo")
        self.root.geometry("800x600")
        
        # Set theme colors
        self.root.configure(bg='white')
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white', foreground='black')
        style.configure('TButton', padding=6)
        style.configure('Success.TLabel', foreground='#2e7d32')
        style.configure('Error.TLabel', foreground='#d32f2f')
        
        self.blockchain = []
        self.difficulty = 2
        
        # Create the first block (genesis block)
        genesis_block = Block(0, "Genesis Block", "0")
        genesis_block.mine_block(self.difficulty)
        self.blockchain.append(genesis_block)
        
        self.setup_gui()

    def setup_gui(self):
        # Input Frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Data:").pack(side=tk.LEFT)
        self.data_entry = ttk.Entry(input_frame, width=40)
        self.data_entry.pack(side=tk.LEFT, padx=5)

        add_button = ttk.Button(input_frame, text="Add Block", command=self.add_block)
        add_button.pack(side=tk.LEFT, padx=5)
        
        verify_button = ttk.Button(input_frame, text="Verify Chain", command=self.verify_chain)
        verify_button.pack(side=tk.LEFT, padx=5)

        # Blockchain Display
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True)

        self.blockchain_display = scrolledtext.ScrolledText(
            display_frame, 
            wrap=tk.WORD, 
            height=20,
            bg='white',
            fg='black',
            font=('Courier', 10)
        )
        self.blockchain_display.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(
            self.root, 
            text="", 
            padding="10",
            style='TLabel'
        )
        self.status_label.pack(fill=tk.X)

        self.update_display()

    def add_block(self):
        data = self.data_entry.get()
        if data:
            new_block = Block(
                len(self.blockchain),
                data,
                self.blockchain[-1].hash
            )
            new_block.mine_block(self.difficulty)
            self.blockchain.append(new_block)
            self.data_entry.delete(0, tk.END)
            self.update_display()
            self.status_label.configure(style='Success.TLabel')
            self.status_label.configure(text="New block added and mined successfully!")
        else:
            self.status_label.configure(style='Error.TLabel')
            self.status_label.configure(text="Please enter some data!")

    def verify_chain(self):
        for i in range(1, len(self.blockchain)):
            current_block = self.blockchain[i]
            previous_block = self.blockchain[i-1]

            if current_block.hash != current_block.calculate_hash():
                self.status_label.configure(style='Error.TLabel')
                self.status_label.configure(text="Chain invalid: Current hash is invalid!")
                return
            
            if current_block.previous_hash != previous_block.hash:
                self.status_label.configure(style='Error.TLabel')
                self.status_label.configure(text="Chain invalid: Previous hash mismatch!")
                return

        self.status_label.configure(style='Success.TLabel')
        self.status_label.configure(text="Blockchain is valid!")

    def update_display(self):
        self.blockchain_display.delete(1.0, tk.END)
        for block in self.blockchain:
            self.blockchain_display.insert(tk.END, 
                f"\nBlock #{block.index}\n"
                f"Timestamp: {block.timestamp}\n"
                f"Data: {block.data}\n"
                f"Previous Hash: {block.previous_hash}\n"
                f"Hash: {block.hash}\n"
                f"Nonce: {block.nonce}\n"
                f"{'-'*50}\n"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainGUI(root)
    root.mainloop()