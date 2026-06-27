"""
台灣鄉鎮市區人口密度查詢系統
使用 pandas 處理資料，tkinter + ttk 建立 GUI 介面
"""

import os
import pandas as pd
import tkinter as tk
from tkinter import ttk


class PopulationDensityApp:
    """台灣鄉鎮市區人口密度查詢系統"""

    def __init__(self, root):
        self.root = root
        self.root.title("台灣鄉鎮市區人口密度查詢系統")
        self.root.geometry("900x600")

        # 讀取 CSV 資料
        self.df = self.load_data()

        # 建立 GUI 介面
        self.setup_ui()

        # 預設顯示所有資料
        self.update_table(self.df)

    def load_data(self):
        """讀取並整理資料"""
        # 取得程式所在目錄，讀取同目錄下的 CSV 檔案
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, '各鄉鎮市區人口密度.csv')

        # CSV 第一列為英文欄位，第二列才是中文欄位名稱，跳過第一列並以第二列作為 header
        df = pd.read_csv(
            csv_path,
            encoding='utf-8',
            header=1
        )

        # 移除最後 5 筆非資料內容
        df = df.iloc[:-5].reset_index(drop=True)

        # 僅保留 '區域別'、'年底人口數'、'土地面積' 三個欄位
        df = df[['區域別', '年底人口數', '土地面積']].copy()

        # 重新命名 '年底人口數' 為 '人口數'
        df.rename(columns={'年底人口數': '人口數'}, inplace=True)

        # 將 '人口數' 與 '土地面積' 轉換為數值型態
        df['人口數'] = pd.to_numeric(df['人口數'], errors='coerce')
        df['土地面積'] = pd.to_numeric(df['土地面積'], errors='coerce')

        # 移除含有空值的列
        df.dropna(subset=['人口數', '土地面積'], inplace=True)

        # 新增 '人口密度' 欄位：人口數 / 土地面積
        df['人口密度'] = df['人口數'] / df['土地面積']

        # 人口密度四捨五入至小數點後兩位
        df['人口密度'] = df['人口密度'].round(2)

        # 人口數顯示為整數
        df['人口數'] = df['人口數'].astype(int)

        return df

    def setup_ui(self):
        """建立 GUI 介面"""
        # 上方控制區
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="輸入區域名稱：").pack(side=tk.LEFT, padx=(0, 5))

        self.keyword_entry = ttk.Entry(control_frame, width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=(0, 5))
        # 支援 Enter 鍵觸發查詢
        self.keyword_entry.bind('<Return>', lambda e: self.query_data())

        ttk.Button(control_frame, text="查詢", command=self.query_data).pack(side=tk.LEFT)

        # 下方表格區
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 定義欄位
        columns = ('區域別', '人口數', '土地面積', '人口密度')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)

        # 設定各欄位標題與寬度
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor=tk.CENTER)

        # 加入垂直與水平滾動條
        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def query_data(self):
        """根據關鍵字查詢並更新表格"""
        keyword = self.keyword_entry.get().strip()

        if keyword:
            # 篩選出區域別包含關鍵字的資料
            mask = self.df['區域別'].str.contains(keyword, na=False)
            filtered_df = self.df[mask]
        else:
            # 若輸入為空，顯示全部資料
            filtered_df = self.df

        self.update_table(filtered_df)

    def update_table(self, data):
        """更新表格顯示內容"""
        # 清除現有資料
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 插入新資料
        for _, row_data in data.iterrows():
            self.tree.insert(
                '',
                tk.END,
                values=(
                    row_data['區域別'],
                    row_data['人口數'],
                    row_data['土地面積'],
                    row_data['人口密度']
                )
            )


def main():
    root = tk.Tk()
    app = PopulationDensityApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
