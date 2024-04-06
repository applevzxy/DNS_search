# -*- coding: utf-8 -*-
# python3.10环境

"""
Created on Thu Mar 28 16:55:00 2024
@author: 开心的胖子
"""

import dns.resolver
import re


def validate_domain(domain: str) -> bool:
    """
    验证域名的格式是否合法
    """
    pattern = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
    return pattern.match(domain) is not None


def print_and_write(file, message):
    """
    打印信息并写入文件
    """
    print(message)
    file.write(message + '\n')


def query_dns_records(resolver, domain, record_type, file):
    """
    查询指定域名的DNS记录并写入文件
    """
    try:
        answers = resolver.resolve(domain, record_type)
        print_and_write(file, f"********************{record_type}记录********************")
        for record in answers:
            print_and_write(file, str(record))
    except dns.resolver.NoAnswer:
        print_and_write(file, f"--------------------该域名没有{record_type}记录!!--------------------")
    except dns.resolver.NXDOMAIN:
        print_and_write(file, f"--------------------该域名不存在!!--------------------")
    except Exception as e:
        print_and_write(file, f"在查询{record_type}记录时发生错误：{e}")


def create_custom_resolver(dns_servers):
    """
    创建一个使用指定 DNS 服务器的自定义解析器
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = dns_servers
    return resolver


def main():
    domain = input("请输入要查询的域名全拼(例如：www.baidu.com)：")
    if not validate_domain(domain):
        print("输入的域名格式不正确，请重新输入。")
        return

    domain_parts = domain.split('.')
    subdomain = '.'.join(domain_parts[-2:])  # 网站主域名

    filename = f"{subdomain}.txt"  # 使用网站主域名作为文件名
    if '/' in filename or '\\' in filename:
        print("生成的文件名包含非法字符，程序将退出。")
        return

    custom_dns_servers = ['8.8.8.8', '1.1.1.1']  # 定义您希望使用的 DNS 服务器列表
    custom_resolver = create_custom_resolver(custom_dns_servers)

    with open(filename, "w", encoding="utf-8") as file:
        print_and_write(file, f"该网站主域名为：{subdomain}")

        # 查询不同类型的DNS记录
        record_types = ['A', 'CNAME', 'MX', 'NS', 'SOA', 'TXT', 'SRV', 'AAAA']
        for record_type in record_types:
            if record_type in ['A', 'SRV']:
                query_dns_records(custom_resolver, domain, record_type, file)
            else:
                query_dns_records(custom_resolver, subdomain, record_type, file)

    print(f"查询结果已写入文件：{filename}")


if __name__ == "__main__":
    main()
