import requests
import json
import csv
from collections import defaultdict

global sorted_wallet_counts_all

def generate_wallet_csv(url, n):
    global sorted_wallet_counts_all
    # 发送GET请求获取网页内容
    response = requests.get(url)

    # 检查响应状态码，确保请求成功
    if response.status_code == 200:
        # 将响应内容转换为JSON格式
        data = response.json()

        # 创建一个defaultdict来统计"wallet"值的出现次数
        wallet_counts = defaultdict(int)

        # 检查每个元素的"wallet"值并进行统计
        collection_items = data.get("collection_items")
        if collection_items:
            for item in collection_items:
                wallet_value = item.get("wallet")
                if wallet_value:
                    wallet_counts[wallet_value] += 1

            # 按统计次数从大到小排序并取前N名
            sorted_wallet_counts = sorted(wallet_counts.items(), key=lambda x: x[1], reverse=True)
            sorted_wallet_counts_all = sorted_wallet_counts
            if n > 0:
                sorted_wallet_counts = sorted_wallet_counts[:n]
            # 处理钱包值并生成简化后的数据
            simplified_data = []
            total_items = len(collection_items)
            for wallet, count in sorted_wallet_counts:
                abridge = wallet[:4] + "..." + wallet[-4:]
                percent_owned = f"{(count / total_items) * 100:.2f}%"
                simplified_data.append((wallet, abridge, count, percent_owned))

            # 将简化后的统计结果保存为 CSV 文件
            if n > 0:
                filename = f"wallet_Top{n}.csv"
            else:
                filename = f"wallet_all.csv"
            with open(filename, "w", newline="") as csvfile:
                fieldnames = ["WALLET", "WALLET SHORTENER", "OWNED", "% OWNED"]
                writer = csv.writer(csvfile)
                writer.writerow(fieldnames)
                writer.writerows(simplified_data)

            print("CSV file generated:", filename)
            
    else:
        print("Request error")

def generate_owner_distribution_csv(data):
    owned_counts = defaultdict(int)
    for wallet, count in data:
        if count == 1:
            owned_counts["1 item"] += 1
        elif 2 <= count <= 3:
            owned_counts["2-3 items"] += 1
        elif 4 <= count <= 10:
            owned_counts["4-10 items"] += 1
        elif 11 <= count <= 25:
            owned_counts["11-25 items"] += 1
        elif 26 <= count <= 50:
            owned_counts["26-50 items"] += 1
        else:
            owned_counts["51+ items"] += 1
    total_wallets = len(data)
    owner_distribution = []
    for owned, count in owned_counts.items():
        percentage = f"{(count / total_wallets) * 100:.2f}%"
        owner_distribution.append((owned, count, percentage))
    filename = "wallet_distribution.csv"
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["OWNED", "WALLETS", "PERCENTAGE"]
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(owner_distribution)
    print("CSV file generated:", filename)

url = "https://ordapi.bestinslot.xyz/v1/get_collection/bitcoin-frogs"
n = 10
generate_wallet_csv(url, n)
generate_owner_distribution_csv(sorted_wallet_counts_all)

