import requests
import json
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

 # 发送GET请求获取网页内容
url = "https://ordapi.bestinslot.xyz/v1/get_collection/bitcoin-frogs"

response = requests.get(url)

orignialdata = response.json()

# 示例用法
collection_items = orignialdata["collection_items"]



def sort_collection_items(collection_items, order_type):
    # 地址持有数降序排列
    if order_type == OrderType.ORDER_HOLDS_DESC.value:
        owners_dict = count_owners(collection_items)
        sorted_owners = sorted(owners_dict.items(), key=lambda x: x[1], reverse=True)
        formatted_owners = [{"wallet": key, "count": value} for key, value in sorted_owners]
        owners_json = {"owners": formatted_owners}
        save_dict_to_json(owners_json, f"{order_type}.json")
    # 地址持有数升序排列
    elif order_type == OrderType.ORDER_HOLDS_ASC.value:
        owners_dict = count_owners(collection_items)
        sorted_owners = sorted(owners_dict.items(), key=lambda x: x[1], reverse=False)
        formatted_owners = [{"wallet": key, "count": value} for key, value in sorted_owners]
        owners_json = {"owners": formatted_owners}
        save_dict_to_json(owners_json, f"{order_type}.json")

    elif order_type == OrderType.ORDER_BUY_NOW_DESC.value:
        collection_items.sort(key=lambda item: get_listingprice_from_item(item) if get_listingprice_from_item(item) is not None else float('-inf'), reverse=True)
        save_dict_to_json(collection_items, f"{order_type}.json")
    elif order_type == OrderType.ORDER_BUY_NOW_ASC.value:
        collection_items.sort(key=lambda item: get_listingprice_from_item(item) if get_listingprice_from_item(item) is not None else float('inf'))
        save_dict_to_json(collection_items, f"{order_type}.json")
    elif order_type == OrderType.ORDER_LAST_SALE_DESC.value:
        collection_items.sort(key=lambda item: item["last_sale"] if item["last_sale"] is not None else float('-inf'), reverse=True)
        save_dict_to_json(collection_items, f"{order_type}.json")
    elif order_type == OrderType.ORDER_LAST_SALE_ASC.value:
        collection_items.sort(key=lambda item: item["last_sale"] if item["last_sale"] is not None else float('inf'))
        save_dict_to_json(collection_items, f"{order_type}.json")
    elif order_type == OrderType.ORDER_INCSR_NO_DESC.value:
        collection_items.sort(key=lambda item: item["inscription_number"] if item["inscription_number"] is not None else float('-inf'), reverse=True)
        save_dict_to_json(collection_items, f"{order_type}.json")
    elif order_type == OrderType.ORDER_INCSR_NO_ASC.value:
        collection_items.sort(key=lambda item: item["inscription_number"] if item["inscription_number"] is not None else float('inf'))
        save_dict_to_json(collection_items, f"{order_type}.json")
    elif order_type == OrderType.ORDER_ITEM_NAME_DESC.value:
        collection_items.sort(key=lambda item: item["item_name"] if item["item_name"] is not None else float('-inf'), reverse=True)
        save_dict_to_json(collection_items, f"{order_type}.json")
    elif order_type == OrderType.ORDER_ITEM_NAME_ASC.value:
        collection_items.sort(key=lambda item: item["item_name"] if item["item_name"] is not None else float('inf'))
        save_dict_to_json(collection_items, f"{order_type}.json")
        



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

def save_dict_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)




# 调用 sort_collection_items 函数进行排序
sort_collection_items(collection_items, "order_last_sale_desc")

