# -*- coding: utf-8 -*-
# python3.10环境

"""
Created on Thu Mar 28 16:55:00 2024
@author: 开心的胖子
"""

# DNS域名记录查询脚本
import dns.resolver

def print_and_write(file, message):
    print(message)
    file.write(message + '\n')

def query_dns_records(domain, record_type, file):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        print_and_write(file, f"********************{record_type}记录********************")
        for record in answers:
            print_and_write(file, str(record))
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        print_and_write(file, f"--------------------该域名没有{record_type}记录!!--------------------")
    except Exception as e:
        print_and_write(file, f"在查询{record_type}记录时发生错误：{e}")

domain = input("请输入要查询的域名全拼(例如：www.baidu.com)：")  # 网站子域名
domain_parts = domain.split('.')
subdomain = '.'.join(domain_parts[-2:])  # 网站主域名

filename = f"{domain}.txt"
with open(filename, "w", encoding="utf-8") as file:
    print_and_write(file, f"该网站主域名为：{subdomain}")

    # 查询A记录
    query_dns_records(domain, 'A', file)

    # 查询CNAME记录
    query_dns_records(domain, 'CNAME', file)

    # 查询MX记录
    query_dns_records(subdomain, 'MX', file)

    # 查询NS记录
    query_dns_records(subdomain, 'NS', file)

    # 查询SOA记录
    query_dns_records(subdomain, 'SOA', file)

    # 查询TXT记录
    query_dns_records(subdomain, 'TXT', file)

    # 查询SRV记录
    query_dns_records(domain, 'SRV', file)

    # 查询AAAA记录
    query_dns_records(domain, 'AAAA', file)

print(f"查询结果已写入文件：{filename}")