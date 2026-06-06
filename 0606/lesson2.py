import requests
from requests import Response
url: str = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

#__name__ = "__main__"代表為主執行檔
n=10
def main(): #def自訂的function，main是function的名稱，():裡面是參數
    print("這裡是main function的命名空間") #這裡是function程式是命名空間
    
    response: Response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("下載成功")
        print(type(data))
        print(len(data)) #查詢串列資料
        print(data[0])
    else:
        print("下載失敗")
        print(response.status_code)

if __name__ == '__main__':
    main()
#n放在main的記憶體空間叫做local variable(區域變數)，只能在main function裡面使用

