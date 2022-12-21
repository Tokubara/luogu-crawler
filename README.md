本爬虫的目的是想看看洛谷上最多提交数的题目.

限于作者算法水平, 只爬取了洛谷 "普及/提高-"(3) 以及 "普及+/提高"(4) 题目的题号, 提交数, 通过数. 当然要抓取其它难度的题目也只需要调用 get_problem_list, 以及跑一遍 while 循环.  后悔没有抓取名字, 加上名字应该非常容易, 但是不想再运行一遍了.

由于不会使用代理, 害怕被封, 用的是单线程, 并且会随机等待 (0.8, 1.5)s. 可以想象很慢. 由于只爬取了 1600 道左右题目, 用时应该不会超过 1 小时.

代码是用  vscode notebook 写的, 比较凌乱, 建议运行的话也用 vscode 交互式运行.

##### 生成结果

problems.csv: 包含提交数, 通过数, 题号, 难度信息. 按照提交数降序排序. 由于没有爬取名字, 使用起来不方便, 我发现排名靠前的题目都是名字中有 "模板" 的题目.

problems_detail_dict: 比如 problems_detail["P1328"], 会是一个 dict, 有 "commit", "pass_count" 信息.

problems_detail_list: 和 problems.csv 信息相同. 相当于是 list 版的 problems.csv.

problems_dict: 比如 problems_dict["3"] 会是所有难度为 "普及/提高-" 的题目名称.

这里只上传了 problems.csv, 因为其它的都不是直接产物.

