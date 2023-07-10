import requests
import json
import csv
from collections import defaultdict
from enum import Enum

class OrderType(Enum):
    ORDER_HOLDS_DESC = "order_holds_desc"
    ORDER_HOLDS_ASC = "order_holds_asc"
    ORDER_BUY_NOW_DESC = "order_buy_now_desc"
    ORDER_BUY_NOW_ASC = "order_buy_now_asc"
    ORDER_LAST_SALE_DESC = "order_last_sale_desc"
    ORDER_LAST_SALE_ASC = "order_last_sale_asc"
    ORDER_INCSR_NO_DESC = "order_incsr_no_desc"
    ORDER_INCSR_NO_ASC = "order_incsr_no_asc"
    ORDER_ITEM_NAME_DESC = "order_item_name_desc"
    ORDER_ITEM_NAME_ASC = "order_item_name_asc"

#平台前缀
prefix_list = ["ordswap", "magiceden", "ordinalswallet", "gammaio", "nostr", "ordynals", "unisat", "ordinalsmarket"]

 # 发送GET请求获取网页内容
url = "https://ordapi.bestinslot.xyz/v1/get_collection/bitcoin-frogs"

response = requests.get(url)

orignialdata = response.json()

# 示例用法
collection_items = orignialdata["collection_items"]


def sort_collection_items(data, order_type, file_type):
    if response.status_code == 200:
        # 地址持有数降序排列
        if order_type == OrderType.ORDER_HOLDS_DESC.value:
            owners_dict = count_owners(data)
            sorted_owners = sorted(owners_dict.items(), key=lambda x: x[1], reverse=True)
            formatted_owners = [{"wallet": key, "count": value} for key, value in sorted_owners]
            
            #owners_json = {"owners": formatted_owners}
            if file_type is not None:
                save_data(formatted_owners, order_type, file_type)
            else:
                return formatted_owners
        # 地址持有数升序排列
        elif order_type == OrderType.ORDER_HOLDS_ASC.value:
            owners_dict = count_owners(data)
            sorted_owners = sorted(owners_dict.items(), key=lambda x: x[1], reverse=False)
            formatted_owners = [{"wallet": key, "count": value} for key, value in sorted_owners]
            
            #owners_json = {"owners": formatted_owners}
            if file_type is not None:
                save_data(formatted_owners, order_type, file_type)
            else:
                return formatted_owners
        elif order_type == OrderType.ORDER_BUY_NOW_DESC.value:
            data.sort(key=lambda item: get_listingprice_from_item(item) if get_listingprice_from_item(item) is not None else float('-inf'), reverse=True)
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data
        elif order_type == OrderType.ORDER_BUY_NOW_ASC.value:
            data.sort(key=lambda item: get_listingprice_from_item(item) if get_listingprice_from_item(item) is not None else float('inf'))
             
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data
        elif order_type == OrderType.ORDER_LAST_SALE_DESC.value:
            data.sort(key=lambda item: item["last_sale"] if item["last_sale"] is not None else float('-inf'), reverse=True)
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data
        elif order_type == OrderType.ORDER_LAST_SALE_ASC.value:
            data.sort(key=lambda item: item["last_sale"] if item["last_sale"] is not None else float('inf'))
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data
        elif order_type == OrderType.ORDER_INCSR_NO_DESC.value:
            data.sort(key=lambda item: item["inscription_number"] if item["inscription_number"] is not None else float('-inf'), reverse=True)
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data
        elif order_type == OrderType.ORDER_INCSR_NO_ASC.value:
            data.sort(key=lambda item: item["inscription_number"] if item["inscription_number"] is not None else float('inf'))
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data
        elif order_type == OrderType.ORDER_ITEM_NAME_DESC.value:
            data.sort(key=lambda item: item["item_name"] if item["item_name"] is not None else float('-inf'), reverse=True)
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data
        elif order_type == OrderType.ORDER_ITEM_NAME_ASC.value:
            data.sort(key=lambda item: item["item_name"] if item["item_name"] is not None else float('inf'))
            if file_type is not None:
                save_data(data, order_type, file_type)
            else:
                return data  
    else:
            print("The request failed, please check the network connection or API interface")


def get_listingprice_from_item(item):
    listing_prices = [item.get(key) for key in ["ordswap_listing_price", "magiceden_listing_price",
                                               "ordinalswallet_listing_price", "gammaio_listing_price",
                                               "nostr_listing_price", "ordynals_listing_price",
                                               "unisat", "ordinalsmarket_listing_price"]]

    # 过滤掉值为 None 的元素
    filtered_prices = [price for price in listing_prices if price is not None]

    if filtered_prices:
        return min(filtered_prices)
    else:
        return None



# 定义 owners 字典用于储存 "wallet" 与出现次数
def count_owners(collection_items):
    owners = defaultdict(int)
    for item in collection_items:
        owners[item["wallet"]] += 1
    return dict(owners)

'''
def save_dict_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
'''


'''
----------------------------------------------------------------------------------------
'''
# 各平台listed清单
def get_specified_listed(data,prefix, file_type):
# 检查响应状态码，确保请求成功
    if response.status_code == 200:
        prefix_listed_item = []  # 每个前缀对应的列表
        for item in data:
            if item[prefix + "_listing_price"] is not None:
                prefix_listed_item.append(item)

        prefix_listed_item.sort(key=lambda item: item[f"{prefix}_listing_price"] if item[f"{prefix}_listing_price"] is not None else float('inf'))
        # 将对应前缀的列表写入JSON文件
        filename = prefix + "_listed"
        save_data(prefix_listed_item, filename, file_type)
    else:
        print("The request failed, please check the network connection or API interface")
      

# 总listed清单
def get_all_listed(data, file_type):
 # 检查响应状态码，确保请求成功
    if response.status_code == 200:        
        total_listed_item = []  # 总的列表

        for item in data:
            for prefix in prefix_list:
                if item[prefix + "_listing_price"] is not None:
                    total_listed_item.append(item)
                    break
        total_listed_item.sort(key=lambda item: get_listingprice_from_item(item) if get_listingprice_from_item(item) is not None else float('inf'))
        filename = "total_listed"
        save_data(total_listed_item, filename, file_type)
    else:
        print("The request failed, please check the network connection or API interface")



'''
----------------------------------------------------------------------------------------
'''
# Json与CSV格式储存切换
def save_data(data, file_path, file_type):
    if file_type == 'json':
        with open(f"{file_path}.json", 'w') as json_file:
            json.dump(data, json_file)
        print(f"{file_path}.json saved as JSON file")
    elif file_type == 'csv':
        fieldnames = data[0].keys()
        with open(f"{file_path}.csv", 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"{file_path}.csv saved as CSV file")
    else:
        print("invalid file type")






# 调用 sort_collection_items 函数进行排序
# sort_collection_items(collection_items, OrderType.ORDER_HOLDS_DESC.value, 'csv')

#sort_collection_items(collection_items, OrderType.ORDER_HOLDS_DESC.value, None)


get_all_listed(collection_items ,'json')


get_specified_listed(collection_items,'magiceden' ,'json')