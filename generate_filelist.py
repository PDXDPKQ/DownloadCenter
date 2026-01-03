import os
import sys
import json
from pathlib import Path

# def escape_js_string(s):
#     """转义字符串中的特殊字符，确保JavaScript语法正确"""
#     # 替换双引号为转义字符
#     s = s.replace('"', '\\"')
#     # 替换换行符
#     s = s.replace('\n', '\\n')
#     s = s.replace('\r', '\\r')
#     return s

def get_readable_size(size_in_bytes):
    """将字节数转换为易读的大小表示"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0 or unit == 'GB':
            break
        size_in_bytes /= 1024.0
    
    # 根据大小选择合适的小数位数
    if unit == 'B':
        return f"{int(size_in_bytes)} B"
    elif unit == 'KB':
        return f"{size_in_bytes:.0f} KB" if size_in_bytes < 10 else f"{size_in_bytes:.1f} KB"
    else:
        return f"{size_in_bytes:.1f} {unit}"

def generate_file_list_js(output_filename="fileList.js", exclude_extensions=None):
    """
    生成包含当前目录文件列表的JavaScript文件
    
    Args:
        output_filename: 输出的JS文件名
        exclude_extensions: 要排除的文件扩展名列表
    """
    if exclude_extensions is None:
        exclude_extensions = ['generate_filelist.py']  # 默认排除脚本文件自身
    
    current_dir = Path.cwd()
    files_data = []
    
    print(f"扫描目录: {current_dir}")
    
    # 遍历当前目录的所有文件
    for file_path in current_dir.iterdir():
        if file_path.is_file():
            # 检查是否在排除列表中
            if any(str(file_path).endswith(ext) for ext in exclude_extensions):
                continue

            try:
                # 获取文件大小
                file_size = file_path.stat().st_size

                # 添加到文件列表
                files_data.append({
                    'name': file_path.name,
                    'size': get_readable_size(file_size)
                })

                print(f"找到文件: {file_path.name} ({get_readable_size(file_size)})")

            # try:
            #     if file_path.is_file():
            #         # 处理文件
            #         file_size = file_path.stat().st_size
            #         files_data.append({
            #             'name': file_path.name,
            #             'size': get_readable_size(file_size),
            #             # 'type': 'file'
            #         })
            #         print(f"找到文件: {file_path.name} ({get_readable_size(file_size)})")
            #
            #     elif file_path.is_dir():
            #         # 处理文件夹
            #         # 计算文件夹中的文件数量
            #         file_count = sum(1 for _ in file_path.iterdir())
            #         files_data.append({
            #             'name': file_path.name,
            #             'size': f"文件夹 ({file_count} 个项目)",
            #             # 'type': 'folder'
            #         })
            #         print(f"找到文件夹: {file_path.name} ({file_count} 个项目)")


                
            except (OSError, PermissionError) as e:
                print(f"无法访问文件 {file_path.name}: {e}")
                continue
    
    if not files_data:
        print("当前目录没有找到文件（已排除脚本文件）")
        return False
    
    # 按文件名排序
    files_data.sort(key=lambda x: x['name'].lower())

    # 生成JavaScript内容
    js_content = f"""// 自动生成的文件列表
    // 生成时间: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
    // 目录: {current_dir}

    const mockFiles = {json.dumps(files_data, indent=4, ensure_ascii=False)};

    // 导出供其他模块使用（如果需要）
    if (typeof module !== 'undefined' && module.exports) {{
        module.exports = mockFiles;
    }}
    """

    # # 生成JavaScript内容 - 严格按照要求的格式
    # js_lines = ["const mockFiles = ["]
    #
    # for i, file_info in enumerate(files_data):
    #     # 转义文件名中的特殊字符
    #     escaped_name = escape_js_string(file_info['name'])
    #
    #     # 构建行，属性名不带引号
    #     line = f'    {{ name: "{escaped_name}", size: "{file_info["size"]}" }}'
    #
    #     # 如果不是最后一行，添加逗号
    #     if i < len(files_data) - 1:
    #         line += ','
    #
    #     js_lines.append(line)
    #
    # js_lines.append("];")
    #
    # js_content = "\n".join(js_lines)
    
    # 写入文件
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"\n✅ 成功生成JavaScript文件: {output_filename}")
        print(f"   包含 {len(files_data)} 个文件")
        return True
        
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("文件列表生成器")
    print("=" * 50)
    
    # 询问用户是否要排除特定扩展名
    exclude_input = input("输入要排除的文件扩展名（用逗号分隔，留空使用默认[generate_filelist.py]）: ").strip()
    
    if exclude_input:
        exclude_extensions = [ext.strip() for ext in exclude_input.split(',') if ext.strip()]
    else:
        exclude_extensions = ['generate_filelist.py']
    
    # 询问输出文件名
    output_name = input("输入输出的JS文件名（留空使用 fileList.js）: ").strip()
    if not output_name:
        output_name = "fileList.js"
    
    # 生成文件列表
    success = generate_file_list_js(output_name, exclude_extensions)
    
    if success:
        print("\n🎉 脚本执行完成！")
        print("生成的JS文件内容示例:")
        print("-" * 40)
        
        # 显示前几个文件作为示例
        try:
            with open(output_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if i < 15:  # 只显示前15行
                        print(line.rstrip())
                    else:
                        print("...")
                        break
        except:
            pass
    
    input("\n按Enter键退出...")

if __name__ == "__main__":
    # 如果直接运行，使用交互模式
    if len(sys.argv) == 1:
        main()
    else:
        # 命令行参数模式
        import argparse
        
        parser = argparse.ArgumentParser(description='生成当前目录文件列表的JavaScript文件')
        parser.add_argument('-o', '--output', default='fileList.js', help='输出文件名')
        parser.add_argument('-e', '--exclude', nargs='*', default=['generate_filelist.py'],
                          help='要排除的文件扩展名')
        parser.add_argument('-q', '--quiet', action='store_true', help='安静模式，不显示详细信息')
        
        args = parser.parse_args()
        
        if not args.quiet:
            print(f"生成文件列表到: {args.output}")
            print(f"排除扩展名: {args.exclude}")
        
        generate_file_list_js(args.output, args.exclude)