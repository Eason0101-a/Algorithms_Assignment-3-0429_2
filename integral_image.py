import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class IntegralImage:
    def __init__(self, image):
        if not image or not image[0]:
            raise ValueError("image 不能是空的")

        self.rows = len(image)
        self.cols = len(image[0])
        self.integral = [[0] * (self.cols + 1) for _ in range(self.rows + 1)]
        self._build(image)

    def _build(self, image):
        # 使用多一列與多一欄的 0，方便處理邊界。
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                self.integral[r][c] = (
                    image[r - 1][c - 1]
                    + self.integral[r - 1][c]
                    + self.integral[r][c - 1]
                    - self.integral[r - 1][c - 1]
                )

    def get_sum(self, top, left, bottom, right):
        if top < 0 or left < 0 or bottom >= self.rows or right >= self.cols:
            raise ValueError("座標超出範圍")
        if top > bottom or left > right:
            raise ValueError("座標不合法")

        r1, c1 = top + 1, left + 1
        r2, c2 = bottom + 1, right + 1
        return (
            self.integral[r2][c2]
            - self.integral[r1 - 1][c2]
            - self.integral[r2][c1 - 1]
            + self.integral[r1 - 1][c1 - 1]
        )

    def print_integral_image(self):
        for row in self.integral:
            print(" ".join(f"{x:>4}" for x in row))

    def print_time_complexity(self):
        print("時間複雜度：")
        print("- 建立積分影像：O(rows * cols)")
        print("- 查詢任意矩形總和：O(1)")
        print("- 空間複雜度：O(rows * cols)")


class IntegralImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("積分影像計算器")
        self.root.geometry("900x700")
        self.ii = None
        
        # 設定中文字體
        self.default_font = ("新細明體", 10)
        self.root.option_add("*Font", self.default_font)
        
        self._create_widgets()
    
    def _create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== 上半部：矩陣輸入 =====
        input_frame = ttk.LabelFrame(main_frame, text="矩陣輸入", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        ttk.Label(input_frame, text="輸入矩陣（逗號或空格分隔，每行換一列）：").pack(anchor=tk.W)
        
        self.matrix_text = scrolledtext.ScrolledText(input_frame, height=6, width=50, wrap=tk.WORD)
        self.matrix_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.matrix_text.insert(tk.END, "1 2 2 4 1\n3 4 1 5 2\n2 3 3 2 4\n4 1 5 4 6\n6 3 2 1 3")
        
        button_frame1 = ttk.Frame(input_frame)
        button_frame1.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame1, text="載入矩陣", command=self.load_matrix).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="清除", command=self.clear_matrix).pack(side=tk.LEFT, padx=5)
        
        # ===== 中間部：查詢設定 =====
        query_frame = ttk.LabelFrame(main_frame, text="矩形查詢", padding="10")
        query_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 座標輸入
        coords_frame = ttk.Frame(query_frame)
        coords_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(coords_frame, text="起始列 (top):").pack(side=tk.LEFT, padx=5)
        self.top_var = tk.StringVar(value="2")
        ttk.Entry(coords_frame, textvariable=self.top_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(coords_frame, text="起始行 (left):").pack(side=tk.LEFT, padx=5)
        self.left_var = tk.StringVar(value="2")
        ttk.Entry(coords_frame, textvariable=self.left_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(coords_frame, text="結束列 (bottom):").pack(side=tk.LEFT, padx=5)
        self.bottom_var = tk.StringVar(value="3")
        ttk.Entry(coords_frame, textvariable=self.bottom_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(coords_frame, text="結束行 (right):").pack(side=tk.LEFT, padx=5)
        self.right_var = tk.StringVar(value="3")
        ttk.Entry(coords_frame, textvariable=self.right_var, width=5).pack(side=tk.LEFT, padx=5)
        
        button_frame2 = ttk.Frame(query_frame)
        button_frame2.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame2, text="查詢矩形和", command=self.query_sum).pack(side=tk.LEFT, padx=5)
        
        # ===== 下半部：輸出結果 =====
        output_frame = ttk.LabelFrame(main_frame, text="結果顯示", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=20, width=80, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def load_matrix(self):
        try:
            text = self.matrix_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("錯誤", "請輸入矩陣")
                return
            
            # 解析矩陣
            lines = text.split('\n')
            matrix = []
            for line in lines:
                if line.strip():
                    row = [int(x) for x in line.replace(',', ' ').split()]
                    matrix.append(row)
            
            # 驗證矩陣
            if not matrix or not matrix[0]:
                messagebox.showerror("錯誤", "矩陣不能為空")
                return
            
            # 建立積分影像
            self.ii = IntegralImage(matrix)
            
            # 顯示結果
            output = "矩陣已載入成功！\n\n"
            output += "原始矩陣：\n"
            for row in matrix:
                output += "  " + "  ".join(f"{x:>3}" for x in row) + "\n"
            
            output += "\n積分影像：\n"
            for row in self.ii.integral:
                output += "  " + "  ".join(f"{x:>4}" for x in row) + "\n"
            
            output += "\n時間複雜度：\n"
            output += "- 建立積分影像：O(rows * cols)\n"
            output += "- 查詢任意矩形總和：O(1)\n"
            output += "- 空間複雜度：O(rows * cols)\n"
            
            self._update_output(output)
            messagebox.showinfo("成功", "矩陣載入成功")
            
        except ValueError as e:
            messagebox.showerror("錯誤", f"輸入錯誤：{str(e)}")
        except Exception as e:
            messagebox.showerror("錯誤", f"發生錯誤：{str(e)}")
    
    def query_sum(self):
        if not self.ii:
            messagebox.showerror("錯誤", "請先載入矩陣")
            return
        
        try:
            top = int(self.top_var.get())
            left = int(self.left_var.get())
            bottom = int(self.bottom_var.get())
            right = int(self.right_var.get())
            
            result = self.ii.get_sum(top, left, bottom, right)
            
            output = f"查詢參數：\n"
            output += f"- 起始列 (top): {top}\n"
            output += f"- 起始行 (left): {left}\n"
            output += f"- 結束列 (bottom): {bottom}\n"
            output += f"- 結束行 (right): {right}\n\n"
            output += f"查詢結果（矩形區域總和）：{result}\n\n"
            
            output += "座標說明（0-based）：\n"
            output += f"- 矩陣範圍：第 {top} 至 {bottom} 列，第 {left} 至 {right} 行\n"
            
            self._update_output(output)
            messagebox.showinfo("查詢成功", f"矩形區域總和：{result}")
            
        except ValueError:
            messagebox.showerror("錯誤", "座標必須是整數")
        except Exception as e:
            messagebox.showerror("錯誤", f"查詢失敗：{str(e)}")
    
    def clear_matrix(self):
        self.matrix_text.delete("1.0", tk.END)
    
    def _update_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    
    # 建立 Tkinter 視窗並啟動 GUI
    root = tk.Tk()
    gui = IntegralImageGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
