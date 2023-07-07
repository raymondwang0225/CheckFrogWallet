import requests
import json

 # 发送GET请求获取网页内容
url = "https://ordapi.bestinslot.xyz/v1/get_collection/bitcoin-frogs"

response = requests.get(url)

#平台前缀
prefix_list = ["ordswap", "magiceden", "ordinalswallet", "gammaio", "nostr", "ordynals", "unisat", "ordinalsmarket"]

def get_specified_listed(prefix):
# 检查响应状态码，确保请求成功
    if response.status_code == 200:
        # 将响应内容转换为JSON格式
        data = response.json()

        prefix_listed_item = []  # 每个前缀对应的列表
        for item in data["collection_items"]:
            if item[prefix + "_listing_price"] is not None:
                prefix_listed_item.append(item)

            
        # 将对应前缀的列表写入JSON文件
        filename = prefix + "_listed" + ".json"
        with open(filename, "w") as json_file:
            print(prefix + "_listed : "+str(len(prefix_listed_item)))
            json.dump({prefix: prefix_listed_item}, json_file, indent=2)
    else:
        print("请求失败，请检查网络连接或API接口")
      


def get_all_listed(prefix_list):
 # 检查响应状态码，确保请求成功
    if response.status_code == 200:
        # 将响应内容转换为JSON格式
        data = response.json()

        total_listed_item = []  # 总的列表

        for item in data["collection_items"]:
            for prefix in prefix_list:
                if item[prefix + "_listing_price"] is not None:
                    total_listed_item.append(item)
                    break
            
        # 将总的列表写入JSON文件
        with open("total_listed.json", "w") as json_file:
            print("total listed : "+str(len(total_listed_item)))
            json.dump({"listed_items": total_listed_item}, json_file, indent=2)
    else:
        print("请求失败，请检查网络连接或API接口")
           

# 使用 for 循环调用函数
for prefix in prefix_list:
    get_specified_listed(prefix)

# 取全平台数据
get_all_listed(prefix_list)