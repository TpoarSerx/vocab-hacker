#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vocab_hacker.py - 终端风格背单词工具
作者：AI助手
适用：英语四级备考（6月13日考试）
风格：黑客帝国风 - 黑底绿字
版本：v5.0 - 伪装输出系统 + ECDICT词库(2000词)
"""

import os
import sys
import json
import random
import time
import re
from typing import List, Dict, Optional

# ============================================================
# ANSI转义码定义（纯标准库实现）
# ============================================================
class ANSI:
    """ANSI转义码常量"""
    # 颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 背景色
    BG_BLACK = '\033[40m'
    BG_GREEN = '\033[42m'
    BG_WHITE = '\033[47m'
    
    # 样式
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # 重置
    RESET = '\033[0m'
    
    # 清屏
    CLEAR_SCREEN = '\033[2J'
    CLEAR_LINE = '\033[K'
    HOME = '\033[H'
    
    # 光标控制
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'
    SAVE_CURSOR = '\033[s'
    RESTORE_CURSOR = '\033[u'

# 快捷颜色定义
class Colors:
    """常用颜色组合"""
    BOLD = ANSI.BOLD                                  # 加粗
    HACKER_GREEN = f"{ANSI.GREEN}{ANSI.BOLD}"      # 黑客绿
    HACKER_DIM = f"{ANSI.GREEN}{ANSI.DIM}"          # 暗淡绿
    ERROR_RED = f"{ANSI.RED}{ANSI.BOLD}"            # 错误红
    SUCCESS_GREEN = f"{ANSI.GREEN}{ANSI.BOLD}"     # 成功绿
    WARNING_YELLOW = f"{ANSI.YELLOW}{ANSI.BOLD}"    # 警告黄
    INFO_CYAN = f"{ANSI.CYAN}{ANSI.BOLD}"           # 信息青
    PROMPT_MAGENTA = f"{ANSI.MAGENTA}{ANSI.BOLD}"  # 提示符品红

# ============================================================
# ASCII艺术
# ============================================================
ASCII_TITLE = r"""
    _   __            __  ___                 __          
   / | / /___  ____  /  |/  /___  __________/ /__  ____ _
  /  |/ / __ \/ __ \/ /|_/ / __ \/ ___/ ___/ //_/ / __ `/
 / /|  / /_/ / /_/ / /  / / /_/ / /  / /__/ ,<   / /_/ / 
/_/ |_/\____/\____/_/  /_/\____/_/   \___/_/|_|  \__,_/  
                                                        
"""

BOOT_LOGOS = [
    r"""
    [################] 100% 系统就绪
    """,
    r"""
    ╔══════════════════════════════════╗
    ║     VOCAB_HACKER v5.0            ║
    ║     终端背单词系统               ║
    ║     备战CET-4                    ║
    ╚══════════════════════════════════╝
    """
]

# ============================================================
# CET-4 词汇库（2000个高频词汇，按真题词频排序，数据来源：exam-data/CETVocabulary）
# ============================================================
VOCABULARY = {
    "unit_1": {
        "name": "CET4词汇 第1单元",
        "words": [
            {"word": "the", "phonetic": "", "meaning": "这个、这些", "pos": ""},
            {"word": "to", "phonetic": "", "meaning": "目的、终点", "pos": ""},
            {"word": "and", "phonetic": "", "meaning": "和", "pos": ""},
            {"word": "in", "phonetic": "", "meaning": "在…内、范围", "pos": ""},
            {"word": "have", "phonetic": "", "meaning": "有", "pos": ""},
            {"word": "that", "phonetic": "", "meaning": "那", "pos": ""},
            {"word": "for", "phonetic": "", "meaning": "原因、对象", "pos": ""},
            {"word": "on", "phonetic": "", "meaning": "在…上、持续", "pos": ""},
            {"word": "they", "phonetic": "", "meaning": "他们", "pos": ""},
            {"word": "you", "phonetic": "", "meaning": "你", "pos": ""},
            {"word": "with", "phonetic": "", "meaning": "伴随", "pos": ""},
            {"word": "as", "phonetic": "", "meaning": "作为、既然、随着、就像", "pos": ""},
            {"word": "their", "phonetic": "", "meaning": "他们的", "pos": ""},
            {"word": "by", "phonetic": "", "meaning": "方式、到…为止", "pos": ""},
            {"word": "not", "phonetic": "", "meaning": "不、没有", "pos": ""},
            {"word": "he", "phonetic": "", "meaning": "他", "pos": ""},
            {"word": "from", "phonetic": "", "meaning": "从…、起点", "pos": ""},
            {"word": "at", "phonetic": "", "meaning": "在…位置", "pos": ""},
            {"word": "will", "phonetic": "", "meaning": "将、会", "pos": ""},
            {"word": "more", "phonetic": "", "meaning": "更多的", "pos": ""},
        ]
    },
    "unit_2": {
        "name": "CET4词汇 第2单元",
        "words": [
            {"word": "do", "phonetic": "", "meaning": "做", "pos": ""},
            {"word": "we", "phonetic": "", "meaning": "我们", "pos": ""},
            {"word": "passage", "phonetic": "", "meaning": "段落、通道", "pos": ""},
            {"word": "this", "phonetic": "", "meaning": "这", "pos": ""},
            {"word": "or", "phonetic": "", "meaning": "或者、否则", "pos": ""},
            {"word": "can", "phonetic": "", "meaning": "能", "pos": ""},
            {"word": "one", "phonetic": "", "meaning": "一个", "pos": ""},
            {"word": "but", "phonetic": "", "meaning": "但是", "pos": ""},
            {"word": "question", "phonetic": "", "meaning": "问题", "pos": ""},
            {"word": "people", "phonetic": "", "meaning": "人民、民族", "pos": ""},
            {"word": "what", "phonetic": "", "meaning": "什么事物", "pos": ""},
            {"word": "there", "phonetic": "", "meaning": "那里", "pos": ""},
            {"word": "well", "phonetic": "", "meaning": "好、井、涌出", "pos": ""},
            {"word": "about", "phonetic": "", "meaning": "关于", "pos": ""},
            {"word": "answer", "phonetic": "", "meaning": "回答", "pos": ""},
            {"word": "make", "phonetic": "", "meaning": "制作、使得", "pos": ""},
            {"word": "than", "phonetic": "", "meaning": "比", "pos": ""},
            {"word": "his", "phonetic": "", "meaning": "他的", "pos": ""},
            {"word": "time", "phonetic": "", "meaning": "时间", "pos": ""},
            {"word": "say", "phonetic": "", "meaning": "说、说明", "pos": ""},
        ]
    },
    "unit_3": {
        "name": "CET4词汇 第3单元",
        "words": [
            {"word": "work", "phonetic": "", "meaning": "工作", "pos": ""},
            {"word": "which", "phonetic": "", "meaning": "哪个、什么样的", "pos": ""},
            {"word": "when", "phonetic": "", "meaning": "当", "pos": ""},
            {"word": "should", "phonetic": "", "meaning": "应该", "pos": ""},
            {"word": "part", "phonetic": "", "meaning": "部分", "pos": ""},
            {"word": "your", "phonetic": "", "meaning": "你的", "pos": ""},
            {"word": "use", "phonetic": "", "meaning": "使用", "pos": ""},
            {"word": "all", "phonetic": "", "meaning": "一切", "pos": ""},
            {"word": "follow", "phonetic": "", "meaning": "跟随", "pos": ""},
            {"word": "she", "phonetic": "", "meaning": "她", "pos": ""},
            {"word": "who", "phonetic": "", "meaning": "谁", "pos": ""},
            {"word": "each", "phonetic": "", "meaning": "每个", "pos": ""},
            {"word": "some", "phonetic": "", "meaning": "一些", "pos": ""},
            {"word": "other", "phonetic": "", "meaning": "其他", "pos": ""},
            {"word": "if", "phonetic": "", "meaning": "如果、是否", "pos": ""},
            {"word": "year", "phonetic": "", "meaning": "年", "pos": ""},
            {"word": "write", "phonetic": "", "meaning": "写", "pos": ""},
            {"word": "new", "phonetic": "", "meaning": "新的", "pos": ""},
            {"word": "section", "phonetic": "", "meaning": "部分、地段", "pos": ""},
            {"word": "its", "phonetic": "", "meaning": "它的", "pos": ""},
        ]
    },
    "unit_4": {
        "name": "CET4词汇 第4单元",
        "words": [
            {"word": "word", "phonetic": "", "meaning": "说话、单词", "pos": ""},
            {"word": "mark", "phonetic": "", "meaning": "标记", "pos": ""},
            {"word": "may", "phonetic": "", "meaning": "可能、祝", "pos": ""},
            {"word": "take", "phonetic": "", "meaning": "拿走、携带", "pos": ""},
            {"word": "many", "phonetic": "", "meaning": "很多", "pos": ""},
            {"word": "most", "phonetic": "", "meaning": "最多的、大多数的", "pos": ""},
            {"word": "read", "phonetic": "", "meaning": "读", "pos": ""},
            {"word": "up", "phonetic": "", "meaning": "在...上、完成", "pos": ""},
            {"word": "her", "phonetic": "", "meaning": "她的", "pos": ""},
            {"word": "only", "phonetic": "", "meaning": "仅仅", "pos": ""},
            {"word": "would", "phonetic": "", "meaning": "愿意", "pos": ""},
            {"word": "go", "phonetic": "", "meaning": "去", "pos": ""},
            {"word": "hear", "phonetic": "", "meaning": "听到", "pos": ""},
            {"word": "give", "phonetic": "", "meaning": "给", "pos": ""},
            {"word": "base", "phonetic": "", "meaning": "基础、基地", "pos": ""},
            {"word": "no", "phonetic": "", "meaning": "否定", "pos": ""},
            {"word": "so", "phonetic": "", "meaning": "因此", "pos": ""},
            {"word": "get", "phonetic": "", "meaning": "得到", "pos": ""},
            {"word": "two", "phonetic": "", "meaning": "二", "pos": ""},
            {"word": "student", "phonetic": "", "meaning": "学生", "pos": ""},
        ]
    },
    "unit_5": {
        "name": "CET4词汇 第5单元",
        "words": [
            {"word": "our", "phonetic": "", "meaning": "我们的", "pos": ""},
            {"word": "out", "phonetic": "", "meaning": "出去、外面", "pos": ""},
            {"word": "just", "phonetic": "", "meaning": "只、仅仅", "pos": ""},
            {"word": "child", "phonetic": "", "meaning": "孩子", "pos": ""},
            {"word": "how", "phonetic": "", "meaning": "如何", "pos": ""},
            {"word": "find", "phonetic": "", "meaning": "发现", "pos": ""},
            {"word": "way", "phonetic": "", "meaning": "方式", "pos": ""},
            {"word": "into", "phonetic": "", "meaning": "进入内部", "pos": ""},
            {"word": "because", "phonetic": "", "meaning": "因为", "pos": ""},
            {"word": "sheet", "phonetic": "", "meaning": "被单、（一）张、纸", "pos": ""},
            {"word": "like", "phonetic": "", "meaning": "喜欢、像", "pos": ""},
            {"word": "through", "phonetic": "", "meaning": "通过、穿过", "pos": ""},
            {"word": "woman", "phonetic": "", "meaning": "女人", "pos": ""},
            {"word": "school", "phonetic": "", "meaning": "学校", "pos": ""},
            {"word": "think", "phonetic": "", "meaning": "认为", "pos": ""},
            {"word": "world", "phonetic": "", "meaning": "世界", "pos": ""},
            {"word": "choice", "phonetic": "", "meaning": "选择", "pos": ""},
            {"word": "change", "phonetic": "", "meaning": "改变", "pos": ""},
            {"word": "much", "phonetic": "", "meaning": "许多的、非常", "pos": ""},
            {"word": "life", "phonetic": "", "meaning": "生命、人生", "pos": ""},
        ]
    },
    "unit_6": {
        "name": "CET4词汇 第6单元",
        "words": [
            {"word": "long", "phonetic": "", "meaning": "长", "pos": ""},
            {"word": "study", "phonetic": "", "meaning": "学习", "pos": ""},
            {"word": "need", "phonetic": "", "meaning": "需要", "pos": ""},
            {"word": "first", "phonetic": "", "meaning": "第一", "pos": ""},
            {"word": "help", "phonetic": "", "meaning": "帮助", "pos": ""},
            {"word": "four", "phonetic": "", "meaning": "四", "pos": ""},
            {"word": "job", "phonetic": "", "meaning": "工作", "pos": ""},
            {"word": "learn", "phonetic": "", "meaning": "学习、了解", "pos": ""},
            {"word": "high", "phonetic": "", "meaning": "高的、高", "pos": ""},
            {"word": "now", "phonetic": "", "meaning": "现在", "pos": ""},
            {"word": "good", "phonetic": "", "meaning": "好的、货物", "pos": ""},
            {"word": "over", "phonetic": "", "meaning": "在…上方、结束", "pos": ""},
            {"word": "then", "phonetic": "", "meaning": "然后", "pos": ""},
            {"word": "minute", "phonetic": "", "meaning": "微小的、详细的", "pos": ""},
            {"word": "after", "phonetic": "", "meaning": "在…之后", "pos": ""},
            {"word": "live", "phonetic": "", "meaning": "住、生活", "pos": ""},
            {"word": "know", "phonetic": "", "meaning": "知道", "pos": ""},
            {"word": "line", "phonetic": "", "meaning": "排队、线", "pos": ""},
            {"word": "these", "phonetic": "", "meaning": "这些、这些人", "pos": ""},
            {"word": "become", "phonetic": "", "meaning": "成为、适宜", "pos": ""},
        ]
    },
    "unit_7": {
        "name": "CET4词汇 第7单元",
        "words": [
            {"word": "author", "phonetic": "", "meaning": "作者", "pos": ""},
            {"word": "could", "phonetic": "", "meaning": "能够", "pos": ""},
            {"word": "even", "phonetic": "", "meaning": "甚至", "pos": ""},
            {"word": "also", "phonetic": "", "meaning": "也", "pos": ""},
            {"word": "come", "phonetic": "", "meaning": "来", "pos": ""},
            {"word": "mean", "phonetic": "", "meaning": "意思是、意味着", "pos": ""},
            {"word": "such", "phonetic": "", "meaning": "这样的", "pos": ""},
            {"word": "letter", "phonetic": "", "meaning": "信件", "pos": ""},
            {"word": "see", "phonetic": "", "meaning": "看", "pos": ""},
            {"word": "three", "phonetic": "", "meaning": "三", "pos": ""},
            {"word": "those", "phonetic": "", "meaning": "那些", "pos": ""},
            {"word": "end", "phonetic": "", "meaning": "结束", "pos": ""},
            {"word": "once", "phonetic": "", "meaning": "曾经、一次", "pos": ""},
            {"word": "company", "phonetic": "", "meaning": "公司、陪伴", "pos": ""},
            {"word": "problem", "phonetic": "", "meaning": "问题", "pos": ""},
            {"word": "university", "phonetic": "", "meaning": "大学", "pos": ""},
            {"word": "human", "phonetic": "", "meaning": "人", "pos": ""},
            {"word": "state", "phonetic": "", "meaning": "陈述、状态", "pos": ""},
            {"word": "want", "phonetic": "", "meaning": "想要", "pos": ""},
            {"word": "must", "phonetic": "", "meaning": "必须", "pos": ""},
        ]
    },
    "unit_8": {
        "name": "CET4词汇 第8单元",
        "words": [
            {"word": "food", "phonetic": "", "meaning": "食物", "pos": ""},
            {"word": "country", "phonetic": "", "meaning": "国家", "pos": ""},
            {"word": "choose", "phonetic": "", "meaning": "选择", "pos": ""},
            {"word": "any", "phonetic": "", "meaning": "任何", "pos": ""},
            {"word": "my", "phonetic": "", "meaning": "我的", "pos": ""},
            {"word": "day", "phonetic": "", "meaning": "日子", "pos": ""},
            {"word": "less", "phonetic": "", "meaning": "更少", "pos": ""},
            {"word": "accord", "phonetic": "", "meaning": "协议、符合", "pos": ""},
            {"word": "show", "phonetic": "", "meaning": "展示、展现", "pos": ""},
            {"word": "both", "phonetic": "", "meaning": "两者", "pos": ""},
            {"word": "very", "phonetic": "", "meaning": "非常", "pos": ""},
            {"word": "great", "phonetic": "", "meaning": "巨大的", "pos": ""},
            {"word": "thing", "phonetic": "", "meaning": "事情", "pos": ""},
            {"word": "look", "phonetic": "", "meaning": "看", "pos": ""},
            {"word": "too", "phonetic": "", "meaning": "太…、也", "pos": ""},
            {"word": "business", "phonetic": "", "meaning": "商业", "pos": ""},
            {"word": "between", "phonetic": "", "meaning": "在…之间", "pos": ""},
            {"word": "research", "phonetic": "", "meaning": "研究", "pos": ""},
            {"word": "before", "phonetic": "", "meaning": "在…之前", "pos": ""},
            {"word": "number", "phonetic": "", "meaning": "数字", "pos": ""},
        ]
    },
    "unit_9": {
        "name": "CET4词汇 第9单元",
        "words": [
            {"word": "single", "phonetic": "", "meaning": "单一的", "pos": ""},
            {"word": "own", "phonetic": "", "meaning": "拥有", "pos": ""},
            {"word": "feel", "phonetic": "", "meaning": "感觉", "pos": ""},
            {"word": "family", "phonetic": "", "meaning": "家庭", "pos": ""},
            {"word": "often", "phonetic": "", "meaning": "经常", "pos": ""},
            {"word": "old", "phonetic": "", "meaning": "老的", "pos": ""},
            {"word": "parent", "phonetic": "", "meaning": "父母", "pos": ""},
            {"word": "increase", "phonetic": "", "meaning": "增加", "pos": ""},
            {"word": "paragraph", "phonetic": "", "meaning": "段落", "pos": ""},
            {"word": "provide", "phonetic": "", "meaning": "提供", "pos": ""},
            {"word": "few", "phonetic": "", "meaning": "很少", "pos": ""},
            {"word": "home", "phonetic": "", "meaning": "家", "pos": ""},
            {"word": "while", "phonetic": "", "meaning": "当…时、而、尽管", "pos": ""},
            {"word": "last", "phonetic": "", "meaning": "持续", "pos": ""},
            {"word": "point", "phonetic": "", "meaning": "点、指", "pos": ""},
            {"word": "text", "phonetic": "", "meaning": "文本", "pos": ""},
            {"word": "correspond", "phonetic": "", "meaning": "相符合、相当", "pos": ""},
            {"word": "place", "phonetic": "", "meaning": "放置、地点", "pos": ""},
            {"word": "pay", "phonetic": "", "meaning": "支付", "pos": ""},
            {"word": "language", "phonetic": "", "meaning": "语言、风格", "pos": ""},
        ]
    },
    "unit_10": {
        "name": "CET4词汇 第10单元",
        "words": [
            {"word": "still", "phonetic": "", "meaning": "仍然", "pos": ""},
            {"word": "keep", "phonetic": "", "meaning": "保持", "pos": ""},
            {"word": "where", "phonetic": "", "meaning": "哪里", "pos": ""},
            {"word": "book", "phonetic": "", "meaning": "预定、书籍", "pos": ""},
            {"word": "college", "phonetic": "", "meaning": "大学", "pos": ""},
            {"word": "second", "phonetic": "", "meaning": "第二的、次等的", "pos": ""},
            {"word": "listen", "phonetic": "", "meaning": "听", "pos": ""},
            {"word": "why", "phonetic": "", "meaning": "为什么", "pos": ""},
            {"word": "system", "phonetic": "", "meaning": "系统", "pos": ""},
            {"word": "put", "phonetic": "", "meaning": "放", "pos": ""},
            {"word": "blank", "phonetic": "", "meaning": "空白的、失色的", "pos": ""},
            {"word": "might", "phonetic": "", "meaning": "可能", "pos": ""},
            {"word": "result", "phonetic": "", "meaning": "结果", "pos": ""},
            {"word": "try", "phonetic": "", "meaning": "尝试", "pos": ""},
            {"word": "money", "phonetic": "", "meaning": "钱", "pos": ""},
            {"word": "ask", "phonetic": "", "meaning": "问", "pos": ""},
            {"word": "seem", "phonetic": "", "meaning": "似乎", "pos": ""},
            {"word": "speak", "phonetic": "", "meaning": "说", "pos": ""},
            {"word": "news", "phonetic": "", "meaning": "新闻", "pos": ""},
            {"word": "example", "phonetic": "", "meaning": "例子", "pos": ""},
        ]
    },
    "unit_11": {
        "name": "CET4词汇 第11单元",
        "words": [
            {"word": "same", "phonetic": "", "meaning": "同样的", "pos": ""},
            {"word": "important", "phonetic": "", "meaning": "重要的", "pos": ""},
            {"word": "right", "phonetic": "", "meaning": "正确的、权利", "pos": ""},
            {"word": "report", "phonetic": "", "meaning": "报告", "pos": ""},
            {"word": "believe", "phonetic": "", "meaning": "相信", "pos": ""},
            {"word": "public", "phonetic": "", "meaning": "公众的", "pos": ""},
            {"word": "health", "phonetic": "", "meaning": "健康", "pos": ""},
            {"word": "far", "phonetic": "", "meaning": "远的", "pos": ""},
            {"word": "young", "phonetic": "", "meaning": "年轻的", "pos": ""},
            {"word": "call", "phonetic": "", "meaning": "打电话", "pos": ""},
            {"word": "large", "phonetic": "", "meaning": "大的", "pos": ""},
            {"word": "city", "phonetic": "", "meaning": "城市", "pos": ""},
            {"word": "develop", "phonetic": "", "meaning": "发展", "pos": ""},
            {"word": "start", "phonetic": "", "meaning": "开始", "pos": ""},
            {"word": "another", "phonetic": "", "meaning": "另一个", "pos": ""},
            {"word": "during", "phonetic": "", "meaning": "在…期间", "pos": ""},
            {"word": "idea", "phonetic": "", "meaning": "想法", "pos": ""},
            {"word": "allow", "phonetic": "", "meaning": "允许", "pos": ""},
            {"word": "science", "phonetic": "", "meaning": "科学", "pos": ""},
            {"word": "age", "phonetic": "", "meaning": "年龄", "pos": ""},
        ]
    },
    "unit_12": {
        "name": "CET4词汇 第12单元",
        "words": [
            {"word": "every", "phonetic": "", "meaning": "每个", "pos": ""},
            {"word": "leave", "phonetic": "", "meaning": "离开", "pos": ""},
            {"word": "talk", "phonetic": "", "meaning": "说", "pos": ""},
            {"word": "require", "phonetic": "", "meaning": "需要、要求", "pos": ""},
            {"word": "car", "phonetic": "", "meaning": "车", "pos": ""},
            {"word": "society", "phonetic": "", "meaning": "社会", "pos": ""},
            {"word": "short", "phonetic": "", "meaning": "短", "pos": ""},
            {"word": "cause", "phonetic": "", "meaning": "造成", "pos": ""},
            {"word": "down", "phonetic": "", "meaning": "在…下面、情绪低落", "pos": ""},
            {"word": "technology", "phonetic": "", "meaning": "技术、工艺", "pos": ""},
            {"word": "grow", "phonetic": "", "meaning": "成长、增长", "pos": ""},
            {"word": "sentence", "phonetic": "", "meaning": "判决", "pos": ""},
            {"word": "without", "phonetic": "", "meaning": "没有", "pos": ""},
            {"word": "hour", "phonetic": "", "meaning": "小时", "pos": ""},
            {"word": "big", "phonetic": "", "meaning": "大", "pos": ""},
            {"word": "begin", "phonetic": "", "meaning": "开始", "pos": ""},
            {"word": "lead", "phonetic": "", "meaning": "带领", "pos": ""},
            {"word": "build", "phonetic": "", "meaning": "建造", "pos": ""},
            {"word": "early", "phonetic": "", "meaning": "早期的", "pos": ""},
            {"word": "off", "phonetic": "", "meaning": "关闭、不在原处", "pos": ""},
        ]
    },
    "unit_13": {
        "name": "CET4词汇 第13单元",
        "words": [
            {"word": "spend", "phonetic": "", "meaning": "花", "pos": ""},
            {"word": "little", "phonetic": "", "meaning": "少、小", "pos": ""},
            {"word": "bank", "phonetic": "", "meaning": "银行", "pos": ""},
            {"word": "hard", "phonetic": "", "meaning": "困难的", "pos": ""},
            {"word": "class", "phonetic": "", "meaning": "班级", "pos": ""},
            {"word": "cost", "phonetic": "", "meaning": "花费", "pos": ""},
            {"word": "group", "phonetic": "", "meaning": "小组", "pos": ""},
            {"word": "price", "phonetic": "", "meaning": "价格", "pos": ""},
            {"word": "effect", "phonetic": "", "meaning": "效果", "pos": ""},
            {"word": "today", "phonetic": "", "meaning": "在今天、现今", "pos": ""},
            {"word": "tell", "phonetic": "", "meaning": "告诉", "pos": ""},
            {"word": "set", "phonetic": "", "meaning": "设定", "pos": ""},
            {"word": "something", "phonetic": "", "meaning": "某事", "pos": ""},
            {"word": "play", "phonetic": "", "meaning": "玩、扮演、戏剧", "pos": ""},
            {"word": "course", "phonetic": "", "meaning": "课程", "pos": ""},
            {"word": "buy", "phonetic": "", "meaning": "购买", "pos": ""},
            {"word": "understand", "phonetic": "", "meaning": "理解", "pos": ""},
            {"word": "offer", "phonetic": "", "meaning": "提供", "pos": ""},
            {"word": "small", "phonetic": "", "meaning": "小的", "pos": ""},
            {"word": "product", "phonetic": "", "meaning": "产品", "pos": ""},
        ]
    },
    "unit_14": {
        "name": "CET4词汇 第14单元",
        "words": [
            {"word": "experience", "phonetic": "", "meaning": "经历", "pos": ""},
            {"word": "suggest", "phonetic": "", "meaning": "建议", "pos": ""},
            {"word": "decide", "phonetic": "", "meaning": "决定", "pos": ""},
            {"word": "test", "phonetic": "", "meaning": "测试", "pos": ""},
            {"word": "bring", "phonetic": "", "meaning": "带来", "pos": ""},
            {"word": "since", "phonetic": "", "meaning": "自从、因为、既然", "pos": ""},
            {"word": "however", "phonetic": "", "meaning": "但是、然而", "pos": ""},
            {"word": "person", "phonetic": "", "meaning": "人", "pos": ""},
            {"word": "around", "phonetic": "", "meaning": "周围、环绕", "pos": ""},
            {"word": "whether", "phonetic": "", "meaning": "是否", "pos": ""},
            {"word": "future", "phonetic": "", "meaning": "未来", "pos": ""},
            {"word": "reason", "phonetic": "", "meaning": "理由", "pos": ""},
            {"word": "view", "phonetic": "", "meaning": "景观", "pos": ""},
            {"word": "water", "phonetic": "", "meaning": "水", "pos": ""},
            {"word": "improve", "phonetic": "", "meaning": "改进、提高", "pos": ""},
            {"word": "care", "phonetic": "", "meaning": "关心、在意", "pos": ""},
            {"word": "benefit", "phonetic": "", "meaning": "益处、好处", "pos": ""},
            {"word": "low", "phonetic": "", "meaning": "低的", "pos": ""},
            {"word": "program", "phonetic": "", "meaning": "项目", "pos": ""},
            {"word": "market", "phonetic": "", "meaning": "市场", "pos": ""},
        ]
    },
    "unit_15": {
        "name": "CET4词汇 第15单元",
        "words": [
            {"word": "teach", "phonetic": "", "meaning": "教", "pos": ""},
            {"word": "support", "phonetic": "", "meaning": "支持", "pos": ""},
            {"word": "among", "phonetic": "", "meaning": "在……之中", "pos": ""},
            {"word": "kind", "phonetic": "", "meaning": "仁慈的、种类", "pos": ""},
            {"word": "friend", "phonetic": "", "meaning": "朋友", "pos": ""},
            {"word": "skill", "phonetic": "", "meaning": "技术", "pos": ""},
            {"word": "yet", "phonetic": "", "meaning": "然而", "pos": ""},
            {"word": "form", "phonetic": "", "meaning": "形式、形成", "pos": ""},
            {"word": "include", "phonetic": "", "meaning": "包括", "pos": ""},
            {"word": "move", "phonetic": "", "meaning": "移动", "pos": ""},
            {"word": "create", "phonetic": "", "meaning": "创造", "pos": ""},
            {"word": "never", "phonetic": "", "meaning": "从不", "pos": ""},
            {"word": "rather", "phonetic": "", "meaning": "相当的", "pos": ""},
            {"word": "century", "phonetic": "", "meaning": "世纪", "pos": ""},
            {"word": "bad", "phonetic": "", "meaning": "坏的", "pos": ""},
            {"word": "eat", "phonetic": "", "meaning": "吃", "pos": ""},
            {"word": "always", "phonetic": "", "meaning": "总是", "pos": ""},
            {"word": "least", "phonetic": "", "meaning": "最小的、最少的", "pos": ""},
            {"word": "face", "phonetic": "", "meaning": "面对", "pos": ""},
            {"word": "plan", "phonetic": "", "meaning": "计划", "pos": ""},
        ]
    },
    "unit_16": {
        "name": "CET4词汇 第16单元",
        "words": [
            {"word": "consider", "phonetic": "", "meaning": "考虑", "pos": ""},
            {"word": "industry", "phonetic": "", "meaning": "工业、行业", "pos": ""},
            {"word": "themselves", "phonetic": "", "meaning": "他们自己、他们亲自", "pos": ""},
            {"word": "process", "phonetic": "", "meaning": "过程、进程", "pos": ""},
            {"word": "rate", "phonetic": "", "meaning": "比率", "pos": ""},
            {"word": "fact", "phonetic": "", "meaning": "事实", "pos": ""},
            {"word": "house", "phonetic": "", "meaning": "房子", "pos": ""},
            {"word": "culture", "phonetic": "", "meaning": "文化", "pos": ""},
            {"word": "power", "phonetic": "", "meaning": "力、功率", "pos": ""},
            {"word": "share", "phonetic": "", "meaning": "分享", "pos": ""},
            {"word": "area", "phonetic": "", "meaning": "地区、范围", "pos": ""},
            {"word": "million", "phonetic": "", "meaning": "百万", "pos": ""},
            {"word": "lot", "phonetic": "", "meaning": "很、许多", "pos": ""},
            {"word": "sense", "phonetic": "", "meaning": "感觉", "pos": ""},
            {"word": "lose", "phonetic": "", "meaning": "失去、失败", "pos": ""},
            {"word": "against", "phonetic": "", "meaning": "相对、相反", "pos": ""},
            {"word": "rise", "phonetic": "", "meaning": "上升", "pos": ""},
            {"word": "energy", "phonetic": "", "meaning": "精力", "pos": ""},
            {"word": "control", "phonetic": "", "meaning": "控制", "pos": ""},
            {"word": "space", "phonetic": "", "meaning": "空间", "pos": ""},
        ]
    },
    "unit_17": {
        "name": "CET4词汇 第17单元",
        "words": [
            {"word": "case", "phonetic": "", "meaning": "情况", "pos": ""},
            {"word": "hold", "phonetic": "", "meaning": "握着、坚持", "pos": ""},
            {"word": "possible", "phonetic": "", "meaning": "可能的", "pos": ""},
            {"word": "animal", "phonetic": "", "meaning": "动物", "pos": ""},
            {"word": "enough", "phonetic": "", "meaning": "足够", "pos": ""},
            {"word": "value", "phonetic": "", "meaning": "价值", "pos": ""},
            {"word": "role", "phonetic": "", "meaning": "角色", "pos": ""},
            {"word": "week", "phonetic": "", "meaning": "周末", "pos": ""},
            {"word": "individual", "phonetic": "", "meaning": "个人的、独特的", "pos": ""},
            {"word": "hand", "phonetic": "", "meaning": "手", "pos": ""},
            {"word": "open", "phonetic": "", "meaning": "打开", "pos": ""},
            {"word": "ten", "phonetic": "", "meaning": "十", "pos": ""},
            {"word": "term", "phonetic": "", "meaning": "条款、期限", "pos": ""},
            {"word": "away", "phonetic": "", "meaning": "离开", "pos": ""},
            {"word": "happen", "phonetic": "", "meaning": "发生", "pos": ""},
            {"word": "fall", "phonetic": "", "meaning": "掉落", "pos": ""},
            {"word": "art", "phonetic": "", "meaning": "艺术", "pos": ""},
            {"word": "self", "phonetic": "", "meaning": "自我、自己", "pos": ""},
            {"word": "drive", "phonetic": "", "meaning": "驾驶、驱使", "pos": ""},
            {"word": "interest", "phonetic": "", "meaning": "兴趣", "pos": ""},
        ]
    },
    "unit_18": {
        "name": "CET4词汇 第18单元",
        "words": [
            {"word": "issue", "phonetic": "", "meaning": "问题、期刊、发布", "pos": ""},
            {"word": "produce", "phonetic": "", "meaning": "生产", "pos": ""},
            {"word": "complete", "phonetic": "", "meaning": "完全地", "pos": ""},
            {"word": "under", "phonetic": "", "meaning": "在…之下", "pos": ""},
            {"word": "brain", "phonetic": "", "meaning": "大脑", "pos": ""},
            {"word": "level", "phonetic": "", "meaning": "水平、等级", "pos": ""},
            {"word": "able", "phonetic": "", "meaning": "有能力的", "pos": ""},
            {"word": "run", "phonetic": "", "meaning": "跑步、运转", "pos": ""},
            {"word": "past", "phonetic": "", "meaning": "过渡的", "pos": ""},
            {"word": "win", "phonetic": "", "meaning": "赢", "pos": ""},
            {"word": "present", "phonetic": "", "meaning": "呈现、提出、礼物、现在", "pos": ""},
            {"word": "quality", "phonetic": "", "meaning": "质量", "pos": ""},
            {"word": "difficult", "phonetic": "", "meaning": "困难的", "pos": ""},
            {"word": "easy", "phonetic": "", "meaning": "容易的", "pos": ""},
            {"word": "reduce", "phonetic": "", "meaning": "减少", "pos": ""},
            {"word": "tend", "phonetic": "", "meaning": "趋向于、照料", "pos": ""},
            {"word": "five", "phonetic": "", "meaning": "五", "pos": ""},
            {"word": "expect", "phonetic": "", "meaning": "预料、期待", "pos": ""},
            {"word": "order", "phonetic": "", "meaning": "订单、命令、顺序", "pos": ""},
            {"word": "environment", "phonetic": "", "meaning": "环境、自然环境", "pos": ""},
        ]
    },
    "unit_19": {
        "name": "CET4词汇 第19单元",
        "words": [
            {"word": "law", "phonetic": "", "meaning": "法律、法则", "pos": ""},
            {"word": "paper", "phonetic": "", "meaning": "纸、试卷", "pos": ""},
            {"word": "kid", "phonetic": "", "meaning": "孩子", "pos": ""},
            {"word": "mind", "phonetic": "", "meaning": "思维、想法", "pos": ""},
            {"word": "economy", "phonetic": "", "meaning": "经济", "pos": ""},
            {"word": "percent", "phonetic": "", "meaning": "百分之的", "pos": ""},
            {"word": "sleep", "phonetic": "", "meaning": "睡眠", "pos": ""},
            {"word": "recent", "phonetic": "", "meaning": "近来的", "pos": ""},
            {"word": "half", "phonetic": "", "meaning": "一半", "pos": ""},
            {"word": "close", "phonetic": "", "meaning": "关闭、近", "pos": ""},
            {"word": "attention", "phonetic": "", "meaning": "注意", "pos": ""},
            {"word": "free", "phonetic": "", "meaning": "自由的", "pos": ""},
            {"word": "poor", "phonetic": "", "meaning": "糟糕的", "pos": ""},
            {"word": "body", "phonetic": "", "meaning": "身体", "pos": ""},
            {"word": "measure", "phonetic": "", "meaning": "衡量、测量", "pos": ""},
            {"word": "office", "phonetic": "", "meaning": "办公室", "pos": ""},
            {"word": "travel", "phonetic": "", "meaning": "旅行", "pos": ""},
            {"word": "major", "phonetic": "", "meaning": "主要的", "pos": ""},
            {"word": "professor", "phonetic": "", "meaning": "教授", "pos": ""},
            {"word": "remain", "phonetic": "", "meaning": "保持", "pos": ""},
        ]
    },
    "unit_20": {
        "name": "CET4词汇 第20单元",
        "words": [
            {"word": "though", "phonetic": "", "meaning": "尽管", "pos": ""},
            {"word": "next", "phonetic": "", "meaning": "下一个", "pos": ""},
            {"word": "design", "phonetic": "", "meaning": "设计", "pos": ""},
            {"word": "history", "phonetic": "", "meaning": "历史", "pos": ""},
            {"word": "nation", "phonetic": "", "meaning": "国家", "pos": ""},
            {"word": "real", "phonetic": "", "meaning": "真的", "pos": ""},
            {"word": "almost", "phonetic": "", "meaning": "几乎", "pos": ""},
            {"word": "customer", "phonetic": "", "meaning": "顾客", "pos": ""},
            {"word": "subject", "phonetic": "", "meaning": "科目", "pos": ""},
            {"word": "ago", "phonetic": "", "meaning": "以前", "pos": ""},
            {"word": "focus", "phonetic": "", "meaning": "聚焦、焦点", "pos": ""},
            {"word": "local", "phonetic": "", "meaning": "当地的", "pos": ""},
            {"word": "certain", "phonetic": "", "meaning": "确定的", "pos": ""},
            {"word": "ever", "phonetic": "", "meaning": "从来", "pos": ""},
            {"word": "success", "phonetic": "", "meaning": "成功", "pos": ""},
            {"word": "late", "phonetic": "", "meaning": "晚的", "pos": ""},
            {"word": "true", "phonetic": "", "meaning": "真实", "pos": ""},
            {"word": "name", "phonetic": "", "meaning": "叩召", "pos": ""},
            {"word": "matter", "phonetic": "", "meaning": "事情、问题、重要", "pos": ""},
            {"word": "stress", "phonetic": "", "meaning": "压力", "pos": ""},
        ]
    },
    "unit_21": {
        "name": "CET4词汇 第21单元",
        "words": [
            {"word": "identify", "phonetic": "", "meaning": "识别、鉴定", "pos": ""},
            {"word": "involve", "phonetic": "", "meaning": "涉及", "pos": ""},
            {"word": "raise", "phonetic": "", "meaning": "举起、提出", "pos": ""},
            {"word": "online", "phonetic": "", "meaning": "在线的", "pos": ""},
            {"word": "stay", "phonetic": "", "meaning": "保持、停留", "pos": ""},
            {"word": "population", "phonetic": "", "meaning": "人口", "pos": ""},
            {"word": "risk", "phonetic": "", "meaning": "风险", "pos": ""},
            {"word": "medium", "phonetic": "", "meaning": "中等的、媒介", "pos": ""},
            {"word": "fill", "phonetic": "", "meaning": "填", "pos": ""},
            {"word": "lack", "phonetic": "", "meaning": "缺乏", "pos": ""},
            {"word": "strong", "phonetic": "", "meaning": "强壮的、强烈的", "pos": ""},
            {"word": "patient", "phonetic": "", "meaning": "有耐心的、病人", "pos": ""},
            {"word": "rule", "phonetic": "", "meaning": "规则", "pos": ""},
            {"word": "until", "phonetic": "", "meaning": "直到", "pos": ""},
            {"word": "continue", "phonetic": "", "meaning": "继续", "pos": ""},
            {"word": "receive", "phonetic": "", "meaning": "收到", "pos": ""},
            {"word": "already", "phonetic": "", "meaning": "已经", "pos": ""},
            {"word": "record", "phonetic": "", "meaning": "记录", "pos": ""},
            {"word": "sell", "phonetic": "", "meaning": "卖", "pos": ""},
            {"word": "month", "phonetic": "", "meaning": "月", "pos": ""},
        ]
    },
    "unit_22": {
        "name": "CET4词汇 第22单元",
        "words": [
            {"word": "note", "phonetic": "", "meaning": "笔记", "pos": ""},
            {"word": "community", "phonetic": "", "meaning": "社区、共同体", "pos": ""},
            {"word": "demand", "phonetic": "", "meaning": "要求", "pos": ""},
            {"word": "instead", "phonetic": "", "meaning": "反而", "pos": ""},
            {"word": "challenge", "phonetic": "", "meaning": "挑战", "pos": ""},
            {"word": "store", "phonetic": "", "meaning": "存储、商店", "pos": ""},
            {"word": "check", "phonetic": "", "meaning": "检查", "pos": ""},
            {"word": "deal", "phonetic": "", "meaning": "处理", "pos": ""},
            {"word": "opportunity", "phonetic": "", "meaning": "机会", "pos": ""},
            {"word": "list", "phonetic": "", "meaning": "清单", "pos": ""},
            {"word": "average", "phonetic": "", "meaning": "平均的", "pos": ""},
            {"word": "although", "phonetic": "", "meaning": "尽管", "pos": ""},
            {"word": "break", "phonetic": "", "meaning": "打破", "pos": ""},
            {"word": "eye", "phonetic": "", "meaning": "眼睛", "pos": ""},
            {"word": "fast", "phonetic": "", "meaning": "快", "pos": ""},
            {"word": "common", "phonetic": "", "meaning": "普通的", "pos": ""},
            {"word": "condition", "phonetic": "", "meaning": "条件、情况", "pos": ""},
            {"word": "within", "phonetic": "", "meaning": "内部", "pos": ""},
            {"word": "light", "phonetic": "", "meaning": "点亮、轻的", "pos": ""},
            {"word": "meet", "phonetic": "", "meaning": "遇见、会见", "pos": ""},
        ]
    },
    "unit_23": {
        "name": "CET4词汇 第23单元",
        "words": [
            {"word": "shop", "phonetic": "", "meaning": "购物", "pos": ""},
            {"word": "concern", "phonetic": "", "meaning": "关心、涉及", "pos": ""},
            {"word": "task", "phonetic": "", "meaning": "任务", "pos": ""},
            {"word": "effort", "phonetic": "", "meaning": "努力", "pos": ""},
            {"word": "plant", "phonetic": "", "meaning": "植物、工厂", "pos": ""},
            {"word": "encourage", "phonetic": "", "meaning": "鼓励、发展", "pos": ""},
            {"word": "career", "phonetic": "", "meaning": "职业", "pos": ""},
            {"word": "fail", "phonetic": "", "meaning": "衰退、破产", "pos": ""},
            {"word": "avoid", "phonetic": "", "meaning": "避免", "pos": ""},
            {"word": "influence", "phonetic": "", "meaning": "影响", "pos": ""},
            {"word": "music", "phonetic": "", "meaning": "音乐", "pos": ""},
            {"word": "add", "phonetic": "", "meaning": "增加", "pos": ""},
            {"word": "item", "phonetic": "", "meaning": "物品", "pos": ""},
            {"word": "policy", "phonetic": "", "meaning": "政策", "pos": ""},
            {"word": "force", "phonetic": "", "meaning": "强迫、迫使", "pos": ""},
            {"word": "member", "phonetic": "", "meaning": "成员", "pos": ""},
            {"word": "cut", "phonetic": "", "meaning": "切、砍", "pos": ""},
            {"word": "enjoy", "phonetic": "", "meaning": "享受", "pos": ""},
            {"word": "explain", "phonetic": "", "meaning": "解释", "pos": ""},
            {"word": "side", "phonetic": "", "meaning": "一边", "pos": ""},
        ]
    },
    "unit_24": {
        "name": "CET4词汇 第24单元",
        "words": [
            {"word": "adult", "phonetic": "", "meaning": "大人、成人", "pos": ""},
            {"word": "general", "phonetic": "", "meaning": "一般的、总的、将军", "pos": ""},
            {"word": "international", "phonetic": "", "meaning": "国际的", "pos": ""},
            {"word": "nature", "phonetic": "", "meaning": "自然界、性质", "pos": ""},
            {"word": "type", "phonetic": "", "meaning": "类型、输入", "pos": ""},
            {"word": "doctor", "phonetic": "", "meaning": "医生", "pos": ""},
            {"word": "mother", "phonetic": "", "meaning": "妈妈", "pos": ""},
            {"word": "save", "phonetic": "", "meaning": "保存、拯救", "pos": ""},
            {"word": "several", "phonetic": "", "meaning": "几个", "pos": ""},
            {"word": "situation", "phonetic": "", "meaning": "情况", "pos": ""},
            {"word": "essay", "phonetic": "", "meaning": "论文", "pos": ""},
            {"word": "game", "phonetic": "", "meaning": "游戏", "pos": ""},
            {"word": "graduate", "phonetic": "", "meaning": "毕业、获学位", "pos": ""},
            {"word": "decade", "phonetic": "", "meaning": "十年", "pos": ""},
            {"word": "medical", "phonetic": "", "meaning": "医疗的", "pos": ""},
            {"word": "miss", "phonetic": "", "meaning": "错过、想念", "pos": ""},
            {"word": "train", "phonetic": "", "meaning": "列车、行列", "pos": ""},
            {"word": "interview", "phonetic": "", "meaning": "采访、面试", "pos": ""},
            {"word": "third", "phonetic": "", "meaning": "第三", "pos": ""},
            {"word": "stop", "phonetic": "", "meaning": "阻止", "pos": ""},
        ]
    },
    "unit_25": {
        "name": "CET4词汇 第25单元",
        "words": [
            {"word": "reach", "phonetic": "", "meaning": "到达、达到", "pos": ""},
            {"word": "sign", "phonetic": "", "meaning": "标牌", "pos": ""},
            {"word": "earth", "phonetic": "", "meaning": "地球、泥土", "pos": ""},
            {"word": "project", "phonetic": "", "meaning": "项目、计划", "pos": ""},
            {"word": "generation", "phonetic": "", "meaning": "产生、一代人", "pos": ""},
            {"word": "rich", "phonetic": "", "meaning": "丰富的", "pos": ""},
            {"word": "standard", "phonetic": "", "meaning": "标准", "pos": ""},
            {"word": "story", "phonetic": "", "meaning": "故事", "pos": ""},
            {"word": "war", "phonetic": "", "meaning": "战争", "pos": ""},
            {"word": "again", "phonetic": "", "meaning": "再次", "pos": ""},
            {"word": "air", "phonetic": "", "meaning": "空气", "pos": ""},
            {"word": "contain", "phonetic": "", "meaning": "包含", "pos": ""},
            {"word": "night", "phonetic": "", "meaning": "夜晚", "pos": ""},
            {"word": "main", "phonetic": "", "meaning": "主要的", "pos": ""},
            {"word": "love", "phonetic": "", "meaning": "爱", "pos": ""},
            {"word": "soon", "phonetic": "", "meaning": "很快的", "pos": ""},
            {"word": "sound", "phonetic": "", "meaning": "声音", "pos": ""},
            {"word": "account", "phonetic": "", "meaning": "账户", "pos": ""},
            {"word": "affect", "phonetic": "", "meaning": "影响", "pos": ""},
            {"word": "return", "phonetic": "", "meaning": "回归、返回", "pos": ""},
        ]
    },
    "unit_26": {
        "name": "CET4词汇 第26单元",
        "words": [
            {"word": "sure", "phonetic": "", "meaning": "肯定的", "pos": ""},
            {"word": "translate", "phonetic": "", "meaning": "解释、翻译、转变", "pos": ""},
            {"word": "describe", "phonetic": "", "meaning": "描述", "pos": ""},
            {"word": "full", "phonetic": "", "meaning": "满的", "pos": ""},
            {"word": "purpose", "phonetic": "", "meaning": "目的", "pos": ""},
            {"word": "room", "phonetic": "", "meaning": "房间", "pos": ""},
            {"word": "appear", "phonetic": "", "meaning": "出现", "pos": ""},
            {"word": "center", "phonetic": "", "meaning": "中心", "pos": ""},
            {"word": "impact", "phonetic": "", "meaning": "冲击", "pos": ""},
            {"word": "period", "phonetic": "", "meaning": "一段时间", "pos": ""},
            {"word": "quite", "phonetic": "", "meaning": "相当的", "pos": ""},
            {"word": "television", "phonetic": "", "meaning": "电视", "pos": ""},
            {"word": "position", "phonetic": "", "meaning": "位置", "pos": ""},
            {"word": "attitude", "phonetic": "", "meaning": "态度", "pos": ""},
            {"word": "machine", "phonetic": "", "meaning": "机器", "pos": ""},
            {"word": "clear", "phonetic": "", "meaning": "清楚的", "pos": ""},
            {"word": "field", "phonetic": "", "meaning": "田地、场地、领域", "pos": ""},
            {"word": "pass", "phonetic": "", "meaning": "经过", "pos": ""},
            {"word": "below", "phonetic": "", "meaning": "在…下面", "pos": ""},
            {"word": "here", "phonetic": "", "meaning": "这里", "pos": ""},
        ]
    },
    "unit_27": {
        "name": "CET4词汇 第27单元",
        "words": [
            {"word": "protect", "phonetic": "", "meaning": "保护", "pos": ""},
            {"word": "lecture", "phonetic": "", "meaning": "讲座", "pos": ""},
            {"word": "factor", "phonetic": "", "meaning": "因素、因子", "pos": ""},
            {"word": "top", "phonetic": "", "meaning": "顶端", "pos": ""},
            {"word": "draw", "phonetic": "", "meaning": "画画", "pos": ""},
            {"word": "firm", "phonetic": "", "meaning": "牢固的", "pos": ""},
            {"word": "memory", "phonetic": "", "meaning": "记忆", "pos": ""},
            {"word": "whole", "phonetic": "", "meaning": "全部的", "pos": ""},
            {"word": "watch", "phonetic": "", "meaning": "观看", "pos": ""},
            {"word": "death", "phonetic": "", "meaning": "死亡", "pos": ""},
            {"word": "white", "phonetic": "", "meaning": "白色的", "pos": ""},
            {"word": "bear", "phonetic": "", "meaning": "携带、承受", "pos": ""},
            {"word": "claim", "phonetic": "", "meaning": "索要、声称", "pos": ""},
            {"word": "decline", "phonetic": "", "meaning": "拒绝、下降", "pos": ""},
            {"word": "model", "phonetic": "", "meaning": "模型", "pos": ""},
            {"word": "wrong", "phonetic": "", "meaning": "错误的", "pos": ""},
            {"word": "expert", "phonetic": "", "meaning": "专家、专门的", "pos": ""},
            {"word": "act", "phonetic": "", "meaning": "行为、行动、扮演", "pos": ""},
            {"word": "carry", "phonetic": "", "meaning": "携带", "pos": ""},
            {"word": "send", "phonetic": "", "meaning": "发送", "pos": ""},
        ]
    },
    "unit_28": {
        "name": "CET4词汇 第28单元",
        "words": [
            {"word": "accept", "phonetic": "", "meaning": "接受", "pos": ""},
            {"word": "degree", "phonetic": "", "meaning": "温度、程度", "pos": ""},
            {"word": "potential", "phonetic": "", "meaning": "潜在的", "pos": ""},
            {"word": "pause", "phonetic": "", "meaning": "暂停", "pos": ""},
            {"word": "amount", "phonetic": "", "meaning": "数量", "pos": ""},
            {"word": "income", "phonetic": "", "meaning": "收入", "pos": ""},
            {"word": "opinion", "phonetic": "", "meaning": "意见", "pos": ""},
            {"word": "disease", "phonetic": "", "meaning": "疾病", "pos": ""},
            {"word": "stand", "phonetic": "", "meaning": "站立", "pos": ""},
            {"word": "popular", "phonetic": "", "meaning": "受欢迎的", "pos": ""},
            {"word": "argue", "phonetic": "", "meaning": "论述、争论、争吵", "pos": ""},
            {"word": "physical", "phonetic": "", "meaning": "自然科学的、肉体的", "pos": ""},
            {"word": "team", "phonetic": "", "meaning": "团队", "pos": ""},
            {"word": "material", "phonetic": "", "meaning": "材料", "pos": ""},
            {"word": "compare", "phonetic": "", "meaning": "比较", "pos": ""},
            {"word": "prove", "phonetic": "", "meaning": "证明", "pos": ""},
            {"word": "nothing", "phonetic": "", "meaning": "没有", "pos": ""},
            {"word": "perhaps", "phonetic": "", "meaning": "也许", "pos": ""},
            {"word": "please", "phonetic": "", "meaning": "请、使愉快", "pos": ""},
            {"word": "private", "phonetic": "", "meaning": "私人的", "pos": ""},
        ]
    },
    "unit_29": {
        "name": "CET4词汇 第29单元",
        "words": [
            {"word": "head", "phonetic": "", "meaning": "前往", "pos": ""},
            {"word": "street", "phonetic": "", "meaning": "街道", "pos": ""},
            {"word": "available", "phonetic": "", "meaning": "可行的", "pos": ""},
            {"word": "boy", "phonetic": "", "meaning": "男孩", "pos": ""},
            {"word": "current", "phonetic": "", "meaning": "当前、电流、趋向", "pos": ""},
            {"word": "goal", "phonetic": "", "meaning": "目标", "pos": ""},
            {"word": "speed", "phonetic": "", "meaning": "加速", "pos": ""},
            {"word": "together", "phonetic": "", "meaning": "一共", "pos": ""},
            {"word": "along", "phonetic": "", "meaning": "沿着", "pos": ""},
            {"word": "middle", "phonetic": "", "meaning": "中间的", "pos": ""},
            {"word": "sale", "phonetic": "", "meaning": "销售", "pos": ""},
            {"word": "grade", "phonetic": "", "meaning": "年级", "pos": ""},
            {"word": "visit", "phonetic": "", "meaning": "拜访", "pos": ""},
            {"word": "content", "phonetic": "", "meaning": "内容、目录、满足的", "pos": ""},
            {"word": "source", "phonetic": "", "meaning": "来源", "pos": ""},
            {"word": "across", "phonetic": "", "meaning": "穿过", "pos": ""},
            {"word": "gap", "phonetic": "", "meaning": "间隙、分歧", "pos": ""},
            {"word": "let", "phonetic": "", "meaning": "让", "pos": ""},
            {"word": "depend", "phonetic": "", "meaning": "依赖", "pos": ""},
            {"word": "especially", "phonetic": "", "meaning": "尤其", "pos": ""},
        ]
    },
    "unit_30": {
        "name": "CET4词汇 第30单元",
        "words": [
            {"word": "farm", "phonetic": "", "meaning": "农场", "pos": ""},
            {"word": "modern", "phonetic": "", "meaning": "现代的", "pos": ""},
            {"word": "approach", "phonetic": "", "meaning": "接近、方法", "pos": ""},
            {"word": "correct", "phonetic": "", "meaning": "更正、纠正", "pos": ""},
            {"word": "hope", "phonetic": "", "meaning": "希望", "pos": ""},
            {"word": "someone", "phonetic": "", "meaning": "某人", "pos": ""},
            {"word": "special", "phonetic": "", "meaning": "特别的", "pos": ""},
            {"word": "picture", "phonetic": "", "meaning": "图片", "pos": ""},
            {"word": "survey", "phonetic": "", "meaning": "调查、测量", "pos": ""},
            {"word": "event", "phonetic": "", "meaning": "事件", "pos": ""},
            {"word": "everyone", "phonetic": "", "meaning": "每人", "pos": ""},
            {"word": "either", "phonetic": "", "meaning": "两者之一", "pos": ""},
            {"word": "step", "phonetic": "", "meaning": "迈步", "pos": ""},
            {"word": "habit", "phonetic": "", "meaning": "习惯", "pos": ""},
            {"word": "similar", "phonetic": "", "meaning": "相似的", "pos": ""},
            {"word": "chance", "phonetic": "", "meaning": "机会", "pos": ""},
            {"word": "necessary", "phonetic": "", "meaning": "必要的", "pos": ""},
            {"word": "apply", "phonetic": "", "meaning": "应用", "pos": ""},
            {"word": "father", "phonetic": "", "meaning": "父亲", "pos": ""},
            {"word": "foreign", "phonetic": "", "meaning": "国外的", "pos": ""},
        ]
    },
    "unit_31": {
        "name": "CET4词汇 第31单元",
        "words": [
            {"word": "access", "phonetic": "", "meaning": "进入、存取", "pos": ""},
            {"word": "anything", "phonetic": "", "meaning": "任何事", "pos": ""},
            {"word": "oil", "phonetic": "", "meaning": "油", "pos": ""},
            {"word": "sport", "phonetic": "", "meaning": "体育运动", "pos": ""},
            {"word": "exist", "phonetic": "", "meaning": "存在", "pos": ""},
            {"word": "advantage", "phonetic": "", "meaning": "优势", "pos": ""},
            {"word": "agree", "phonetic": "", "meaning": "同意", "pos": ""},
            {"word": "newspaper", "phonetic": "", "meaning": "报纸", "pos": ""},
            {"word": "remember", "phonetic": "", "meaning": "记得", "pos": ""},
            {"word": "land", "phonetic": "", "meaning": "着陆、土地", "pos": ""},
            {"word": "solve", "phonetic": "", "meaning": "解答", "pos": ""},
            {"word": "function", "phonetic": "", "meaning": "功能", "pos": ""},
            {"word": "phrase", "phonetic": "", "meaning": "短语", "pos": ""},
            {"word": "everything", "phonetic": "", "meaning": "每件事", "pos": ""},
            {"word": "experiment", "phonetic": "", "meaning": "实验", "pos": ""},
            {"word": "sit", "phonetic": "", "meaning": "坐在", "pos": ""},
            {"word": "structure", "phonetic": "", "meaning": "结构", "pos": ""},
            {"word": "message", "phonetic": "", "meaning": "消息", "pos": ""},
            {"word": "seek", "phonetic": "", "meaning": "寻求", "pos": ""},
            {"word": "per", "phonetic": "", "meaning": "每、经", "pos": ""},
        ]
    },
    "unit_32": {
        "name": "CET4词汇 第32单元",
        "words": [
            {"word": "promote", "phonetic": "", "meaning": "促进", "pos": ""},
            {"word": "figure", "phonetic": "", "meaning": "算计、人物、数字", "pos": ""},
            {"word": "road", "phonetic": "", "meaning": "路", "pos": ""},
            {"word": "limit", "phonetic": "", "meaning": "限制", "pos": ""},
            {"word": "sometimes", "phonetic": "", "meaning": "有时", "pos": ""},
            {"word": "fear", "phonetic": "", "meaning": "恐惧", "pos": ""},
            {"word": "supply", "phonetic": "", "meaning": "供应", "pos": ""},
            {"word": "relate", "phonetic": "", "meaning": "讲述、使相互关联", "pos": ""},
            {"word": "prevent", "phonetic": "", "meaning": "阻止", "pos": ""},
            {"word": "baby", "phonetic": "", "meaning": "宝贝", "pos": ""},
            {"word": "pattern", "phonetic": "", "meaning": "模式、图案", "pos": ""},
            {"word": "itself", "phonetic": "", "meaning": "它自己", "pos": ""},
            {"word": "search", "phonetic": "", "meaning": "搜索", "pos": ""},
            {"word": "beyond", "phonetic": "", "meaning": "超越", "pos": ""},
            {"word": "near", "phonetic": "", "meaning": "近的、亲近的", "pos": ""},
            {"word": "regard", "phonetic": "", "meaning": "看待", "pos": ""},
            {"word": "serious", "phonetic": "", "meaning": "严肃认真的、严重的", "pos": ""},
            {"word": "black", "phonetic": "", "meaning": "黑色的", "pos": ""},
            {"word": "climate", "phonetic": "", "meaning": "气候", "pos": ""},
            {"word": "heart", "phonetic": "", "meaning": "心", "pos": ""},
        ]
    },
    "unit_33": {
        "name": "CET4词汇 第33单元",
        "words": [
            {"word": "president", "phonetic": "", "meaning": "总统", "pos": ""},
            {"word": "serve", "phonetic": "", "meaning": "服务", "pos": ""},
            {"word": "traffic", "phonetic": "", "meaning": "交通", "pos": ""},
            {"word": "walk", "phonetic": "", "meaning": "走路", "pos": ""},
            {"word": "award", "phonetic": "", "meaning": "颁奖、奖励", "pos": ""},
            {"word": "determine", "phonetic": "", "meaning": "决定", "pos": ""},
            {"word": "gain", "phonetic": "", "meaning": "获得、增加", "pos": ""},
            {"word": "speech", "phonetic": "", "meaning": "演讲、言语", "pos": ""},
            {"word": "prepare", "phonetic": "", "meaning": "准备", "pos": ""},
            {"word": "except", "phonetic": "", "meaning": "除了……之外", "pos": ""},
            {"word": "publish", "phonetic": "", "meaning": "公布、出版", "pos": ""},
            {"word": "suffer", "phonetic": "", "meaning": "遭受", "pos": ""},
            {"word": "mental", "phonetic": "", "meaning": "精神的", "pos": ""},
            {"word": "positive", "phonetic": "", "meaning": "积极的", "pos": ""},
            {"word": "outside", "phonetic": "", "meaning": "外面的", "pos": ""},
            {"word": "party", "phonetic": "", "meaning": "派对", "pos": ""},
            {"word": "contribute", "phonetic": "", "meaning": "贡献", "pos": ""},
            {"word": "dream", "phonetic": "", "meaning": "梦想", "pos": ""},
            {"word": "drink", "phonetic": "", "meaning": "喝", "pos": ""},
            {"word": "trade", "phonetic": "", "meaning": "交易", "pos": ""},
        ]
    },
    "unit_34": {
        "name": "CET4词汇 第34单元",
        "words": [
            {"word": "himself", "phonetic": "", "meaning": "他自己、他本人", "pos": ""},
            {"word": "therefore", "phonetic": "", "meaning": "因此", "pos": ""},
            {"word": "achieve", "phonetic": "", "meaning": "实现", "pos": ""},
            {"word": "conflict", "phonetic": "", "meaning": "冲突", "pos": ""},
            {"word": "trouble", "phonetic": "", "meaning": "麻烦", "pos": ""},
            {"word": "girl", "phonetic": "", "meaning": "女孩", "pos": ""},
            {"word": "exercise", "phonetic": "", "meaning": "锻炼", "pos": ""},
            {"word": "status", "phonetic": "", "meaning": "状态", "pos": ""},
            {"word": "various", "phonetic": "", "meaning": "各种各样的", "pos": ""},
            {"word": "above", "phonetic": "", "meaning": "在…上面", "pos": ""},
            {"word": "basic", "phonetic": "", "meaning": "基本的、根本的", "pos": ""},
            {"word": "fit", "phonetic": "", "meaning": "健康的、适合", "pos": ""},
            {"word": "occur", "phonetic": "", "meaning": "发生", "pos": ""},
            {"word": "refer", "phonetic": "", "meaning": "提及", "pos": ""},
            {"word": "die", "phonetic": "", "meaning": "死", "pos": ""},
            {"word": "attend", "phonetic": "", "meaning": "出席、照看", "pos": ""},
            {"word": "maintain", "phonetic": "", "meaning": "保持、维持", "pos": ""},
            {"word": "town", "phonetic": "", "meaning": "城镇", "pos": ""},
            {"word": "wait", "phonetic": "", "meaning": "等待", "pos": ""},
            {"word": "alone", "phonetic": "", "meaning": "单独的、仅仅", "pos": ""},
        ]
    },
    "unit_35": {
        "name": "CET4词汇 第35单元",
        "words": [
            {"word": "meeting", "phonetic": "", "meaning": "会议", "pos": ""},
            {"word": "feature", "phonetic": "", "meaning": "特征、容貌、以……为特色", "pos": ""},
            {"word": "tax", "phonetic": "", "meaning": "税、对……征税", "pos": ""},
            {"word": "express", "phonetic": "", "meaning": "表达", "pos": ""},
            {"word": "hundred", "phonetic": "", "meaning": "百、许多", "pos": ""},
            {"word": "shift", "phonetic": "", "meaning": "转移、转换", "pos": ""},
            {"word": "simple", "phonetic": "", "meaning": "简单的", "pos": ""},
            {"word": "thousand", "phonetic": "", "meaning": "一千", "pos": ""},
            {"word": "couple", "phonetic": "", "meaning": "情侣、夫妻", "pos": ""},
            {"word": "image", "phonetic": "", "meaning": "形象、肖像", "pos": ""},
            {"word": "key", "phonetic": "", "meaning": "钥匙、关键", "pos": ""},
            {"word": "theory", "phonetic": "", "meaning": "理论", "pos": ""},
            {"word": "card", "phonetic": "", "meaning": "卡片、纸牌", "pos": ""},
            {"word": "catch", "phonetic": "", "meaning": "抓住", "pos": ""},
            {"word": "realize", "phonetic": "", "meaning": "实现", "pos": ""},
            {"word": "select", "phonetic": "", "meaning": "选择", "pos": ""},
            {"word": "whose", "phonetic": "", "meaning": "谁的", "pos": ""},
            {"word": "cover", "phonetic": "", "meaning": "覆盖", "pos": ""},
            {"word": "earn", "phonetic": "", "meaning": "挣得", "pos": ""},
            {"word": "attract", "phonetic": "", "meaning": "吸引", "pos": ""},
        ]
    },
    "unit_36": {
        "name": "CET4词汇 第36单元",
        "words": [
            {"word": "clean", "phonetic": "", "meaning": "干净的", "pos": ""},
            {"word": "trend", "phonetic": "", "meaning": "趋势", "pos": ""},
            {"word": "desire", "phonetic": "", "meaning": "渴望", "pos": ""},
            {"word": "lie", "phonetic": "", "meaning": "谎话、说谎", "pos": ""},
            {"word": "method", "phonetic": "", "meaning": "方法", "pos": ""},
            {"word": "promise", "phonetic": "", "meaning": "承诺", "pos": ""},
            {"word": "network", "phonetic": "", "meaning": "网络", "pos": ""},
            {"word": "billion", "phonetic": "", "meaning": "十亿、万亿", "pos": ""},
            {"word": "cook", "phonetic": "", "meaning": "烹饪", "pos": ""},
            {"word": "daily", "phonetic": "", "meaning": "破晓、开始", "pos": ""},
            {"word": "detail", "phonetic": "", "meaning": "细节", "pos": ""},
            {"word": "normal", "phonetic": "", "meaning": "正常的", "pos": ""},
            {"word": "post", "phonetic": "", "meaning": "发布、张贴、邮寄", "pos": ""},
            {"word": "reward", "phonetic": "", "meaning": "回报", "pos": ""},
            {"word": "upon", "phonetic": "", "meaning": "在…上面", "pos": ""},
            {"word": "thus", "phonetic": "", "meaning": "因此", "pos": ""},
            {"word": "toward", "phonetic": "", "meaning": "向、朝向", "pos": ""},
            {"word": "device", "phonetic": "", "meaning": "装置、方法", "pos": ""},
            {"word": "discover", "phonetic": "", "meaning": "探索、发现", "pos": ""},
            {"word": "drop", "phonetic": "", "meaning": "掉下", "pos": ""},
        ]
    },
    "unit_37": {
        "name": "CET4词汇 第37单元",
        "words": [
            {"word": "else", "phonetic": "", "meaning": "其他", "pos": ""},
            {"word": "introduce", "phonetic": "", "meaning": "介绍", "pos": ""},
            {"word": "court", "phonetic": "", "meaning": "法庭、球场", "pos": ""},
            {"word": "drug", "phonetic": "", "meaning": "药", "pos": ""},
            {"word": "range", "phonetic": "", "meaning": "范围", "pos": ""},
            {"word": "warm", "phonetic": "", "meaning": "温暖", "pos": ""},
            {"word": "accident", "phonetic": "", "meaning": "事故", "pos": ""},
            {"word": "fashion", "phonetic": "", "meaning": "时尚", "pos": ""},
            {"word": "indicate", "phonetic": "", "meaning": "表明", "pos": ""},
            {"word": "particular", "phonetic": "", "meaning": "特定的", "pos": ""},
            {"word": "attach", "phonetic": "", "meaning": "附上、附加", "pos": ""},
            {"word": "six", "phonetic": "", "meaning": "六", "pos": ""},
            {"word": "slow", "phonetic": "", "meaning": "慢的", "pos": ""},
            {"word": "credit", "phonetic": "", "meaning": "信用", "pos": ""},
            {"word": "finish", "phonetic": "", "meaning": "完成", "pos": ""},
            {"word": "happy", "phonetic": "", "meaning": "快乐的", "pos": ""},
            {"word": "bill", "phonetic": "", "meaning": "账单", "pos": ""},
            {"word": "deep", "phonetic": "", "meaning": "深的", "pos": ""},
            {"word": "fire", "phonetic": "", "meaning": "火、开除", "pos": ""},
            {"word": "belief", "phonetic": "", "meaning": "信仰、相信", "pos": ""},
        ]
    },
    "unit_38": {
        "name": "CET4词汇 第38单元",
        "words": [
            {"word": "moment", "phonetic": "", "meaning": "时刻", "pos": ""},
            {"word": "museum", "phonetic": "", "meaning": "博物馆", "pos": ""},
            {"word": "site", "phonetic": "", "meaning": "景点、站点", "pos": ""},
            {"word": "address", "phonetic": "", "meaning": "演说、地址", "pos": ""},
            {"word": "concept", "phonetic": "", "meaning": "概念", "pos": ""},
            {"word": "crime", "phonetic": "", "meaning": "犯罪", "pos": ""},
            {"word": "damage", "phonetic": "", "meaning": "损害", "pos": ""},
            {"word": "restaurant", "phonetic": "", "meaning": "饭馆", "pos": ""},
            {"word": "size", "phonetic": "", "meaning": "大小", "pos": ""},
            {"word": "federal", "phonetic": "", "meaning": "联邦的", "pos": ""},
            {"word": "progress", "phonetic": "", "meaning": "进步", "pos": ""},
            {"word": "mistake", "phonetic": "", "meaning": "错误", "pos": ""},
            {"word": "robot", "phonetic": "", "meaning": "机器人", "pos": ""},
            {"word": "weather", "phonetic": "", "meaning": "天气", "pos": ""},
            {"word": "charge", "phonetic": "", "meaning": "收费、索价、充电", "pos": ""},
            {"word": "enter", "phonetic": "", "meaning": "进入", "pos": ""},
            {"word": "infer", "phonetic": "", "meaning": "推断", "pos": ""},
            {"word": "medicine", "phonetic": "", "meaning": "医药", "pos": ""},
            {"word": "engage", "phonetic": "", "meaning": "吸引、使参加", "pos": ""},
            {"word": "object", "phonetic": "", "meaning": "目标、物体", "pos": ""},
        ]
    },
    "unit_39": {
        "name": "CET4词汇 第39单元",
        "words": [
            {"word": "race", "phonetic": "", "meaning": "比赛、竞速", "pos": ""},
            {"word": "wide", "phonetic": "", "meaning": "广泛的、宽的", "pos": ""},
            {"word": "hospital", "phonetic": "", "meaning": "医院", "pos": ""},
            {"word": "manage", "phonetic": "", "meaning": "管理、设法做到", "pos": ""},
            {"word": "huge", "phonetic": "", "meaning": "大的", "pos": ""},
            {"word": "official", "phonetic": "", "meaning": "官方的", "pos": ""},
            {"word": "hire", "phonetic": "", "meaning": "雇佣", "pos": ""},
            {"word": "hotel", "phonetic": "", "meaning": "酒店", "pos": ""},
            {"word": "perform", "phonetic": "", "meaning": "演奏、执行", "pos": ""},
            {"word": "treat", "phonetic": "", "meaning": "对待", "pos": ""},
            {"word": "article", "phonetic": "", "meaning": "文章", "pos": ""},
            {"word": "profit", "phonetic": "", "meaning": "利润", "pos": ""},
            {"word": "trip", "phonetic": "", "meaning": "旅行", "pos": ""},
            {"word": "aspect", "phonetic": "", "meaning": "样子、方面", "pos": ""},
            {"word": "due", "phonetic": "", "meaning": "预期的、到期的", "pos": ""},
            {"word": "wear", "phonetic": "", "meaning": "穿着", "pos": ""},
            {"word": "balance", "phonetic": "", "meaning": "平衡", "pos": ""},
            {"word": "define", "phonetic": "", "meaning": "定义", "pos": ""},
            {"word": "enable", "phonetic": "", "meaning": "使能够", "pos": ""},
            {"word": "character", "phonetic": "", "meaning": "性格", "pos": ""},
        ]
    },
    "unit_40": {
        "name": "CET4词汇 第40单元",
        "words": [
            {"word": "crisis", "phonetic": "", "meaning": "危机", "pos": ""},
            {"word": "dollar", "phonetic": "", "meaning": "美元", "pos": ""},
            {"word": "green", "phonetic": "", "meaning": "绿的、未熟的", "pos": ""},
            {"word": "cold", "phonetic": "", "meaning": "冷的", "pos": ""},
            {"word": "contact", "phonetic": "", "meaning": "联系", "pos": ""},
            {"word": "department", "phonetic": "", "meaning": "部门", "pos": ""},
            {"word": "math", "phonetic": "", "meaning": "数学", "pos": ""},
            {"word": "advice", "phonetic": "", "meaning": "建议", "pos": ""},
            {"word": "board", "phonetic": "", "meaning": "板", "pos": ""},
            {"word": "comment", "phonetic": "", "meaning": "评论", "pos": ""},
            {"word": "consequence", "phonetic": "", "meaning": "后果、结果", "pos": ""},
            {"word": "fight", "phonetic": "", "meaning": "打斗", "pos": ""},
            {"word": "meal", "phonetic": "", "meaning": "饭", "pos": ""},
            {"word": "style", "phonetic": "", "meaning": "风格", "pos": ""},
            {"word": "worry", "phonetic": "", "meaning": "担心", "pos": ""},
            {"word": "tool", "phonetic": "", "meaning": "工具", "pos": ""},
            {"word": "waste", "phonetic": "", "meaning": "浪费", "pos": ""},
            {"word": "despite", "phonetic": "", "meaning": "尽管", "pos": ""},
            {"word": "morning", "phonetic": "", "meaning": "早晨", "pos": ""},
            {"word": "predict", "phonetic": "", "meaning": "预测", "pos": ""},
        ]
    },
    "unit_41": {
        "name": "CET4词汇 第41单元",
        "words": [
            {"word": "kill", "phonetic": "", "meaning": "杀", "pos": ""},
            {"word": "stage", "phonetic": "", "meaning": "阶段", "pos": ""},
            {"word": "purchase", "phonetic": "", "meaning": "购买", "pos": ""},
            {"word": "specific", "phonetic": "", "meaning": "具体的、详细的", "pos": ""},
            {"word": "print", "phonetic": "", "meaning": "打印", "pos": ""},
            {"word": "replace", "phonetic": "", "meaning": "替代", "pos": ""},
            {"word": "shape", "phonetic": "", "meaning": "形状", "pos": ""},
            {"word": "significant", "phonetic": "", "meaning": "有意义的、重要的", "pos": ""},
            {"word": "thirty", "phonetic": "", "meaning": "三十", "pos": ""},
            {"word": "yourself", "phonetic": "", "meaning": "你自己、你亲自", "pos": ""},
            {"word": "ground", "phonetic": "", "meaning": "地面、场所", "pos": ""},
            {"word": "screen", "phonetic": "", "meaning": "屏幕", "pos": ""},
            {"word": "lay", "phonetic": "", "meaning": "放置、躺、位于、说谎", "pos": ""},
            {"word": "sea", "phonetic": "", "meaning": "大海", "pos": ""},
            {"word": "struggle", "phonetic": "", "meaning": "斗争、奋斗", "pos": ""},
            {"word": "cross", "phonetic": "", "meaning": "跨过、穿过", "pos": ""},
            {"word": "expand", "phonetic": "", "meaning": "扩大", "pos": ""},
            {"word": "forget", "phonetic": "", "meaning": "忘记", "pos": ""},
            {"word": "multiple", "phonetic": "", "meaning": "多种多样的、倍数", "pos": ""},
            {"word": "wife", "phonetic": "", "meaning": "妻子", "pos": ""},
        ]
    },
    "unit_42": {
        "name": "CET4词汇 第42单元",
        "words": [
            {"word": "conduct", "phonetic": "", "meaning": "实施、开展", "pos": ""},
            {"word": "direct", "phonetic": "", "meaning": "径直的、直接的", "pos": ""},
            {"word": "ensure", "phonetic": "", "meaning": "确保", "pos": ""},
            {"word": "fund", "phonetic": "", "meaning": "资金", "pos": ""},
            {"word": "intellectual", "phonetic": "", "meaning": "知识分子、知识的", "pos": ""},
            {"word": "region", "phonetic": "", "meaning": "地区", "pos": ""},
            {"word": "aim", "phonetic": "", "meaning": "目标", "pos": ""},
            {"word": "husband", "phonetic": "", "meaning": "丈夫", "pos": ""},
            {"word": "legal", "phonetic": "", "meaning": "法律的、合法的", "pos": ""},
            {"word": "link", "phonetic": "", "meaning": "连接", "pos": ""},
            {"word": "reflect", "phonetic": "", "meaning": "反射、反映、思考", "pos": ""},
            {"word": "underline", "phonetic": "", "meaning": "下划线、强调", "pos": ""},
            {"word": "worth", "phonetic": "", "meaning": "值得", "pos": ""},
            {"word": "reveal", "phonetic": "", "meaning": "显露、展现", "pos": ""},
            {"word": "suppose", "phonetic": "", "meaning": "假设", "pos": ""},
            {"word": "advance", "phonetic": "", "meaning": "前进、提高", "pos": ""},
            {"word": "practical", "phonetic": "", "meaning": "实际的", "pos": ""},
            {"word": "smoke", "phonetic": "", "meaning": "烟", "pos": ""},
            {"word": "south", "phonetic": "", "meaning": "南、南方的", "pos": ""},
            {"word": "attack", "phonetic": "", "meaning": "攻击", "pos": ""},
        ]
    },
    "unit_43": {
        "name": "CET4词汇 第43单元",
        "words": [
            {"word": "holiday", "phonetic": "", "meaning": "假日", "pos": ""},
            {"word": "male", "phonetic": "", "meaning": "男性、男性的", "pos": ""},
            {"word": "peer", "phonetic": "", "meaning": "凝视、同伴、贵族", "pos": ""},
            {"word": "film", "phonetic": "", "meaning": "电影", "pos": ""},
            {"word": "police", "phonetic": "", "meaning": "警察", "pos": ""},
            {"word": "push", "phonetic": "", "meaning": "推", "pos": ""},
            {"word": "twenty", "phonetic": "", "meaning": "二十", "pos": ""},
            {"word": "associate", "phonetic": "", "meaning": "联系、结交", "pos": ""},
            {"word": "attempt", "phonetic": "", "meaning": "试图、企图", "pos": ""},
            {"word": "prefer", "phonetic": "", "meaning": "偏好", "pos": ""},
            {"word": "review", "phonetic": "", "meaning": "复习、回顾、评论", "pos": ""},
            {"word": "wealth", "phonetic": "", "meaning": "财富", "pos": ""},
            {"word": "title", "phonetic": "", "meaning": "标题", "pos": ""},
            {"word": "trust", "phonetic": "", "meaning": "信任", "pos": ""},
            {"word": "box", "phonetic": "", "meaning": "盒子", "pos": ""},
            {"word": "cry", "phonetic": "", "meaning": "尝试", "pos": ""},
            {"word": "ill", "phonetic": "", "meaning": "有病的、坏的", "pos": ""},
            {"word": "china", "phonetic": "", "meaning": "瓷器", "pos": ""},
            {"word": "derive", "phonetic": "", "meaning": "取得", "pos": ""},
            {"word": "hardly", "phonetic": "", "meaning": "几乎不、仅仅", "pos": ""},
        ]
    },
    "unit_44": {
        "name": "CET4词汇 第44单元",
        "words": [
            {"word": "textbook", "phonetic": "", "meaning": "课本", "pos": ""},
            {"word": "total", "phonetic": "", "meaning": "总共的", "pos": ""},
            {"word": "track", "phonetic": "", "meaning": "追踪、足迹、痕迹", "pos": ""},
            {"word": "warn", "phonetic": "", "meaning": "警告", "pos": ""},
            {"word": "bird", "phonetic": "", "meaning": "鸟", "pos": ""},
            {"word": "extra", "phonetic": "", "meaning": "额外的", "pos": ""},
            {"word": "heavy", "phonetic": "", "meaning": "重的", "pos": ""},
            {"word": "ignore", "phonetic": "", "meaning": "忽视", "pos": ""},
            {"word": "survive", "phonetic": "", "meaning": "幸存", "pos": ""},
            {"word": "fuel", "phonetic": "", "meaning": "燃料", "pos": ""},
            {"word": "magazine", "phonetic": "", "meaning": "杂志", "pos": ""},
            {"word": "summer", "phonetic": "", "meaning": "夏天、夏季的", "pos": ""},
            {"word": "complex", "phonetic": "", "meaning": "复杂的", "pos": ""},
            {"word": "danger", "phonetic": "", "meaning": "危险", "pos": ""},
            {"word": "library", "phonetic": "", "meaning": "图书馆", "pos": ""},
            {"word": "piece", "phonetic": "", "meaning": "（一）件、碎片", "pos": ""},
            {"word": "throughout", "phonetic": "", "meaning": "遍及、到处", "pos": ""},
            {"word": "institution", "phonetic": "", "meaning": "机构", "pos": ""},
            {"word": "mention", "phonetic": "", "meaning": "提及", "pos": ""},
            {"word": "appeal", "phonetic": "", "meaning": "呼吁、吸引", "pos": ""},
        ]
    },
    "unit_45": {
        "name": "CET4词汇 第45单元",
        "words": [
            {"word": "background", "phonetic": "", "meaning": "背景", "pos": ""},
            {"word": "colleague", "phonetic": "", "meaning": "同事", "pos": ""},
            {"word": "exact", "phonetic": "", "meaning": "确切的、特定的", "pos": ""},
            {"word": "intend", "phonetic": "", "meaning": "想要（做某事）", "pos": ""},
            {"word": "paint", "phonetic": "", "meaning": "绘画", "pos": ""},
            {"word": "recognize", "phonetic": "", "meaning": "认出、承认", "pos": ""},
            {"word": "strategy", "phonetic": "", "meaning": "策略", "pos": ""},
            {"word": "arrive", "phonetic": "", "meaning": "到、达到", "pos": ""},
            {"word": "authority", "phonetic": "", "meaning": "权力、权威人士", "pos": ""},
            {"word": "cheap", "phonetic": "", "meaning": "便宜的、不值钱的", "pos": ""},
            {"word": "factory", "phonetic": "", "meaning": "工厂", "pos": ""},
            {"word": "grant", "phonetic": "", "meaning": "同意、授予", "pos": ""},
            {"word": "journal", "phonetic": "", "meaning": "日记", "pos": ""},
            {"word": "ready", "phonetic": "", "meaning": "准备好的", "pos": ""},
            {"word": "tree", "phonetic": "", "meaning": "树、爬上树", "pos": ""},
            {"word": "expense", "phonetic": "", "meaning": "花费", "pos": ""},
            {"word": "patent", "phonetic": "", "meaning": "专利、专利的", "pos": ""},
            {"word": "spread", "phonetic": "", "meaning": "传播", "pos": ""},
            {"word": "chief", "phonetic": "", "meaning": "首领、主要的", "pos": ""},
            {"word": "establish", "phonetic": "", "meaning": "建立、查实", "pos": ""},
        ]
    },
    "unit_46": {
        "name": "CET4词汇 第46单元",
        "words": [
            {"word": "foot", "phonetic": "", "meaning": "脚、走", "pos": ""},
            {"word": "indeed", "phonetic": "", "meaning": "确实", "pos": ""},
            {"word": "nor", "phonetic": "", "meaning": "也不", "pos": ""},
            {"word": "observe", "phonetic": "", "meaning": "观察", "pos": ""},
            {"word": "safe", "phonetic": "", "meaning": "安全的", "pos": ""},
            {"word": "compete", "phonetic": "", "meaning": "竞争", "pos": ""},
            {"word": "debate", "phonetic": "", "meaning": "讨论", "pos": ""},
            {"word": "educate", "phonetic": "", "meaning": "教育", "pos": ""},
            {"word": "staff", "phonetic": "", "meaning": "员工", "pos": ""},
            {"word": "wish", "phonetic": "", "meaning": "希望", "pos": ""},
            {"word": "adapt", "phonetic": "", "meaning": "改编、适应", "pos": ""},
            {"word": "boss", "phonetic": "", "meaning": "老板", "pos": ""},
            {"word": "fix", "phonetic": "", "meaning": "固定、修理", "pos": ""},
            {"word": "unless", "phonetic": "", "meaning": "除非", "pos": ""},
            {"word": "scale", "phonetic": "", "meaning": "刻度、天平", "pos": ""},
            {"word": "emotion", "phonetic": "", "meaning": "情感", "pos": ""},
            {"word": "threat", "phonetic": "", "meaning": "威胁", "pos": ""},
            {"word": "union", "phonetic": "", "meaning": "一致、联合", "pos": ""},
            {"word": "adopt", "phonetic": "", "meaning": "采用、收养", "pos": ""},
            {"word": "capacity", "phonetic": "", "meaning": "容量、能力、生产力", "pos": ""},
        ]
    },
    "unit_47": {
        "name": "CET4词汇 第47单元",
        "words": [
            {"word": "lesson", "phonetic": "", "meaning": "课、教训", "pos": ""},
            {"word": "mile", "phonetic": "", "meaning": "英里", "pos": ""},
            {"word": "movie", "phonetic": "", "meaning": "电影", "pos": ""},
            {"word": "obvious", "phonetic": "", "meaning": "明显的", "pos": ""},
            {"word": "passenger", "phonetic": "", "meaning": "乘客", "pos": ""},
            {"word": "regular", "phonetic": "", "meaning": "定期的、常规的", "pos": ""},
            {"word": "represent", "phonetic": "", "meaning": "代表", "pos": ""},
            {"word": "score", "phonetic": "", "meaning": "分数", "pos": ""},
            {"word": "voice", "phonetic": "", "meaning": "声音", "pos": ""},
            {"word": "discuss", "phonetic": "", "meaning": "讨论", "pos": ""},
            {"word": "join", "phonetic": "", "meaning": "参加", "pos": ""},
            {"word": "operate", "phonetic": "", "meaning": "运转、动手术", "pos": ""},
            {"word": "ancient", "phonetic": "", "meaning": "古老的", "pos": ""},
            {"word": "date", "phonetic": "", "meaning": "日期", "pos": ""},
            {"word": "extend", "phonetic": "", "meaning": "延伸、延展", "pos": ""},
            {"word": "match", "phonetic": "", "meaning": "比赛、匹配", "pos": ""},
            {"word": "audience", "phonetic": "", "meaning": "观众", "pos": ""},
            {"word": "forest", "phonetic": "", "meaning": "森林", "pos": ""},
            {"word": "gas", "phonetic": "", "meaning": "气体、天然气", "pos": ""},
            {"word": "separate", "phonetic": "", "meaning": "分开", "pos": ""},
        ]
    },
    "unit_48": {
        "name": "CET4词汇 第48单元",
        "words": [
            {"word": "station", "phonetic": "", "meaning": "车站", "pos": ""},
            {"word": "unique", "phonetic": "", "meaning": "独特的", "pos": ""},
            {"word": "wonder", "phonetic": "", "meaning": "好奇、奇观", "pos": ""},
            {"word": "carbon", "phonetic": "", "meaning": "碳、复写纸", "pos": ""},
            {"word": "conclude", "phonetic": "", "meaning": "总结", "pos": ""},
            {"word": "employ", "phonetic": "", "meaning": "雇佣、采用", "pos": ""},
            {"word": "female", "phonetic": "", "meaning": "女性、雌性", "pos": ""},
            {"word": "moral", "phonetic": "", "meaning": "道德的", "pos": ""},
            {"word": "temperature", "phonetic": "", "meaning": "温度", "pos": ""},
            {"word": "wall", "phonetic": "", "meaning": "墙壁", "pos": ""},
            {"word": "acquire", "phonetic": "", "meaning": "获得", "pos": ""},
            {"word": "aware", "phonetic": "", "meaning": "意识的", "pos": ""},
            {"word": "campus", "phonetic": "", "meaning": "校园", "pos": ""},
            {"word": "classroom", "phonetic": "", "meaning": "教室", "pos": ""},
            {"word": "consume", "phonetic": "", "meaning": "消耗、耗尽", "pos": ""},
            {"word": "mail", "phonetic": "", "meaning": "邮件", "pos": ""},
            {"word": "principle", "phonetic": "", "meaning": "原则", "pos": ""},
            {"word": "aid", "phonetic": "", "meaning": "援助", "pos": ""},
            {"word": "pain", "phonetic": "", "meaning": "痛苦", "pos": ""},
            {"word": "cell", "phonetic": "", "meaning": "细胞", "pos": ""},
        ]
    },
    "unit_49": {
        "name": "CET4词汇 第49单元",
        "words": [
            {"word": "confidence", "phonetic": "", "meaning": "信任", "pos": ""},
            {"word": "doubt", "phonetic": "", "meaning": "怀疑", "pos": ""},
            {"word": "ice", "phonetic": "", "meaning": "冰、使结冰", "pos": ""},
            {"word": "imagine", "phonetic": "", "meaning": "想象", "pos": ""},
            {"word": "taste", "phonetic": "", "meaning": "口味", "pos": ""},
            {"word": "dinner", "phonetic": "", "meaning": "正餐", "pos": ""},
            {"word": "equal", "phonetic": "", "meaning": "平等的", "pos": ""},
            {"word": "senior", "phonetic": "", "meaning": "年长的、资格老的", "pos": ""},
            {"word": "examine", "phonetic": "", "meaning": "检查", "pos": ""},
            {"word": "overall", "phonetic": "", "meaning": "全面的、总体上", "pos": ""},
            {"word": "pick", "phonetic": "", "meaning": "挑", "pos": ""},
            {"word": "strike", "phonetic": "", "meaning": "击打", "pos": ""},
            {"word": "succeed", "phonetic": "", "meaning": "成功、接替", "pos": ""},
            {"word": "cancer", "phonetic": "", "meaning": "癌症", "pos": ""},
            {"word": "divide", "phonetic": "", "meaning": "划分", "pos": ""},
            {"word": "floor", "phonetic": "", "meaning": "地面", "pos": ""},
            {"word": "former", "phonetic": "", "meaning": "以前的、前者", "pos": ""},
            {"word": "front", "phonetic": "", "meaning": "前面的", "pos": ""},
            {"word": "harm", "phonetic": "", "meaning": "伤害", "pos": ""},
            {"word": "instance", "phonetic": "", "meaning": "例子", "pos": ""},
        ]
    },
    "unit_50": {
        "name": "CET4词汇 第50单元",
        "words": [
            {"word": "judge", "phonetic": "", "meaning": "判断", "pos": ""},
            {"word": "partner", "phonetic": "", "meaning": "伙伴", "pos": ""},
            {"word": "release", "phonetic": "", "meaning": "释放、解除", "pos": ""},
            {"word": "rely", "phonetic": "", "meaning": "依靠", "pos": ""},
            {"word": "clock", "phonetic": "", "meaning": "时钟、计时", "pos": ""},
            {"word": "hunt", "phonetic": "", "meaning": "打猎", "pos": ""},
            {"word": "imply", "phonetic": "", "meaning": "意指", "pos": ""},
            {"word": "radio", "phonetic": "", "meaning": "收音机", "pos": ""},
            {"word": "remove", "phonetic": "", "meaning": "移除", "pos": ""},
            {"word": "tradition", "phonetic": "", "meaning": "传统", "pos": ""},
            {"word": "vocabulary", "phonetic": "", "meaning": "词汇", "pos": ""},
            {"word": "assume", "phonetic": "", "meaning": "假设、揣测", "pos": ""},
            {"word": "campaign", "phonetic": "", "meaning": "运动、战役", "pos": ""},
            {"word": "collect", "phonetic": "", "meaning": "收集", "pos": ""},
            {"word": "invite", "phonetic": "", "meaning": "邀请", "pos": ""},
            {"word": "native", "phonetic": "", "meaning": "本地的、天生的", "pos": ""},
            {"word": "gender", "phonetic": "", "meaning": "性别", "pos": ""},
            {"word": "reform", "phonetic": "", "meaning": "改革", "pos": ""},
            {"word": "urban", "phonetic": "", "meaning": "城市的", "pos": ""},
            {"word": "color", "phonetic": "", "meaning": "颜色", "pos": ""},
        ]
    },
    "unit_51": {
        "name": "CET4词汇 第51单元",
        "words": [
            {"word": "connect", "phonetic": "", "meaning": "连接", "pos": ""},
            {"word": "debt", "phonetic": "", "meaning": "债务", "pos": ""},
            {"word": "diet", "phonetic": "", "meaning": "饮食", "pos": ""},
            {"word": "door", "phonetic": "", "meaning": "门", "pos": ""},
            {"word": "emerge", "phonetic": "", "meaning": "出现", "pos": ""},
            {"word": "enhance", "phonetic": "", "meaning": "提高", "pos": ""},
            {"word": "forward", "phonetic": "", "meaning": "前进的", "pos": ""},
            {"word": "handle", "phonetic": "", "meaning": "处理", "pos": ""},
            {"word": "round", "phonetic": "", "meaning": "圆的", "pos": ""},
            {"word": "sort", "phonetic": "", "meaning": "种类、排序", "pos": ""},
            {"word": "afford", "phonetic": "", "meaning": "承担得起", "pos": ""},
            {"word": "apple", "phonetic": "", "meaning": "苹果", "pos": ""},
            {"word": "eventually", "phonetic": "", "meaning": "最终", "pos": ""},
            {"word": "hot", "phonetic": "", "meaning": "热的", "pos": ""},
            {"word": "manufacture", "phonetic": "", "meaning": "制造、产品", "pos": ""},
            {"word": "north", "phonetic": "", "meaning": "北、北方的", "pos": ""},
            {"word": "ocean", "phonetic": "", "meaning": "海洋", "pos": ""},
            {"word": "sugar", "phonetic": "", "meaning": "糖", "pos": ""},
            {"word": "advocate", "phonetic": "", "meaning": "主张、倡议", "pos": ""},
            {"word": "contrast", "phonetic": "", "meaning": "形成对比", "pos": ""},
        ]
    },
    "unit_52": {
        "name": "CET4词汇 第52单元",
        "words": [
            {"word": "ideal", "phonetic": "", "meaning": "理想的、空想的", "pos": ""},
            {"word": "inside", "phonetic": "", "meaning": "在里面", "pos": ""},
            {"word": "mass", "phonetic": "", "meaning": "大量", "pos": ""},
            {"word": "noise", "phonetic": "", "meaning": "噪音", "pos": ""},
            {"word": "vehicle", "phonetic": "", "meaning": "交通工具", "pos": ""},
            {"word": "west", "phonetic": "", "meaning": "西、向西", "pos": ""},
            {"word": "double", "phonetic": "", "meaning": "双的、使加倍", "pos": ""},
            {"word": "gift", "phonetic": "", "meaning": "礼物", "pos": ""},
            {"word": "novel", "phonetic": "", "meaning": "新颖的、长篇小说", "pos": ""},
            {"word": "organize", "phonetic": "", "meaning": "组织", "pos": ""},
            {"word": "page", "phonetic": "", "meaning": "页码", "pos": ""},
            {"word": "park", "phonetic": "", "meaning": "停车、公园", "pos": ""},
            {"word": "seven", "phonetic": "", "meaning": "七", "pos": ""},
            {"word": "cent", "phonetic": "", "meaning": "分", "pos": ""},
            {"word": "citizen", "phonetic": "", "meaning": "公民", "pos": ""},
            {"word": "code", "phonetic": "", "meaning": "代码、法典", "pos": ""},
            {"word": "display", "phonetic": "", "meaning": "陈列、显示", "pos": ""},
            {"word": "outline", "phonetic": "", "meaning": "轮廓、提纲", "pos": ""},
            {"word": "son", "phonetic": "", "meaning": "儿子、孩子", "pos": ""},
            {"word": "budget", "phonetic": "", "meaning": "预算、做预算", "pos": ""},
        ]
    },
    "unit_53": {
        "name": "CET4词汇 第53单元",
        "words": [
            {"word": "smart", "phonetic": "", "meaning": "聪明的", "pos": ""},
            {"word": "sun", "phonetic": "", "meaning": "太阳", "pos": ""},
            {"word": "whom", "phonetic": "", "meaning": "谁、哪个人", "pos": ""},
            {"word": "agriculture", "phonetic": "", "meaning": "农业", "pos": ""},
            {"word": "brand", "phonetic": "", "meaning": "品牌", "pos": ""},
            {"word": "crop", "phonetic": "", "meaning": "作物、收成", "pos": ""},
            {"word": "estimate", "phonetic": "", "meaning": "估计", "pos": ""},
            {"word": "explore", "phonetic": "", "meaning": "探索", "pos": ""},
            {"word": "launch", "phonetic": "", "meaning": "发射、使船下水", "pos": ""},
            {"word": "manner", "phonetic": "", "meaning": "礼貌、礼仪、方式", "pos": ""},
            {"word": "scan", "phonetic": "", "meaning": "扫描", "pos": ""},
            {"word": "being", "phonetic": "", "meaning": "生物、生存", "pos": ""},
            {"word": "count", "phonetic": "", "meaning": "数数", "pos": ""},
            {"word": "distance", "phonetic": "", "meaning": "距离", "pos": ""},
            {"word": "expose", "phonetic": "", "meaning": "暴露", "pos": ""},
            {"word": "hit", "phonetic": "", "meaning": "打", "pos": ""},
            {"word": "nurse", "phonetic": "", "meaning": "护士、护理", "pos": ""},
            {"word": "ticket", "phonetic": "", "meaning": "票", "pos": ""},
            {"word": "truth", "phonetic": "", "meaning": "真相", "pos": ""},
            {"word": "ban", "phonetic": "", "meaning": "禁止", "pos": ""},
        ]
    },
    "unit_54": {
        "name": "CET4词汇 第54单元",
        "words": [
            {"word": "bit", "phonetic": "", "meaning": "一点", "pos": ""},
            {"word": "combine", "phonetic": "", "meaning": "结合", "pos": ""},
            {"word": "impossible", "phonetic": "", "meaning": "不可能的", "pos": ""},
            {"word": "nuclear", "phonetic": "", "meaning": "原子的", "pos": ""},
            {"word": "basis", "phonetic": "", "meaning": "基础", "pos": ""},
            {"word": "boost", "phonetic": "", "meaning": "往上推、增加", "pos": ""},
            {"word": "dog", "phonetic": "", "meaning": "狗", "pos": ""},
            {"word": "rain", "phonetic": "", "meaning": "雨", "pos": ""},
            {"word": "reserve", "phonetic": "", "meaning": "预留", "pos": ""},
            {"word": "communicate", "phonetic": "", "meaning": "传达、交流", "pos": ""},
            {"word": "disaster", "phonetic": "", "meaning": "灾难", "pos": ""},
            {"word": "discipline", "phonetic": "", "meaning": "纪律", "pos": ""},
            {"word": "previous", "phonetic": "", "meaning": "先前的", "pos": ""},
            {"word": "primary", "phonetic": "", "meaning": "初级的、最初的", "pos": ""},
            {"word": "prize", "phonetic": "", "meaning": "奖", "pos": ""},
            {"word": "revolution", "phonetic": "", "meaning": "革命、旋转", "pos": ""},
            {"word": "seat", "phonetic": "", "meaning": "座位", "pos": ""},
            {"word": "candidate", "phonetic": "", "meaning": "候选人", "pos": ""},
            {"word": "eight", "phonetic": "", "meaning": "八", "pos": ""},
            {"word": "fly", "phonetic": "", "meaning": "飞", "pos": ""},
        ]
    },
    "unit_55": {
        "name": "CET4词汇 第55单元",
        "words": [
            {"word": "heat", "phonetic": "", "meaning": "热", "pos": ""},
            {"word": "identity", "phonetic": "", "meaning": "身份", "pos": ""},
            {"word": "quick", "phonetic": "", "meaning": "迅速的", "pos": ""},
            {"word": "repair", "phonetic": "", "meaning": "修理、补救", "pos": ""},
            {"word": "stock", "phonetic": "", "meaning": "股票、库存", "pos": ""},
            {"word": "tear", "phonetic": "", "meaning": "眼泪、撕碎", "pos": ""},
            {"word": "conference", "phonetic": "", "meaning": "会议", "pos": ""},
            {"word": "press", "phonetic": "", "meaning": "报刊、新闻界", "pos": ""},
            {"word": "web", "phonetic": "", "meaning": "网", "pos": ""},
            {"word": "clothe", "phonetic": "", "meaning": "给穿衣", "pos": ""},
            {"word": "facility", "phonetic": "", "meaning": "灵巧、天资", "pos": ""},
            {"word": "generate", "phonetic": "", "meaning": "产生、引起", "pos": ""},
            {"word": "recession", "phonetic": "", "meaning": "经济衰退、退后", "pos": ""},
            {"word": "signal", "phonetic": "", "meaning": "信号", "pos": ""},
            {"word": "spot", "phonetic": "", "meaning": "发现、污点", "pos": ""},
            {"word": "burn", "phonetic": "", "meaning": "燃烧", "pos": ""},
            {"word": "bus", "phonetic": "", "meaning": "公车", "pos": ""},
            {"word": "decrease", "phonetic": "", "meaning": "减少", "pos": ""},
            {"word": "fat", "phonetic": "", "meaning": "脂肪", "pos": ""},
            {"word": "gold", "phonetic": "", "meaning": "金子", "pos": ""},
        ]
    },
    "unit_56": {
        "name": "CET4词汇 第56单元",
        "words": [
            {"word": "ourselves", "phonetic": "", "meaning": "我们自己、我们亲自", "pos": ""},
            {"word": "refuse", "phonetic": "", "meaning": "拒绝", "pos": ""},
            {"word": "sample", "phonetic": "", "meaning": "样品", "pos": ""},
            {"word": "table", "phonetic": "", "meaning": "桌子、表格", "pos": ""},
            {"word": "ahead", "phonetic": "", "meaning": "在…前面", "pos": ""},
            {"word": "airport", "phonetic": "", "meaning": "机场", "pos": ""},
            {"word": "domestic", "phonetic": "", "meaning": "家庭的", "pos": ""},
            {"word": "guest", "phonetic": "", "meaning": "客人", "pos": ""},
            {"word": "obtain", "phonetic": "", "meaning": "获得", "pos": ""},
            {"word": "fair", "phonetic": "", "meaning": "公平的", "pos": ""},
            {"word": "familiar", "phonetic": "", "meaning": "熟悉的", "pos": ""},
            {"word": "formal", "phonetic": "", "meaning": "正式的、形式的", "pos": ""},
            {"word": "marry", "phonetic": "", "meaning": "结婚", "pos": ""},
            {"word": "perfect", "phonetic": "", "meaning": "完美的", "pos": ""},
            {"word": "planet", "phonetic": "", "meaning": "行星", "pos": ""},
            {"word": "strange", "phonetic": "", "meaning": "奇怪的", "pos": ""},
            {"word": "deliver", "phonetic": "", "meaning": "传递、传输", "pos": ""},
            {"word": "series", "phonetic": "", "meaning": "系列", "pos": ""},
            {"word": "vast", "phonetic": "", "meaning": "巨大的、大量的", "pos": ""},
            {"word": "altogether", "phonetic": "", "meaning": "总共、完全地", "pos": ""},
        ]
    },
    "unit_57": {
        "name": "CET4词汇 第57单元",
        "words": [
            {"word": "blood", "phonetic": "", "meaning": "血", "pos": ""},
            {"word": "calorie", "phonetic": "", "meaning": "卡路里", "pos": ""},
            {"word": "herself", "phonetic": "", "meaning": "她自己、她亲自", "pos": ""},
            {"word": "inform", "phonetic": "", "meaning": "通知、告诉", "pos": ""},
            {"word": "revenue", "phonetic": "", "meaning": "财政收入", "pos": ""},
            {"word": "sector", "phonetic": "", "meaning": "部分、扇区", "pos": ""},
            {"word": "thank", "phonetic": "", "meaning": "感谢", "pos": ""},
            {"word": "twice", "phonetic": "", "meaning": "两次", "pos": ""},
            {"word": "welfare", "phonetic": "", "meaning": "福利", "pos": ""},
            {"word": "cite", "phonetic": "", "meaning": "引用", "pos": ""},
            {"word": "guide", "phonetic": "", "meaning": "指引、指导", "pos": ""},
            {"word": "household", "phonetic": "", "meaning": "户、家庭的", "pos": ""},
            {"word": "intelligent", "phonetic": "", "meaning": "聪明的", "pos": ""},
            {"word": "pupil", "phonetic": "", "meaning": "学生、瞳孔", "pos": ""},
            {"word": "exchange", "phonetic": "", "meaning": "交换", "pos": ""},
            {"word": "ship", "phonetic": "", "meaning": "船舶、装运", "pos": ""},
            {"word": "statistic", "phonetic": "", "meaning": "统计数值", "pos": ""},
            {"word": "admit", "phonetic": "", "meaning": "承认", "pos": ""},
            {"word": "commit", "phonetic": "", "meaning": "把…交托给、犯（罪）", "pos": ""},
            {"word": "complain", "phonetic": "", "meaning": "抱怨", "pos": ""},
        ]
    },
    "unit_58": {
        "name": "CET4词汇 第58单元",
        "words": [
            {"word": "context", "phonetic": "", "meaning": "上下文、环境", "pos": ""},
            {"word": "differ", "phonetic": "", "meaning": "与……不同", "pos": ""},
            {"word": "fine", "phonetic": "", "meaning": "很好", "pos": ""},
            {"word": "label", "phonetic": "", "meaning": "标签、加标签于", "pos": ""},
            {"word": "objective", "phonetic": "", "meaning": "客观的、目的", "pos": ""},
            {"word": "brother", "phonetic": "", "meaning": "兄弟", "pos": ""},
            {"word": "church", "phonetic": "", "meaning": "教堂", "pos": ""},
            {"word": "rent", "phonetic": "", "meaning": "租", "pos": ""},
            {"word": "soil", "phonetic": "", "meaning": "泥土、国土", "pos": ""},
            {"word": "video", "phonetic": "", "meaning": "录像", "pos": ""},
            {"word": "yield", "phonetic": "", "meaning": "放弃、屈服、收益", "pos": ""},
            {"word": "active", "phonetic": "", "meaning": "活跃的、积极的", "pos": ""},
            {"word": "capital", "phonetic": "", "meaning": "首都、大写字母", "pos": ""},
            {"word": "circumstance", "phonetic": "", "meaning": "情况", "pos": ""},
            {"word": "illustrate", "phonetic": "", "meaning": "说明、加插图", "pos": ""},
            {"word": "pretty", "phonetic": "", "meaning": "漂亮的", "pos": ""},
            {"word": "schedule", "phonetic": "", "meaning": "日程", "pos": ""},
            {"word": "target", "phonetic": "", "meaning": "目标", "pos": ""},
            {"word": "window", "phonetic": "", "meaning": "窗户", "pos": ""},
            {"word": "alter", "phonetic": "", "meaning": "改变", "pos": ""},
        ]
    },
    "unit_59": {
        "name": "CET4词汇 第59单元",
        "words": [
            {"word": "gather", "phonetic": "", "meaning": "聚集、搜集", "pos": ""},
            {"word": "sensitive", "phonetic": "", "meaning": "敏感的、易受伤害的", "pos": ""},
            {"word": "artificial", "phonetic": "", "meaning": "人造的", "pos": ""},
            {"word": "busy", "phonetic": "", "meaning": "忙碌的", "pos": ""},
            {"word": "eliminate", "phonetic": "", "meaning": "排除、淘汰", "pos": ""},
            {"word": "engineer", "phonetic": "", "meaning": "工程师", "pos": ""},
            {"word": "neither", "phonetic": "", "meaning": "两个都不", "pos": ""},
            {"word": "property", "phonetic": "", "meaning": "财产、性质、特性", "pos": ""},
            {"word": "rank", "phonetic": "", "meaning": "排列、等级", "pos": ""},
            {"word": "teenager", "phonetic": "", "meaning": "青少年", "pos": ""},
            {"word": "touch", "phonetic": "", "meaning": "触摸、感动", "pos": ""},
            {"word": "circle", "phonetic": "", "meaning": "圆", "pos": ""},
            {"word": "cure", "phonetic": "", "meaning": "治愈", "pos": ""},
            {"word": "secretary", "phonetic": "", "meaning": "秘书", "pos": ""},
            {"word": "switch", "phonetic": "", "meaning": "开关、改变", "pos": ""},
            {"word": "welcome", "phonetic": "", "meaning": "欢迎", "pos": ""},
            {"word": "cope", "phonetic": "", "meaning": "处理、应对", "pos": ""},
            {"word": "crowd", "phonetic": "", "meaning": "聚集、挤满", "pos": ""},
            {"word": "fresh", "phonetic": "", "meaning": "新鲜的", "pos": ""},
            {"word": "interpret", "phonetic": "", "meaning": "口译、解释", "pos": ""},
        ]
    },
    "unit_60": {
        "name": "CET4词汇 第60单元",
        "words": [
            {"word": "lawyer", "phonetic": "", "meaning": "律师", "pos": ""},
            {"word": "military", "phonetic": "", "meaning": "军事的、军队", "pos": ""},
            {"word": "nowadays", "phonetic": "", "meaning": "现今", "pos": ""},
            {"word": "propose", "phonetic": "", "meaning": "提议、提名", "pos": ""},
            {"word": "pull", "phonetic": "", "meaning": "拉", "pos": ""},
            {"word": "relative", "phonetic": "", "meaning": "亲戚、比较的", "pos": ""},
            {"word": "sex", "phonetic": "", "meaning": "性", "pos": ""},
            {"word": "abroad", "phonetic": "", "meaning": "到国外、广为流传", "pos": ""},
            {"word": "afternoon", "phonetic": "", "meaning": "下午", "pos": ""},
            {"word": "birth", "phonetic": "", "meaning": "出生", "pos": ""},
            {"word": "feed", "phonetic": "", "meaning": "喂食", "pos": ""},
            {"word": "fiction", "phonetic": "", "meaning": "虚构、小说", "pos": ""},
            {"word": "fish", "phonetic": "", "meaning": "鱼", "pos": ""},
            {"word": "plane", "phonetic": "", "meaning": "飞机", "pos": ""},
            {"word": "prospect", "phonetic": "", "meaning": "景色、前景", "pos": ""},
            {"word": "psychology", "phonetic": "", "meaning": "心理学", "pos": ""},
            {"word": "routine", "phonetic": "", "meaning": "常规、惯例", "pos": ""},
            {"word": "shoe", "phonetic": "", "meaning": "鞋子", "pos": ""},
            {"word": "talent", "phonetic": "", "meaning": "才华、人才", "pos": ""},
            {"word": "technical", "phonetic": "", "meaning": "技术的", "pos": ""},
        ]
    },
    "unit_61": {
        "name": "CET4词汇 第61单元",
        "words": [
            {"word": "consist", "phonetic": "", "meaning": "组成、在于", "pos": ""},
            {"word": "flow", "phonetic": "", "meaning": "流动", "pos": ""},
            {"word": "hurt", "phonetic": "", "meaning": "伤害", "pos": ""},
            {"word": "master", "phonetic": "", "meaning": "主人、精通、掌握", "pos": ""},
            {"word": "preserve", "phonetic": "", "meaning": "保护、保存", "pos": ""},
            {"word": "technique", "phonetic": "", "meaning": "技术", "pos": ""},
            {"word": "wake", "phonetic": "", "meaning": "醒来", "pos": ""},
            {"word": "block", "phonetic": "", "meaning": "阻挡、块", "pos": ""},
            {"word": "blue", "phonetic": "", "meaning": "蓝色的", "pos": ""},
            {"word": "broad", "phonetic": "", "meaning": "宽的", "pos": ""},
            {"word": "convince", "phonetic": "", "meaning": "使人信服", "pos": ""},
            {"word": "delay", "phonetic": "", "meaning": "推迟", "pos": ""},
            {"word": "destroy", "phonetic": "", "meaning": "摧毁", "pos": ""},
            {"word": "exhibit", "phonetic": "", "meaning": "展览", "pos": ""},
            {"word": "meat", "phonetic": "", "meaning": "肉类", "pos": ""},
            {"word": "smile", "phonetic": "", "meaning": "笑", "pos": ""},
            {"word": "sufficient", "phonetic": "", "meaning": "足够的", "pos": ""},
            {"word": "vision", "phonetic": "", "meaning": "视力、想象", "pos": ""},
            {"word": "wage", "phonetic": "", "meaning": "工资、发动", "pos": ""},
            {"word": "actual", "phonetic": "", "meaning": "实在的", "pos": ""},
        ]
    },
    "unit_62": {
        "name": "CET4词汇 第62单元",
        "words": [
            {"word": "blame", "phonetic": "", "meaning": "责备", "pos": ""},
            {"word": "grammar", "phonetic": "", "meaning": "语法", "pos": ""},
            {"word": "invest", "phonetic": "", "meaning": "投资", "pos": ""},
            {"word": "peace", "phonetic": "", "meaning": "和平", "pos": ""},
            {"word": "proper", "phonetic": "", "meaning": "适合的、固有的", "pos": ""},
            {"word": "star", "phonetic": "", "meaning": "星、恒星", "pos": ""},
            {"word": "tough", "phonetic": "", "meaning": "艰难的", "pos": ""},
            {"word": "club", "phonetic": "", "meaning": "俱乐部", "pos": ""},
            {"word": "efficient", "phonetic": "", "meaning": "有效的、能胜任的", "pos": ""},
            {"word": "emphasis", "phonetic": "", "meaning": "强调", "pos": ""},
            {"word": "escape", "phonetic": "", "meaning": "逃跑", "pos": ""},
            {"word": "import", "phonetic": "", "meaning": "进口、进口商品", "pos": ""},
            {"word": "otherwise", "phonetic": "", "meaning": "否则", "pos": ""},
            {"word": "red", "phonetic": "", "meaning": "红色的", "pos": ""},
            {"word": "advise", "phonetic": "", "meaning": "劝告、建议", "pos": ""},
            {"word": "agent", "phonetic": "", "meaning": "代理", "pos": ""},
            {"word": "copy", "phonetic": "", "meaning": "复制", "pos": ""},
            {"word": "dominate", "phonetic": "", "meaning": "支配、占优势", "pos": ""},
            {"word": "element", "phonetic": "", "meaning": "元素、要素", "pos": ""},
            {"word": "impose", "phonetic": "", "meaning": "把……强加于", "pos": ""},
        ]
    },
    "unit_63": {
        "name": "CET4词汇 第63单元",
        "words": [
            {"word": "loan", "phonetic": "", "meaning": "贷款、借出", "pos": ""},
            {"word": "narrow", "phonetic": "", "meaning": "狭窄的", "pos": ""},
            {"word": "pace", "phonetic": "", "meaning": "速度、行进", "pos": ""},
            {"word": "participate", "phonetic": "", "meaning": "参与、分享", "pos": ""},
            {"word": "transfer", "phonetic": "", "meaning": "转移、转让", "pos": ""},
            {"word": "vary", "phonetic": "", "meaning": "改变", "pos": ""},
            {"word": "vote", "phonetic": "", "meaning": "投票、选票", "pos": ""},
            {"word": "yes", "phonetic": "", "meaning": "是", "pos": ""},
            {"word": "alcohol", "phonetic": "", "meaning": "酒精", "pos": ""},
            {"word": "breakfast", "phonetic": "", "meaning": "早饭", "pos": ""},
            {"word": "contract", "phonetic": "", "meaning": "合同、缩小", "pos": ""},
            {"word": "demonstrate", "phonetic": "", "meaning": "论证、说明", "pos": ""},
            {"word": "district", "phonetic": "", "meaning": "地区", "pos": ""},
            {"word": "dry", "phonetic": "", "meaning": "干燥的", "pos": ""},
            {"word": "evening", "phonetic": "", "meaning": "傍晚", "pos": ""},
            {"word": "fundamental", "phonetic": "", "meaning": "基础的、根本的", "pos": ""},
            {"word": "origin", "phonetic": "", "meaning": "起源", "pos": ""},
            {"word": "recommend", "phonetic": "", "meaning": "推荐", "pos": ""},
            {"word": "afraid", "phonetic": "", "meaning": "害怕的", "pos": ""},
            {"word": "capable", "phonetic": "", "meaning": "有能力的", "pos": ""},
        ]
    },
    "unit_64": {
        "name": "CET4词汇 第64单元",
        "words": [
            {"word": "cash", "phonetic": "", "meaning": "现金", "pos": ""},
            {"word": "gene", "phonetic": "", "meaning": "基因", "pos": ""},
            {"word": "moreover", "phonetic": "", "meaning": "再者", "pos": ""},
            {"word": "ordinary", "phonetic": "", "meaning": "普通的", "pos": ""},
            {"word": "persuade", "phonetic": "", "meaning": "说服", "pos": ""},
            {"word": "photo", "phonetic": "", "meaning": "照片", "pos": ""},
            {"word": "quarter", "phonetic": "", "meaning": "四分之一、季度", "pos": ""},
            {"word": "secret", "phonetic": "", "meaning": "秘密", "pos": ""},
            {"word": "software", "phonetic": "", "meaning": "软件", "pos": ""},
            {"word": "steal", "phonetic": "", "meaning": "偷", "pos": ""},
            {"word": "thought", "phonetic": "", "meaning": "思想、想法", "pos": ""},
            {"word": "wave", "phonetic": "", "meaning": "招手", "pos": ""},
            {"word": "apart", "phonetic": "", "meaning": "相隔、分开", "pos": ""},
            {"word": "athlete", "phonetic": "", "meaning": "运动员", "pos": ""},
            {"word": "corporation", "phonetic": "", "meaning": "公司、法人", "pos": ""},
            {"word": "homework", "phonetic": "", "meaning": "作业", "pos": ""},
            {"word": "outcome", "phonetic": "", "meaning": "结果", "pos": ""},
            {"word": "sight", "phonetic": "", "meaning": "视野、景象", "pos": ""},
            {"word": "surface", "phonetic": "", "meaning": "表面", "pos": ""},
            {"word": "burden", "phonetic": "", "meaning": "负担", "pos": ""},
        ]
    },
    "unit_65": {
        "name": "CET4词汇 第65单元",
        "words": [
            {"word": "cycle", "phonetic": "", "meaning": "骑自行车、周期", "pos": ""},
            {"word": "electricity", "phonetic": "", "meaning": "电、电学", "pos": ""},
            {"word": "email", "phonetic": "", "meaning": "电子邮件", "pos": ""},
            {"word": "final", "phonetic": "", "meaning": "最终的", "pos": ""},
            {"word": "justice", "phonetic": "", "meaning": "公平、审判", "pos": ""},
            {"word": "king", "phonetic": "", "meaning": "君主", "pos": ""},
            {"word": "mountain", "phonetic": "", "meaning": "山", "pos": ""},
            {"word": "notice", "phonetic": "", "meaning": "注意、通知", "pos": ""},
            {"word": "salary", "phonetic": "", "meaning": "薪水", "pos": ""},
            {"word": "satellite", "phonetic": "", "meaning": "卫星", "pos": ""},
            {"word": "annual", "phonetic": "", "meaning": "每年的、全年的", "pos": ""},
            {"word": "comfort", "phonetic": "", "meaning": "舒适、安慰", "pos": ""},
            {"word": "earthquake", "phonetic": "", "meaning": "地震", "pos": ""},
            {"word": "ease", "phonetic": "", "meaning": "减轻", "pos": ""},
            {"word": "engine", "phonetic": "", "meaning": "引擎", "pos": ""},
            {"word": "foundation", "phonetic": "", "meaning": "基础、地基", "pos": ""},
            {"word": "garden", "phonetic": "", "meaning": "花园、园艺", "pos": ""},
            {"word": "guarantee", "phonetic": "", "meaning": "保障", "pos": ""},
            {"word": "lunch", "phonetic": "", "meaning": "午饭", "pos": ""},
            {"word": "request", "phonetic": "", "meaning": "请求", "pos": ""},
        ]
    },
    "unit_66": {
        "name": "CET4词汇 第66单元",
        "words": [
            {"word": "symbol", "phonetic": "", "meaning": "符号、象征", "pos": ""},
            {"word": "telephone", "phonetic": "", "meaning": "电话、打电话", "pos": ""},
            {"word": "arise", "phonetic": "", "meaning": "形成、上升", "pos": ""},
            {"word": "climb", "phonetic": "", "meaning": "攀爬", "pos": ""},
            {"word": "partly", "phonetic": "", "meaning": "部分地", "pos": ""},
            {"word": "rapid", "phonetic": "", "meaning": "快的", "pos": ""},
            {"word": "tie", "phonetic": "", "meaning": "系", "pos": ""},
            {"word": "abandon", "phonetic": "", "meaning": "抛弃", "pos": ""},
            {"word": "custom", "phonetic": "", "meaning": "习惯、惠顾", "pos": ""},
            {"word": "fee", "phonetic": "", "meaning": "费用", "pos": ""},
            {"word": "island", "phonetic": "", "meaning": "岛", "pos": ""},
            {"word": "net", "phonetic": "", "meaning": "网、净的", "pos": ""},
            {"word": "none", "phonetic": "", "meaning": "没有", "pos": ""},
            {"word": "pound", "phonetic": "", "meaning": "英镑、磅", "pos": ""},
            {"word": "stem", "phonetic": "", "meaning": "茎、词干", "pos": ""},
            {"word": "widespread", "phonetic": "", "meaning": "遍布的", "pos": ""},
            {"word": "distinguish", "phonetic": "", "meaning": "区别、使有特色", "pos": ""},
            {"word": "favor", "phonetic": "", "meaning": "喜欢、赞同", "pos": ""},
            {"word": "independent", "phonetic": "", "meaning": "独立的、私营的", "pos": ""},
            {"word": "notion", "phonetic": "", "meaning": "概念、见解、打算", "pos": ""},
        ]
    },
    "unit_67": {
        "name": "CET4词汇 第67单元",
        "words": [
            {"word": "perspective", "phonetic": "", "meaning": "观点、判断力", "pos": ""},
            {"word": "secure", "phonetic": "", "meaning": "使安全、争取到", "pos": ""},
            {"word": "throw", "phonetic": "", "meaning": "扔", "pos": ""},
            {"word": "toy", "phonetic": "", "meaning": "玩具", "pos": ""},
            {"word": "transport", "phonetic": "", "meaning": "运输", "pos": ""},
            {"word": "ambition", "phonetic": "", "meaning": "雄心、志向", "pos": ""},
            {"word": "behave", "phonetic": "", "meaning": "表现", "pos": ""},
            {"word": "dark", "phonetic": "", "meaning": "黑暗的、深色的", "pos": ""},
            {"word": "disappear", "phonetic": "", "meaning": "消失", "pos": ""},
            {"word": "giant", "phonetic": "", "meaning": "巨人、巨大的", "pos": ""},
            {"word": "height", "phonetic": "", "meaning": "身高", "pos": ""},
            {"word": "inspire", "phonetic": "", "meaning": "激发", "pos": ""},
            {"word": "kitchen", "phonetic": "", "meaning": "厨房", "pos": ""},
            {"word": "monitor", "phonetic": "", "meaning": "监视器", "pos": ""},
            {"word": "quit", "phonetic": "", "meaning": "退出", "pos": ""},
            {"word": "reject", "phonetic": "", "meaning": "拒绝", "pos": ""},
            {"word": "suit", "phonetic": "", "meaning": "适合", "pos": ""},
            {"word": "typical", "phonetic": "", "meaning": "典型的", "pos": ""},
            {"word": "youth", "phonetic": "", "meaning": "青春、年轻人", "pos": ""},
            {"word": "actor", "phonetic": "", "meaning": "男演员", "pos": ""},
        ]
    },
    "unit_68": {
        "name": "CET4词汇 第68单元",
        "words": [
            {"word": "egg", "phonetic": "", "meaning": "蛋、卵", "pos": ""},
            {"word": "extent", "phonetic": "", "meaning": "程度、长度", "pos": ""},
            {"word": "jump", "phonetic": "", "meaning": "跳", "pos": ""},
            {"word": "phenomenon", "phonetic": "", "meaning": "现象", "pos": ""},
            {"word": "physician", "phonetic": "", "meaning": "医师", "pos": ""},
            {"word": "proportion", "phonetic": "", "meaning": "部分、比例", "pos": ""},
            {"word": "pursue", "phonetic": "", "meaning": "追求", "pos": ""},
            {"word": "bracket", "phonetic": "", "meaning": "括号", "pos": ""},
            {"word": "coffee", "phonetic": "", "meaning": "咖啡", "pos": ""},
            {"word": "crash", "phonetic": "", "meaning": "碰撞", "pos": ""},
            {"word": "duty", "phonetic": "", "meaning": "责任", "pos": ""},
            {"word": "overseas", "phonetic": "", "meaning": "外国的、在海外", "pos": ""},
            {"word": "recall", "phonetic": "", "meaning": "回忆", "pos": ""},
            {"word": "river", "phonetic": "", "meaning": "河流", "pos": ""},
            {"word": "solar", "phonetic": "", "meaning": "太阳的", "pos": ""},
            {"word": "weekend", "phonetic": "", "meaning": "周末", "pos": ""},
            {"word": "winter", "phonetic": "", "meaning": "冬季", "pos": ""},
            {"word": "concentrate", "phonetic": "", "meaning": "集中", "pos": ""},
            {"word": "enormous", "phonetic": "", "meaning": "巨大的", "pos": ""},
            {"word": "path", "phonetic": "", "meaning": "小道", "pos": ""},
        ]
    },
    "unit_69": {
        "name": "CET4词汇 第69单元",
        "words": [
            {"word": "urge", "phonetic": "", "meaning": "催促、敦促", "pos": ""},
            {"word": "worldwide", "phonetic": "", "meaning": "全世界的", "pos": ""},
            {"word": "bed", "phonetic": "", "meaning": "床", "pos": ""},
            {"word": "daughter", "phonetic": "", "meaning": "女儿", "pos": ""},
            {"word": "immediate", "phonetic": "", "meaning": "立即的", "pos": ""},
            {"word": "liberal", "phonetic": "", "meaning": "不严格的、自由的", "pos": ""},
            {"word": "retire", "phonetic": "", "meaning": "退休", "pos": ""},
            {"word": "client", "phonetic": "", "meaning": "顾客、委托人", "pos": ""},
            {"word": "clone", "phonetic": "", "meaning": "克隆", "pos": ""},
            {"word": "commission", "phonetic": "", "meaning": "委员会、委托", "pos": ""},
            {"word": "fun", "phonetic": "", "meaning": "快乐", "pos": ""},
            {"word": "insist", "phonetic": "", "meaning": "坚持", "pos": ""},
            {"word": "institute", "phonetic": "", "meaning": "机构、建立", "pos": ""},
            {"word": "nine", "phonetic": "", "meaning": "九", "pos": ""},
            {"word": "quiet", "phonetic": "", "meaning": "安静的", "pos": ""},
            {"word": "rare", "phonetic": "", "meaning": "稀少的、稀薄的", "pos": ""},
            {"word": "scholar", "phonetic": "", "meaning": "学者", "pos": ""},
            {"word": "settle", "phonetic": "", "meaning": "安定、定居", "pos": ""},
            {"word": "substance", "phonetic": "", "meaning": "物质", "pos": ""},
            {"word": "indifferent", "phonetic": "", "meaning": "漠不关心的", "pos": ""},
        ]
    },
    "unit_70": {
        "name": "CET4词汇 第70单元",
        "words": [
            {"word": "mobile", "phonetic": "", "meaning": "移动的", "pos": ""},
            {"word": "mood", "phonetic": "", "meaning": "情绪、心情", "pos": ""},
            {"word": "officer", "phonetic": "", "meaning": "官员、军官", "pos": ""},
            {"word": "plastic", "phonetic": "", "meaning": "塑料、可塑的", "pos": ""},
            {"word": "smell", "phonetic": "", "meaning": "闻", "pos": ""},
            {"word": "symptom", "phonetic": "", "meaning": "症状", "pos": ""},
            {"word": "bright", "phonetic": "", "meaning": "明亮的", "pos": ""},
            {"word": "fault", "phonetic": "", "meaning": "错误", "pos": ""},
            {"word": "neglect", "phonetic": "", "meaning": "忽视、疏忽", "pos": ""},
            {"word": "reputation", "phonetic": "", "meaning": "名誉", "pos": ""},
            {"word": "transform", "phonetic": "", "meaning": "改变", "pos": ""},
            {"word": "workforce", "phonetic": "", "meaning": "劳动力", "pos": ""},
            {"word": "assess", "phonetic": "", "meaning": "评估", "pos": ""},
            {"word": "atmosphere", "phonetic": "", "meaning": "气氛", "pos": ""},
            {"word": "deny", "phonetic": "", "meaning": "否定", "pos": ""},
            {"word": "extreme", "phonetic": "", "meaning": "极端", "pos": ""},
            {"word": "religion", "phonetic": "", "meaning": "宗教、信念", "pos": ""},
            {"word": "root", "phonetic": "", "meaning": "根、根本", "pos": ""},
            {"word": "seldom", "phonetic": "", "meaning": "很少的", "pos": ""},
            {"word": "severe", "phonetic": "", "meaning": "严重的", "pos": ""},
        ]
    },
    "unit_71": {
        "name": "CET4词汇 第71单元",
        "words": [
            {"word": "tip", "phonetic": "", "meaning": "末端、小费、提示", "pos": ""},
            {"word": "alternative", "phonetic": "", "meaning": "备选的", "pos": ""},
            {"word": "cancel", "phonetic": "", "meaning": "取消", "pos": ""},
            {"word": "chair", "phonetic": "", "meaning": "椅子", "pos": ""},
            {"word": "cool", "phonetic": "", "meaning": "冷却", "pos": ""},
            {"word": "depth", "phonetic": "", "meaning": "深度", "pos": ""},
            {"word": "deserve", "phonetic": "", "meaning": "值得、应得", "pos": ""},
            {"word": "organic", "phonetic": "", "meaning": "器官的、有机物的", "pos": ""},
            {"word": "pose", "phonetic": "", "meaning": "摆姿势、提出", "pos": ""},
            {"word": "protein", "phonetic": "", "meaning": "蛋白质", "pos": ""},
            {"word": "relevant", "phonetic": "", "meaning": "相关的", "pos": ""},
            {"word": "repeat", "phonetic": "", "meaning": "重复", "pos": ""},
            {"word": "vital", "phonetic": "", "meaning": "重要的", "pos": ""},
            {"word": "attribute", "phonetic": "", "meaning": "属性", "pos": ""},
            {"word": "chain", "phonetic": "", "meaning": "链", "pos": ""},
            {"word": "mere", "phonetic": "", "meaning": "仅仅的", "pos": ""},
            {"word": "opposite", "phonetic": "", "meaning": "相反的、对立面", "pos": ""},
            {"word": "possess", "phonetic": "", "meaning": "拥有、具有", "pos": ""},
            {"word": "profession", "phonetic": "", "meaning": "职业", "pos": ""},
            {"word": "remote", "phonetic": "", "meaning": "遥远的", "pos": ""},
        ]
    },
    "unit_72": {
        "name": "CET4词汇 第72单元",
        "words": [
            {"word": "tomorrow", "phonetic": "", "meaning": "明天、来日", "pos": ""},
            {"word": "arrange", "phonetic": "", "meaning": "安排", "pos": ""},
            {"word": "chapter", "phonetic": "", "meaning": "章节", "pos": ""},
            {"word": "continent", "phonetic": "", "meaning": "大陆", "pos": ""},
            {"word": "everyday", "phonetic": "", "meaning": "每日的", "pos": ""},
            {"word": "faculty", "phonetic": "", "meaning": "才能、学院", "pos": ""},
            {"word": "praise", "phonetic": "", "meaning": "赞美、表扬", "pos": ""},
            {"word": "stimulate", "phonetic": "", "meaning": "刺激、使兴奋", "pos": ""},
            {"word": "stone", "phonetic": "", "meaning": "石头", "pos": ""},
            {"word": "version", "phonetic": "", "meaning": "版本", "pos": ""},
            {"word": "volunteer", "phonetic": "", "meaning": "志愿者", "pos": ""},
            {"word": "website", "phonetic": "", "meaning": "网站", "pos": ""},
            {"word": "absorb", "phonetic": "", "meaning": "吸收", "pos": ""},
            {"word": "affair", "phonetic": "", "meaning": "事情、事务", "pos": ""},
            {"word": "assign", "phonetic": "", "meaning": "分配、指定", "pos": ""},
            {"word": "belong", "phonetic": "", "meaning": "属于", "pos": ""},
            {"word": "highway", "phonetic": "", "meaning": "公路", "pos": ""},
            {"word": "joy", "phonetic": "", "meaning": "欢乐", "pos": ""},
            {"word": "meanwhile", "phonetic": "", "meaning": "与此同时", "pos": ""},
            {"word": "mission", "phonetic": "", "meaning": "使命", "pos": ""},
        ]
    },
    "unit_73": {
        "name": "CET4词汇 第73单元",
        "words": [
            {"word": "perceive", "phonetic": "", "meaning": "察觉、理解", "pos": ""},
            {"word": "preview", "phonetic": "", "meaning": "预告、试映", "pos": ""},
            {"word": "undergraduate", "phonetic": "", "meaning": "大学生", "pos": ""},
            {"word": "weak", "phonetic": "", "meaning": "弱的", "pos": ""},
            {"word": "acknowledge", "phonetic": "", "meaning": "承认", "pos": ""},
            {"word": "adjust", "phonetic": "", "meaning": "调整", "pos": ""},
            {"word": "airline", "phonetic": "", "meaning": "航线", "pos": ""},
            {"word": "analyze", "phonetic": "", "meaning": "分析", "pos": ""},
            {"word": "announce", "phonetic": "", "meaning": "宣布", "pos": ""},
            {"word": "approve", "phonetic": "", "meaning": "赞同", "pos": ""},
            {"word": "borrow", "phonetic": "", "meaning": "借", "pos": ""},
            {"word": "incentive", "phonetic": "", "meaning": "刺激、动机", "pos": ""},
            {"word": "locate", "phonetic": "", "meaning": "指出、位于", "pos": ""},
            {"word": "necessity", "phonetic": "", "meaning": "必要、必然性", "pos": ""},
            {"word": "usual", "phonetic": "", "meaning": "通常的", "pos": ""},
            {"word": "victim", "phonetic": "", "meaning": "受害者", "pos": ""},
            {"word": "asset", "phonetic": "", "meaning": "资产、天赋", "pos": ""},
            {"word": "beauty", "phonetic": "", "meaning": "美丽、美人", "pos": ""},
            {"word": "considerable", "phonetic": "", "meaning": "相当大的", "pos": ""},
            {"word": "constant", "phonetic": "", "meaning": "坚定的、经常的", "pos": ""},
        ]
    },
    "unit_74": {
        "name": "CET4词汇 第74单元",
        "words": [
            {"word": "council", "phonetic": "", "meaning": "理事会", "pos": ""},
            {"word": "criticize", "phonetic": "", "meaning": "批评", "pos": ""},
            {"word": "document", "phonetic": "", "meaning": "文档", "pos": ""},
            {"word": "entire", "phonetic": "", "meaning": "完全的", "pos": ""},
            {"word": "leisure", "phonetic": "", "meaning": "空闲、悠闲", "pos": ""},
            {"word": "reverse", "phonetic": "", "meaning": "相反的、倒退的", "pos": ""},
            {"word": "apartment", "phonetic": "", "meaning": "房间、公寓", "pos": ""},
            {"word": "appreciate", "phonetic": "", "meaning": "欣赏、感激", "pos": ""},
            {"word": "nobody", "phonetic": "", "meaning": "谁也不、小人物", "pos": ""},
            {"word": "recover", "phonetic": "", "meaning": "恢复", "pos": ""},
            {"word": "sister", "phonetic": "", "meaning": "姐妹", "pos": ""},
            {"word": "somewhat", "phonetic": "", "meaning": "稍微", "pos": ""},
            {"word": "bottle", "phonetic": "", "meaning": "瓶子", "pos": ""},
            {"word": "ceremony", "phonetic": "", "meaning": "仪式", "pos": ""},
            {"word": "coach", "phonetic": "", "meaning": "教练", "pos": ""},
            {"word": "convey", "phonetic": "", "meaning": "运输", "pos": ""},
            {"word": "dead", "phonetic": "", "meaning": "死去的、麻木的", "pos": ""},
            {"word": "discourage", "phonetic": "", "meaning": "使泄气", "pos": ""},
            {"word": "elsewhere", "phonetic": "", "meaning": "在别处", "pos": ""},
            {"word": "jam", "phonetic": "", "meaning": "拥堵、果酱", "pos": ""},
        ]
    },
    "unit_75": {
        "name": "CET4词汇 第75单元",
        "words": [
            {"word": "justify", "phonetic": "", "meaning": "证明……正当", "pos": ""},
            {"word": "merit", "phonetic": "", "meaning": "值得、价值", "pos": ""},
            {"word": "occasion", "phonetic": "", "meaning": "机会、重大活动", "pos": ""},
            {"word": "plate", "phonetic": "", "meaning": "盘子", "pos": ""},
            {"word": "procedure", "phonetic": "", "meaning": "步骤", "pos": ""},
            {"word": "stick", "phonetic": "", "meaning": "棍、刺、粘贴", "pos": ""},
            {"word": "strict", "phonetic": "", "meaning": "严格的", "pos": ""},
            {"word": "virtual", "phonetic": "", "meaning": "实际上的", "pos": ""},
            {"word": "aside", "phonetic": "", "meaning": "在旁边", "pos": ""},
            {"word": "bind", "phonetic": "", "meaning": "捆扎", "pos": ""},
            {"word": "capture", "phonetic": "", "meaning": "占领、体现、吸引、拍摄", "pos": ""},
            {"word": "eager", "phonetic": "", "meaning": "渴望的", "pos": ""},
            {"word": "fifth", "phonetic": "", "meaning": "第五", "pos": ""},
            {"word": "grain", "phonetic": "", "meaning": "谷物", "pos": ""},
            {"word": "inevitable", "phonetic": "", "meaning": "不可避免的", "pos": ""},
            {"word": "recruit", "phonetic": "", "meaning": "招募、新兵", "pos": ""},
            {"word": "retail", "phonetic": "", "meaning": "零售", "pos": ""},
            {"word": "satisfy", "phonetic": "", "meaning": "满意、使确信", "pos": ""},
            {"word": "sick", "phonetic": "", "meaning": "生病的", "pos": ""},
            {"word": "skin", "phonetic": "", "meaning": "皮", "pos": ""},
        ]
    },
    "unit_76": {
        "name": "CET4词汇 第76单元",
        "words": [
            {"word": "surprise", "phonetic": "", "meaning": "惊讶", "pos": ""},
            {"word": "wind", "phonetic": "", "meaning": "风", "pos": ""},
            {"word": "bacteria", "phonetic": "", "meaning": "细菌", "pos": ""},
            {"word": "border", "phonetic": "", "meaning": "边界", "pos": ""},
            {"word": "brief", "phonetic": "", "meaning": "简短的", "pos": ""},
            {"word": "cultivate", "phonetic": "", "meaning": "耕作、培养", "pos": ""},
            {"word": "edge", "phonetic": "", "meaning": "边、刀口", "pos": ""},
            {"word": "export", "phonetic": "", "meaning": "输出、出口", "pos": ""},
            {"word": "fruit", "phonetic": "", "meaning": "水果", "pos": ""},
            {"word": "hide", "phonetic": "", "meaning": "隐藏", "pos": ""},
            {"word": "recycle", "phonetic": "", "meaning": "回收", "pos": ""},
            {"word": "scene", "phonetic": "", "meaning": "场景", "pos": ""},
            {"word": "treasure", "phonetic": "", "meaning": "宝藏", "pos": ""},
            {"word": "empty", "phonetic": "", "meaning": "空的", "pos": ""},
            {"word": "everybody", "phonetic": "", "meaning": "每人", "pos": ""},
            {"word": "hair", "phonetic": "", "meaning": "头发", "pos": ""},
            {"word": "instrument", "phonetic": "", "meaning": "工具、乐器", "pos": ""},
            {"word": "nice", "phonetic": "", "meaning": "很好的", "pos": ""},
            {"word": "regardless", "phonetic": "", "meaning": "不留心的、不顾", "pos": ""},
            {"word": "spring", "phonetic": "", "meaning": "春天、跳跃", "pos": ""},
        ]
    },
    "unit_77": {
        "name": "CET4词汇 第77单元",
        "words": [
            {"word": "sustain", "phonetic": "", "meaning": "支撑、忍受", "pos": ""},
            {"word": "valley", "phonetic": "", "meaning": "山谷", "pos": ""},
            {"word": "arm", "phonetic": "", "meaning": "手臂", "pos": ""},
            {"word": "beat", "phonetic": "", "meaning": "击败", "pos": ""},
            {"word": "confront", "phonetic": "", "meaning": "使面临、勇敢地面对", "pos": ""},
            {"word": "conscious", "phonetic": "", "meaning": "神志清醒的、意识到的", "pos": ""},
            {"word": "delete", "phonetic": "", "meaning": "删除", "pos": ""},
            {"word": "entitle", "phonetic": "", "meaning": "给……题名、给……权利", "pos": ""},
            {"word": "excellent", "phonetic": "", "meaning": "优秀的", "pos": ""},
            {"word": "glass", "phonetic": "", "meaning": "玻璃、玻璃杯", "pos": ""},
            {"word": "hero", "phonetic": "", "meaning": "英雄", "pos": ""},
            {"word": "laugh", "phonetic": "", "meaning": "笑", "pos": ""},
            {"word": "muscle", "phonetic": "", "meaning": "肌肉、体力", "pos": ""},
            {"word": "peak", "phonetic": "", "meaning": "最高点", "pos": ""},
            {"word": "prompt", "phonetic": "", "meaning": "敏捷的、提示", "pos": ""},
            {"word": "shrink", "phonetic": "", "meaning": "起皱、减少", "pos": ""},
            {"word": "spirit", "phonetic": "", "meaning": "精神", "pos": ""},
            {"word": "suspect", "phonetic": "", "meaning": "怀疑", "pos": ""},
            {"word": "universe", "phonetic": "", "meaning": "宇宙", "pos": ""},
            {"word": "wild", "phonetic": "", "meaning": "野生的", "pos": ""},
        ]
    },
    "unit_78": {
        "name": "CET4词汇 第78单元",
        "words": [
            {"word": "bar", "phonetic": "", "meaning": "条、酒吧", "pos": ""},
            {"word": "branch", "phonetic": "", "meaning": "枝、分部", "pos": ""},
            {"word": "dance", "phonetic": "", "meaning": "跳舞", "pos": ""},
            {"word": "declare", "phonetic": "", "meaning": "宣布", "pos": ""},
            {"word": "east", "phonetic": "", "meaning": "东、东方的", "pos": ""},
            {"word": "everywhere", "phonetic": "", "meaning": "到处", "pos": ""},
            {"word": "hill", "phonetic": "", "meaning": "小山", "pos": ""},
            {"word": "invent", "phonetic": "", "meaning": "发明", "pos": ""},
            {"word": "literary", "phonetic": "", "meaning": "文学的", "pos": ""},
            {"word": "maybe", "phonetic": "", "meaning": "可能、大概", "pos": ""},
            {"word": "minister", "phonetic": "", "meaning": "部长", "pos": ""},
            {"word": "puzzle", "phonetic": "", "meaning": "使……困惑", "pos": ""},
            {"word": "register", "phonetic": "", "meaning": "注册", "pos": ""},
            {"word": "resume", "phonetic": "", "meaning": "重新开始、恢复", "pos": ""},
            {"word": "season", "phonetic": "", "meaning": "季节", "pos": ""},
            {"word": "volume", "phonetic": "", "meaning": "容积、音量（一）卷", "pos": ""},
            {"word": "witness", "phonetic": "", "meaning": "目击、见证", "pos": ""},
            {"word": "band", "phonetic": "", "meaning": "乐队、带子", "pos": ""},
            {"word": "battle", "phonetic": "", "meaning": "战斗", "pos": ""},
            {"word": "category", "phonetic": "", "meaning": "类别", "pos": ""},
        ]
    },
    "unit_79": {
        "name": "CET4词汇 第79单元",
        "words": [
            {"word": "committee", "phonetic": "", "meaning": "委员会", "pos": ""},
            {"word": "congress", "phonetic": "", "meaning": "代表大会", "pos": ""},
            {"word": "convenient", "phonetic": "", "meaning": "方便的", "pos": ""},
            {"word": "dress", "phonetic": "", "meaning": "穿", "pos": ""},
            {"word": "fifty", "phonetic": "", "meaning": "五十", "pos": ""},
            {"word": "football", "phonetic": "", "meaning": "足球", "pos": ""},
            {"word": "infant", "phonetic": "", "meaning": "婴幼儿", "pos": ""},
            {"word": "nevertheless", "phonetic": "", "meaning": "然而", "pos": ""},
            {"word": "urgent", "phonetic": "", "meaning": "紧迫的", "pos": ""},
            {"word": "vacation", "phonetic": "", "meaning": "假期", "pos": ""},
            {"word": "vulnerable", "phonetic": "", "meaning": "易受攻击的", "pos": ""},
            {"word": "accurate", "phonetic": "", "meaning": "精确的", "pos": ""},
            {"word": "brown", "phonetic": "", "meaning": "褐色的", "pos": ""},
            {"word": "confirm", "phonetic": "", "meaning": "证实、确认", "pos": ""},
            {"word": "detect", "phonetic": "", "meaning": "查明、发现", "pos": ""},
            {"word": "dispute", "phonetic": "", "meaning": "争论", "pos": ""},
            {"word": "divorce", "phonetic": "", "meaning": "离婚、断绝关系", "pos": ""},
            {"word": "estate", "phonetic": "", "meaning": "地产、遗产", "pos": ""},
            {"word": "hang", "phonetic": "", "meaning": "挂", "pos": ""},
            {"word": "host", "phonetic": "", "meaning": "主持人", "pos": ""},
        ]
    },
    "unit_80": {
        "name": "CET4词汇 第80单元",
        "words": [
            {"word": "odd", "phonetic": "", "meaning": "奇数的、奇怪的", "pos": ""},
            {"word": "raw", "phonetic": "", "meaning": "生的、未经训练的", "pos": ""},
            {"word": "snow", "phonetic": "", "meaning": "雪", "pos": ""},
            {"word": "unit", "phonetic": "", "meaning": "单元、单位", "pos": ""},
            {"word": "cat", "phonetic": "", "meaning": "猫", "pos": ""},
            {"word": "craft", "phonetic": "", "meaning": "工艺", "pos": ""},
            {"word": "curriculum", "phonetic": "", "meaning": "课程", "pos": ""},
            {"word": "elite", "phonetic": "", "meaning": "精英", "pos": ""},
            {"word": "evolve", "phonetic": "", "meaning": "使发展", "pos": ""},
            {"word": "flexible", "phonetic": "", "meaning": "灵活的", "pos": ""},
            {"word": "mislead", "phonetic": "", "meaning": "误导", "pos": ""},
            {"word": "plenty", "phonetic": "", "meaning": "丰富、大量", "pos": ""},
            {"word": "trial", "phonetic": "", "meaning": "审判、试用", "pos": ""},
            {"word": "vegetable", "phonetic": "", "meaning": "蔬菜", "pos": ""},
            {"word": "weigh", "phonetic": "", "meaning": "称重量、有影响", "pos": ""},
            {"word": "alarm", "phonetic": "", "meaning": "警报", "pos": ""},
            {"word": "bag", "phonetic": "", "meaning": "包、袋", "pos": ""},
            {"word": "beach", "phonetic": "", "meaning": "海滩", "pos": ""},
            {"word": "contrary", "phonetic": "", "meaning": "相反的、对方的", "pos": ""},
            {"word": "desert", "phonetic": "", "meaning": "遗弃、沙漠", "pos": ""},
        ]
    },
    "unit_81": {
        "name": "CET4词汇 第81单元",
        "words": [
            {"word": "highlight", "phonetic": "", "meaning": "使显著、强调", "pos": ""},
            {"word": "interact", "phonetic": "", "meaning": "互动", "pos": ""},
            {"word": "regulate", "phonetic": "", "meaning": "管理", "pos": ""},
            {"word": "remark", "phonetic": "", "meaning": "评价、评论", "pos": ""},
            {"word": "royal", "phonetic": "", "meaning": "皇家的", "pos": ""},
            {"word": "rush", "phonetic": "", "meaning": "冲", "pos": ""},
            {"word": "scheme", "phonetic": "", "meaning": "计划、密谋", "pos": ""},
            {"word": "usage", "phonetic": "", "meaning": "用法", "pos": ""},
            {"word": "bottom", "phonetic": "", "meaning": "底下", "pos": ""},
            {"word": "evil", "phonetic": "", "meaning": "邪恶的、坏的", "pos": ""},
            {"word": "internal", "phonetic": "", "meaning": "内部的", "pos": ""},
            {"word": "surround", "phonetic": "", "meaning": "周围", "pos": ""},
            {"word": "anticipate", "phonetic": "", "meaning": "预期、先发制人", "pos": ""},
            {"word": "deprive", "phonetic": "", "meaning": "剥夺", "pos": ""},
            {"word": "finance", "phonetic": "", "meaning": "财政", "pos": ""},
            {"word": "guideline", "phonetic": "", "meaning": "指导方针、指导原则", "pos": ""},
            {"word": "journey", "phonetic": "", "meaning": "旅行", "pos": ""},
            {"word": "license", "phonetic": "", "meaning": "执照", "pos": ""},
            {"word": "myself", "phonetic": "", "meaning": "我自己、我亲自", "pos": ""},
            {"word": "protest", "phonetic": "", "meaning": "抗议", "pos": ""},
        ]
    },
    "unit_82": {
        "name": "CET4词汇 第82单元",
        "words": [
            {"word": "route", "phonetic": "", "meaning": "路线", "pos": ""},
            {"word": "seed", "phonetic": "", "meaning": "种子、播种", "pos": ""},
            {"word": "solid", "phonetic": "", "meaning": "固体的", "pos": ""},
            {"word": "submit", "phonetic": "", "meaning": "顺从、递交", "pos": ""},
            {"word": "tap", "phonetic": "", "meaning": "提取、利用", "pos": ""},
            {"word": "whereas", "phonetic": "", "meaning": "而、考虑到", "pos": ""},
            {"word": "adequate", "phonetic": "", "meaning": "充足的", "pos": ""},
            {"word": "besides", "phonetic": "", "meaning": "除了之外、而且", "pos": ""},
            {"word": "boom", "phonetic": "", "meaning": "繁荣", "pos": ""},
            {"word": "bridge", "phonetic": "", "meaning": "桥", "pos": ""},
            {"word": "contest", "phonetic": "", "meaning": "比赛", "pos": ""},
            {"word": "emergency", "phonetic": "", "meaning": "紧急情况", "pos": ""},
            {"word": "god", "phonetic": "", "meaning": "神、上帝", "pos": ""},
            {"word": "grass", "phonetic": "", "meaning": "草", "pos": ""},
            {"word": "illegal", "phonetic": "", "meaning": "不合法的", "pos": ""},
            {"word": "milk", "phonetic": "", "meaning": "牛奶", "pos": ""},
            {"word": "modify", "phonetic": "", "meaning": "修改、缓和", "pos": ""},
            {"word": "mystery", "phonetic": "", "meaning": "神秘", "pos": ""},
            {"word": "philosophy", "phonetic": "", "meaning": "哲学", "pos": ""},
            {"word": "reluctant", "phonetic": "", "meaning": "厌恶的", "pos": ""},
        ]
    },
    "unit_83": {
        "name": "CET4词汇 第83单元",
        "words": [
            {"word": "rural", "phonetic": "", "meaning": "乡村的", "pos": ""},
            {"word": "sharp", "phonetic": "", "meaning": "尖的、清晰的", "pos": ""},
            {"word": "stable", "phonetic": "", "meaning": "稳定的", "pos": ""},
            {"word": "zone", "phonetic": "", "meaning": "区域", "pos": ""},
            {"word": "accelerate", "phonetic": "", "meaning": "加速", "pos": ""},
            {"word": "barrier", "phonetic": "", "meaning": "障碍", "pos": ""},
            {"word": "breath", "phonetic": "", "meaning": "呼吸", "pos": ""},
            {"word": "breed", "phonetic": "", "meaning": "养育、繁殖", "pos": ""},
            {"word": "counterpart", "phonetic": "", "meaning": "同行", "pos": ""},
            {"word": "era", "phonetic": "", "meaning": "时代", "pos": ""},
            {"word": "false", "phonetic": "", "meaning": "错误的", "pos": ""},
            {"word": "pair", "phonetic": "", "meaning": "一对", "pos": ""},
            {"word": "prison", "phonetic": "", "meaning": "监狱", "pos": ""},
            {"word": "privilege", "phonetic": "", "meaning": "特权、优先权", "pos": ""},
            {"word": "restore", "phonetic": "", "meaning": "恢复、归还", "pos": ""},
            {"word": "slave", "phonetic": "", "meaning": "奴隶", "pos": ""},
            {"word": "smartphone", "phonetic": "", "meaning": "智能手机", "pos": ""},
            {"word": "uniform", "phonetic": "", "meaning": "不变的、制服", "pos": ""},
            {"word": "upset", "phonetic": "", "meaning": "沮丧、难过", "pos": ""},
            {"word": "assist", "phonetic": "", "meaning": "援助", "pos": ""},
        ]
    },
    "unit_84": {
        "name": "CET4词汇 第84单元",
        "words": [
            {"word": "broadcast", "phonetic": "", "meaning": "广播", "pos": ""},
            {"word": "crucial", "phonetic": "", "meaning": "决定性的", "pos": ""},
            {"word": "dam", "phonetic": "", "meaning": "水坝", "pos": ""},
            {"word": "desk", "phonetic": "", "meaning": "桌子", "pos": ""},
            {"word": "devote", "phonetic": "", "meaning": "奉献", "pos": ""},
            {"word": "fan", "phonetic": "", "meaning": "粉丝、扇子", "pos": ""},
            {"word": "greenhouse", "phonetic": "", "meaning": "温室", "pos": ""},
            {"word": "infrastructure", "phonetic": "", "meaning": "基础设施", "pos": ""},
            {"word": "landscape", "phonetic": "", "meaning": "风景", "pos": ""},
            {"word": "luxury", "phonetic": "", "meaning": "奢侈、奢侈品", "pos": ""},
            {"word": "permanent", "phonetic": "", "meaning": "永恒的", "pos": ""},
            {"word": "rock", "phonetic": "", "meaning": "岩石、震动", "pos": ""},
            {"word": "segment", "phonetic": "", "meaning": "段", "pos": ""},
            {"word": "snack", "phonetic": "", "meaning": "点心、易办到的事", "pos": ""},
            {"word": "tall", "phonetic": "", "meaning": "高", "pos": ""},
            {"word": "visual", "phonetic": "", "meaning": "看的", "pos": ""},
            {"word": "beneath", "phonetic": "", "meaning": "在…之下", "pos": ""},
            {"word": "channel", "phonetic": "", "meaning": "频道、隧道", "pos": ""},
            {"word": "cheat", "phonetic": "", "meaning": "作弊、欺骗", "pos": ""},
            {"word": "counter", "phonetic": "", "meaning": "柜台", "pos": ""},
        ]
    },
    "unit_85": {
        "name": "CET4词汇 第85单元",
        "words": [
            {"word": "discount", "phonetic": "", "meaning": "折扣", "pos": ""},
            {"word": "evaluate", "phonetic": "", "meaning": "评估", "pos": ""},
            {"word": "ingredient", "phonetic": "", "meaning": "成分", "pos": ""},
            {"word": "injure", "phonetic": "", "meaning": "使受伤、损害", "pos": ""},
            {"word": "maximum", "phonetic": "", "meaning": "最大的", "pos": ""},
            {"word": "minor", "phonetic": "", "meaning": "较小的、较少的", "pos": ""},
            {"word": "rat", "phonetic": "", "meaning": "老鼠、卑鄙的人", "pos": ""},
            {"word": "remind", "phonetic": "", "meaning": "提醒", "pos": ""},
            {"word": "reply", "phonetic": "", "meaning": "回复", "pos": ""},
            {"word": "sacrifice", "phonetic": "", "meaning": "牺牲", "pos": ""},
            {"word": "spare", "phonetic": "", "meaning": "空闲的", "pos": ""},
            {"word": "steel", "phonetic": "", "meaning": "钢", "pos": ""},
            {"word": "stuff", "phonetic": "", "meaning": "东西、塞入", "pos": ""},
            {"word": "sum", "phonetic": "", "meaning": "总和", "pos": ""},
            {"word": "superior", "phonetic": "", "meaning": "优良的、较……多的", "pos": ""},
            {"word": "tackle", "phonetic": "", "meaning": "用具", "pos": ""},
            {"word": "teen", "phonetic": "", "meaning": "青少年的", "pos": ""},
            {"word": "tone", "phonetic": "", "meaning": "音调、腔调", "pos": ""},
            {"word": "tour", "phonetic": "", "meaning": "旅行", "pos": ""},
            {"word": "tuition", "phonetic": "", "meaning": "学费、教学", "pos": ""},
        ]
    },
    "unit_86": {
        "name": "CET4词汇 第86单元",
        "words": [
            {"word": "virtue", "phonetic": "", "meaning": "美德、优点", "pos": ""},
            {"word": "accomplish", "phonetic": "", "meaning": "完成", "pos": ""},
            {"word": "automate", "phonetic": "", "meaning": "使自动化", "pos": ""},
            {"word": "belt", "phonetic": "", "meaning": "皮带、地带", "pos": ""},
            {"word": "camera", "phonetic": "", "meaning": "照相机", "pos": ""},
            {"word": "coast", "phonetic": "", "meaning": "海岸、沿岸航行", "pos": ""},
            {"word": "entertain", "phonetic": "", "meaning": "娱乐", "pos": ""},
            {"word": "finger", "phonetic": "", "meaning": "手指", "pos": ""},
            {"word": "furniture", "phonetic": "", "meaning": "家具", "pos": ""},
            {"word": "hall", "phonetic": "", "meaning": "大厅", "pos": ""},
            {"word": "interval", "phonetic": "", "meaning": "间隔、休息", "pos": ""},
            {"word": "laboratory", "phonetic": "", "meaning": "实验室", "pos": ""},
            {"word": "march", "phonetic": "", "meaning": "行进", "pos": ""},
            {"word": "obstacle", "phonetic": "", "meaning": "障碍", "pos": ""},
            {"word": "regret", "phonetic": "", "meaning": "遗憾、后悔", "pos": ""},
            {"word": "ride", "phonetic": "", "meaning": "骑", "pos": ""},
            {"word": "ruin", "phonetic": "", "meaning": "毁灭", "pos": ""},
            {"word": "terrible", "phonetic": "", "meaning": "很糟的、可怕的", "pos": ""},
            {"word": "trace", "phonetic": "", "meaning": "痕迹、微量", "pos": ""},
            {"word": "abuse", "phonetic": "", "meaning": "滥用、虐待", "pos": ""},
        ]
    },
    "unit_87": {
        "name": "CET4词汇 第87单元",
        "words": [
            {"word": "aggressive", "phonetic": "", "meaning": "好斗的、有侵略性的", "pos": ""},
            {"word": "bond", "phonetic": "", "meaning": "纽带", "pos": ""},
            {"word": "breathe", "phonetic": "", "meaning": "呼吸", "pos": ""},
            {"word": "camp", "phonetic": "", "meaning": "营地", "pos": ""},
            {"word": "commerce", "phonetic": "", "meaning": "商业", "pos": ""},
            {"word": "constitute", "phonetic": "", "meaning": "组成、建立", "pos": ""},
            {"word": "elementary", "phonetic": "", "meaning": "初等的、简单的", "pos": ""},
            {"word": "embrace", "phonetic": "", "meaning": "拥抱、接受", "pos": ""},
            {"word": "excuse", "phonetic": "", "meaning": "借口", "pos": ""},
            {"word": "flood", "phonetic": "", "meaning": "洪水、涌进", "pos": ""},
            {"word": "flower", "phonetic": "", "meaning": "花朵", "pos": ""},
            {"word": "motor", "phonetic": "", "meaning": "发动机", "pos": ""},
            {"word": "prime", "phonetic": "", "meaning": "最初的、首要的", "pos": ""},
            {"word": "profound", "phonetic": "", "meaning": "深刻的", "pos": ""},
            {"word": "radical", "phonetic": "", "meaning": "根本的、彻底的", "pos": ""},
            {"word": "resolve", "phonetic": "", "meaning": "解决、决定", "pos": ""},
            {"word": "salt", "phonetic": "", "meaning": "盐、腌", "pos": ""},
            {"word": "soldier", "phonetic": "", "meaning": "士兵", "pos": ""},
            {"word": "strain", "phonetic": "", "meaning": "使紧张、拉紧", "pos": ""},
            {"word": "thrive", "phonetic": "", "meaning": "繁荣", "pos": ""},
        ]
    },
    "unit_88": {
        "name": "CET4词汇 第88单元",
        "words": [
            {"word": "tiny", "phonetic": "", "meaning": "极小的", "pos": ""},
            {"word": "valid", "phonetic": "", "meaning": "合理的", "pos": ""},
            {"word": "village", "phonetic": "", "meaning": "村", "pos": ""},
            {"word": "weapon", "phonetic": "", "meaning": "武器", "pos": ""},
            {"word": "wood", "phonetic": "", "meaning": "木头、森林", "pos": ""},
            {"word": "boat", "phonetic": "", "meaning": "船", "pos": ""},
            {"word": "chip", "phonetic": "", "meaning": "薯片、芯片", "pos": ""},
            {"word": "civil", "phonetic": "", "meaning": "公民的", "pos": ""},
            {"word": "conservative", "phonetic": "", "meaning": "保守", "pos": ""},
            {"word": "dioxide", "phonetic": "", "meaning": "二氧化物", "pos": ""},
            {"word": "gamble", "phonetic": "", "meaning": "赌博、投机", "pos": ""},
            {"word": "honor", "phonetic": "", "meaning": "荣耀", "pos": ""},
            {"word": "insert", "phonetic": "", "meaning": "插入", "pos": ""},
            {"word": "mirror", "phonetic": "", "meaning": "镜子", "pos": ""},
            {"word": "panel", "phonetic": "", "meaning": "面板", "pos": ""},
            {"word": "plus", "phonetic": "", "meaning": "加上、正的", "pos": ""},
            {"word": "prejudice", "phonetic": "", "meaning": "偏见、损害", "pos": ""},
            {"word": "transaction", "phonetic": "", "meaning": "交易、业务", "pos": ""},
            {"word": "vitamin", "phonetic": "", "meaning": "维生素", "pos": ""},
            {"word": "blind", "phonetic": "", "meaning": "失明的", "pos": ""},
        ]
    },
    "unit_89": {
        "name": "CET4词汇 第89单元",
        "words": [
            {"word": "businessman", "phonetic": "", "meaning": "商人", "pos": ""},
            {"word": "chairman", "phonetic": "", "meaning": "主席", "pos": ""},
            {"word": "concert", "phonetic": "", "meaning": "音乐会", "pos": ""},
            {"word": "construct", "phonetic": "", "meaning": "建造、创立", "pos": ""},
            {"word": "disorder", "phonetic": "", "meaning": "混乱、骚乱", "pos": ""},
            {"word": "encounter", "phonetic": "", "meaning": "偶遇", "pos": ""},
            {"word": "equip", "phonetic": "", "meaning": "装备", "pos": ""},
            {"word": "file", "phonetic": "", "meaning": "文件", "pos": ""},
            {"word": "genuine", "phonetic": "", "meaning": "真的、真诚的", "pos": ""},
            {"word": "initial", "phonetic": "", "meaning": "起初的", "pos": ""},
            {"word": "instant", "phonetic": "", "meaning": "时刻、立刻", "pos": ""},
            {"word": "investigate", "phonetic": "", "meaning": "调查", "pos": ""},
            {"word": "latter", "phonetic": "", "meaning": "后者", "pos": ""},
            {"word": "minimum", "phonetic": "", "meaning": "最低的", "pos": ""},
            {"word": "neighbor", "phonetic": "", "meaning": "邻居", "pos": ""},
            {"word": "onto", "phonetic": "", "meaning": "在上面、到上面", "pos": ""},
            {"word": "overwhelm", "phonetic": "", "meaning": "征服", "pos": ""},
            {"word": "package", "phonetic": "", "meaning": "包裹", "pos": ""},
            {"word": "principal", "phonetic": "", "meaning": "最重要的、负责人", "pos": ""},
            {"word": "proof", "phonetic": "", "meaning": "证据", "pos": ""},
        ]
    },
    "unit_90": {
        "name": "CET4词汇 第90单元",
        "words": [
            {"word": "quote", "phonetic": "", "meaning": "引用", "pos": ""},
            {"word": "relieve", "phonetic": "", "meaning": "缓解、救济", "pos": ""},
            {"word": "rival", "phonetic": "", "meaning": "竞争", "pos": ""},
            {"word": "sponsor", "phonetic": "", "meaning": "赞助、资助", "pos": ""},
            {"word": "tobacco", "phonetic": "", "meaning": "烟草", "pos": ""},
            {"word": "trap", "phonetic": "", "meaning": "困住", "pos": ""},
            {"word": "truck", "phonetic": "", "meaning": "卡车", "pos": ""},
            {"word": "alert", "phonetic": "", "meaning": "警报", "pos": ""},
            {"word": "amateur", "phonetic": "", "meaning": "业余爱好者、外行", "pos": ""},
            {"word": "anywhere", "phonetic": "", "meaning": "在任何地方", "pos": ""},
            {"word": "army", "phonetic": "", "meaning": "军队、陆军", "pos": ""},
            {"word": "core", "phonetic": "", "meaning": "核心", "pos": ""},
            {"word": "ethnic", "phonetic": "", "meaning": "民族的", "pos": ""},
            {"word": "exception", "phonetic": "", "meaning": "例外", "pos": ""},
            {"word": "fellow", "phonetic": "", "meaning": "同事、同辈", "pos": ""},
            {"word": "found", "phonetic": "", "meaning": "创立、建立", "pos": ""},
            {"word": "helicopter", "phonetic": "", "meaning": "直升机", "pos": ""},
            {"word": "incident", "phonetic": "", "meaning": "事件", "pos": ""},
            {"word": "keen", "phonetic": "", "meaning": "热忱的", "pos": ""},
            {"word": "occupation", "phonetic": "", "meaning": "占领、职业", "pos": ""},
        ]
    },
    "unit_91": {
        "name": "CET4词汇 第91单元",
        "words": [
            {"word": "permit", "phonetic": "", "meaning": "允许", "pos": ""},
            {"word": "stretch", "phonetic": "", "meaning": "伸展、延伸", "pos": ""},
            {"word": "theft", "phonetic": "", "meaning": "偷窃", "pos": ""},
            {"word": "admire", "phonetic": "", "meaning": "钦佩、羡慕、欣赏", "pos": ""},
            {"word": "anxious", "phonetic": "", "meaning": "焦虑的", "pos": ""},
            {"word": "compensate", "phonetic": "", "meaning": "补偿", "pos": ""},
            {"word": "generous", "phonetic": "", "meaning": "慷慨的", "pos": ""},
            {"word": "guard", "phonetic": "", "meaning": "保卫", "pos": ""},
            {"word": "honest", "phonetic": "", "meaning": "诚实的", "pos": ""},
            {"word": "inner", "phonetic": "", "meaning": "内部的、内心的", "pos": ""},
            {"word": "lean", "phonetic": "", "meaning": "瘦的、贫瘠的", "pos": ""},
            {"word": "marine", "phonetic": "", "meaning": "海的、船舶的", "pos": ""},
            {"word": "resist", "phonetic": "", "meaning": "抵挡、抵抗", "pos": ""},
            {"word": "restrict", "phonetic": "", "meaning": "限制", "pos": ""},
            {"word": "shoulder", "phonetic": "", "meaning": "肩膀", "pos": ""},
            {"word": "sky", "phonetic": "", "meaning": "天空", "pos": ""},
            {"word": "supreme", "phonetic": "", "meaning": "最高的、最优的", "pos": ""},
            {"word": "thin", "phonetic": "", "meaning": "薄的、稀薄的", "pos": ""},
            {"word": "angry", "phonetic": "", "meaning": "生气的", "pos": ""},
            {"word": "collapse", "phonetic": "", "meaning": "倒塌", "pos": ""},
        ]
    },
    "unit_92": {
        "name": "CET4词汇 第92单元",
        "words": [
            {"word": "consult", "phonetic": "", "meaning": "咨询", "pos": ""},
            {"word": "controversy", "phonetic": "", "meaning": "争论", "pos": ""},
            {"word": "flat", "phonetic": "", "meaning": "水平的、公寓", "pos": ""},
            {"word": "freeze", "phonetic": "", "meaning": "冻结", "pos": ""},
            {"word": "frequent", "phonetic": "", "meaning": "常常", "pos": ""},
            {"word": "insect", "phonetic": "", "meaning": "昆虫", "pos": ""},
            {"word": "insight", "phonetic": "", "meaning": "洞察力", "pos": ""},
            {"word": "interrupt", "phonetic": "", "meaning": "中断、打断", "pos": ""},
            {"word": "lake", "phonetic": "", "meaning": "湖", "pos": ""},
            {"word": "lend", "phonetic": "", "meaning": "借出", "pos": ""},
            {"word": "metal", "phonetic": "", "meaning": "金属", "pos": ""},
            {"word": "modest", "phonetic": "", "meaning": "谦虚的", "pos": ""},
            {"word": "nearby", "phonetic": "", "meaning": "附近的", "pos": ""},
            {"word": "owe", "phonetic": "", "meaning": "欠、归因于", "pos": ""},
            {"word": "personnel", "phonetic": "", "meaning": "员工、人事部门", "pos": ""},
            {"word": "ray", "phonetic": "", "meaning": "光线、射线", "pos": ""},
            {"word": "resort", "phonetic": "", "meaning": "被迫采取、手段", "pos": ""},
            {"word": "venture", "phonetic": "", "meaning": "冒险、敢于", "pos": ""},
            {"word": "arouse", "phonetic": "", "meaning": "唤醒、激发", "pos": ""},
            {"word": "delight", "phonetic": "", "meaning": "高兴", "pos": ""},
        ]
    },
    "unit_93": {
        "name": "CET4词汇 第93单元",
        "words": [
            {"word": "diverse", "phonetic": "", "meaning": "多种多样的", "pos": ""},
            {"word": "feedback", "phonetic": "", "meaning": "反馈", "pos": ""},
            {"word": "fortune", "phonetic": "", "meaning": "命运、财产", "pos": ""},
            {"word": "genius", "phonetic": "", "meaning": "天才", "pos": ""},
            {"word": "sad", "phonetic": "", "meaning": "悲伤的", "pos": ""},
            {"word": "shake", "phonetic": "", "meaning": "摇", "pos": ""},
            {"word": "shall", "phonetic": "", "meaning": "将要", "pos": ""},
            {"word": "soft", "phonetic": "", "meaning": "软的", "pos": ""},
            {"word": "sophisticated", "phonetic": "", "meaning": "世故的、复杂的", "pos": ""},
            {"word": "square", "phonetic": "", "meaning": "正方形", "pos": ""},
            {"word": "theme", "phonetic": "", "meaning": "主题", "pos": ""},
            {"word": "victory", "phonetic": "", "meaning": "胜利", "pos": ""},
            {"word": "assure", "phonetic": "", "meaning": "使确信、担保", "pos": ""},
            {"word": "bury", "phonetic": "", "meaning": "埋", "pos": ""},
            {"word": "calm", "phonetic": "", "meaning": "冷静、镇定", "pos": ""},
            {"word": "classmate", "phonetic": "", "meaning": "同学", "pos": ""},
            {"word": "contemporary", "phonetic": "", "meaning": "同时代的、现代的", "pos": ""},
            {"word": "convention", "phonetic": "", "meaning": "会议", "pos": ""},
            {"word": "convert", "phonetic": "", "meaning": "转变", "pos": ""},
            {"word": "curious", "phonetic": "", "meaning": "好奇的", "pos": ""},
        ]
    },
    "unit_94": {
        "name": "CET4词汇 第94单元",
        "words": [
            {"word": "database", "phonetic": "", "meaning": "数据库", "pos": ""},
            {"word": "drought", "phonetic": "", "meaning": "旱灾", "pos": ""},
            {"word": "enterprise", "phonetic": "", "meaning": "企业、事业", "pos": ""},
            {"word": "fatal", "phonetic": "", "meaning": "致命的、宿命的", "pos": ""},
            {"word": "grand", "phonetic": "", "meaning": "宏伟的", "pos": ""},
            {"word": "horse", "phonetic": "", "meaning": "马", "pos": ""},
            {"word": "induce", "phonetic": "", "meaning": "引诱、引起", "pos": ""},
            {"word": "lobby", "phonetic": "", "meaning": "门廊", "pos": ""},
            {"word": "monkey", "phonetic": "", "meaning": "猴子", "pos": ""},
            {"word": "pool", "phonetic": "", "meaning": "池塘", "pos": ""},
            {"word": "portion", "phonetic": "", "meaning": "部分", "pos": ""},
            {"word": "prevail", "phonetic": "", "meaning": "流行、占优势", "pos": ""},
            {"word": "quantity", "phonetic": "", "meaning": "数量、数额", "pos": ""},
            {"word": "shed", "phonetic": "", "meaning": "棚", "pos": ""},
            {"word": "temporary", "phonetic": "", "meaning": "临时的", "pos": ""},
            {"word": "trick", "phonetic": "", "meaning": "诡计、技巧", "pos": ""},
            {"word": "wise", "phonetic": "", "meaning": "有智慧的、英明的", "pos": ""},
            {"word": "aircraft", "phonetic": "", "meaning": "航空器", "pos": ""},
            {"word": "ethic", "phonetic": "", "meaning": "伦理", "pos": ""},
            {"word": "external", "phonetic": "", "meaning": "外部的", "pos": ""},
        ]
    },
    "unit_95": {
        "name": "CET4词汇 第95单元",
        "words": [
            {"word": "forum", "phonetic": "", "meaning": "论坛", "pos": ""},
            {"word": "fossil", "phonetic": "", "meaning": "化石", "pos": ""},
            {"word": "lady", "phonetic": "", "meaning": "女士", "pos": ""},
            {"word": "luck", "phonetic": "", "meaning": "运气、好运", "pos": ""},
            {"word": "mouth", "phonetic": "", "meaning": "嘴", "pos": ""},
            {"word": "myth", "phonetic": "", "meaning": "神话", "pos": ""},
            {"word": "pocket", "phonetic": "", "meaning": "口袋", "pos": ""},
            {"word": "poll", "phonetic": "", "meaning": "投票", "pos": ""},
            {"word": "pride", "phonetic": "", "meaning": "自豪、自满", "pos": ""},
            {"word": "react", "phonetic": "", "meaning": "反应", "pos": ""},
            {"word": "retain", "phonetic": "", "meaning": "保留", "pos": ""},
            {"word": "roll", "phonetic": "", "meaning": "滚动、卷", "pos": ""},
            {"word": "slip", "phonetic": "", "meaning": "滑", "pos": ""},
            {"word": "soccer", "phonetic": "", "meaning": "足球", "pos": ""},
            {"word": "sympathy", "phonetic": "", "meaning": "同情", "pos": ""},
            {"word": "taxi", "phonetic": "", "meaning": "出租车", "pos": ""},
            {"word": "via", "phonetic": "", "meaning": "经过", "pos": ""},
            {"word": "academy", "phonetic": "", "meaning": "学院", "pos": ""},
            {"word": "accumulate", "phonetic": "", "meaning": "积累", "pos": ""},
            {"word": "bother", "phonetic": "", "meaning": "打扰", "pos": ""},
        ]
    },
    "unit_96": {
        "name": "CET4词汇 第96单元",
        "words": [
            {"word": "dean", "phonetic": "", "meaning": "教长、学监", "pos": ""},
            {"word": "defend", "phonetic": "", "meaning": "保卫、防守", "pos": ""},
            {"word": "dismiss", "phonetic": "", "meaning": "解散", "pos": ""},
            {"word": "gallon", "phonetic": "", "meaning": "加仑", "pos": ""},
            {"word": "intake", "phonetic": "", "meaning": "吸入", "pos": ""},
            {"word": "lonely", "phonetic": "", "meaning": "孤独地", "pos": ""},
            {"word": "overcome", "phonetic": "", "meaning": "克服", "pos": ""},
            {"word": "overlook", "phonetic": "", "meaning": "俯瞰、忽略", "pos": ""},
            {"word": "rail", "phonetic": "", "meaning": "栏杆、铁轨", "pos": ""},
            {"word": "reinforce", "phonetic": "", "meaning": "加强", "pos": ""},
            {"word": "roof", "phonetic": "", "meaning": "屋顶", "pos": ""},
            {"word": "supermarket", "phonetic": "", "meaning": "超级市场", "pos": ""},
            {"word": "thief", "phonetic": "", "meaning": "小偷", "pos": ""},
            {"word": "tutor", "phonetic": "", "meaning": "导师", "pos": ""},
            {"word": "unemployed", "phonetic": "", "meaning": "失业者", "pos": ""},
            {"word": "accompany", "phonetic": "", "meaning": "陪伴、为……伴奏", "pos": ""},
            {"word": "badly", "phonetic": "", "meaning": "糟糕、严重地、非常", "pos": ""},
            {"word": "casual", "phonetic": "", "meaning": "随意的", "pos": ""},
            {"word": "component", "phonetic": "", "meaning": "组成部分", "pos": ""},
            {"word": "cup", "phonetic": "", "meaning": "杯子", "pos": ""},
        ]
    },
    "unit_97": {
        "name": "CET4词汇 第97单元",
        "words": [
            {"word": "destination", "phonetic": "", "meaning": "目的地", "pos": ""},
            {"word": "distribute", "phonetic": "", "meaning": "分发、分配", "pos": ""},
            {"word": "dozen", "phonetic": "", "meaning": "一打", "pos": ""},
            {"word": "exceed", "phonetic": "", "meaning": "超过、越过", "pos": ""},
            {"word": "exclude", "phonetic": "", "meaning": "不包括", "pos": ""},
            {"word": "glance", "phonetic": "", "meaning": "一瞥", "pos": ""},
            {"word": "imitate", "phonetic": "", "meaning": "模仿、仿造", "pos": ""},
            {"word": "implement", "phonetic": "", "meaning": "实施、工具", "pos": ""},
            {"word": "integrate", "phonetic": "", "meaning": "整合", "pos": ""},
            {"word": "intense", "phonetic": "", "meaning": "强烈的、热烈的", "pos": ""},
            {"word": "intensive", "phonetic": "", "meaning": "密集的", "pos": ""},
            {"word": "load", "phonetic": "", "meaning": "装货、装载", "pos": ""},
            {"word": "lock", "phonetic": "", "meaning": "锁", "pos": ""},
            {"word": "occupy", "phonetic": "", "meaning": "占据", "pos": ""},
            {"word": "orient", "phonetic": "", "meaning": "东方、适应", "pos": ""},
            {"word": "pension", "phonetic": "", "meaning": "养老金", "pos": ""},
            {"word": "phase", "phonetic": "", "meaning": "阶段", "pos": ""},
            {"word": "railway", "phonetic": "", "meaning": "铁路", "pos": ""},
            {"word": "revise", "phonetic": "", "meaning": "修改", "pos": ""},
            {"word": "shelf", "phonetic": "", "meaning": "架子", "pos": ""},
        ]
    },
    "unit_98": {
        "name": "CET4词汇 第98单元",
        "words": [
            {"word": "sink", "phonetic": "", "meaning": "下沉", "pos": ""},
            {"word": "storm", "phonetic": "", "meaning": "风暴", "pos": ""},
            {"word": "straight", "phonetic": "", "meaning": "直接的", "pos": ""},
            {"word": "arrest", "phonetic": "", "meaning": "逮捕", "pos": ""},
            {"word": "celebrate", "phonetic": "", "meaning": "庆祝", "pos": ""},
            {"word": "clerk", "phonetic": "", "meaning": "职员", "pos": ""},
            {"word": "command", "phonetic": "", "meaning": "命令", "pos": ""},
            {"word": "commodity", "phonetic": "", "meaning": "商品", "pos": ""},
            {"word": "compromise", "phonetic": "", "meaning": "妥协", "pos": ""},
            {"word": "dictionary", "phonetic": "", "meaning": "词典", "pos": ""},
            {"word": "endure", "phonetic": "", "meaning": "忍受、持久", "pos": ""},
            {"word": "hate", "phonetic": "", "meaning": "讨厌", "pos": ""},
            {"word": "hazard", "phonetic": "", "meaning": "危险", "pos": ""},
            {"word": "humor", "phonetic": "", "meaning": "幽默、诙谐", "pos": ""},
            {"word": "immune", "phonetic": "", "meaning": "免疫", "pos": ""},
            {"word": "joint", "phonetic": "", "meaning": "共同的、关节", "pos": ""},
            {"word": "jury", "phonetic": "", "meaning": "陪审团", "pos": ""},
            {"word": "knit", "phonetic": "", "meaning": "编织、针织", "pos": ""},
            {"word": "magic", "phonetic": "", "meaning": "魔法", "pos": ""},
            {"word": "motion", "phonetic": "", "meaning": "动、提议", "pos": ""},
        ]
    },
    "unit_99": {
        "name": "CET4词汇 第99单元",
        "words": [
            {"word": "negotiate", "phonetic": "", "meaning": "谈判、协商", "pos": ""},
            {"word": "norm", "phonetic": "", "meaning": "规范", "pos": ""},
            {"word": "numerous", "phonetic": "", "meaning": "许多的", "pos": ""},
            {"word": "shoot", "phonetic": "", "meaning": "射击", "pos": ""},
            {"word": "song", "phonetic": "", "meaning": "歌曲", "pos": ""},
            {"word": "span", "phonetic": "", "meaning": "跨度", "pos": ""},
            {"word": "abstract", "phonetic": "", "meaning": "抽象的、摘要", "pos": ""},
            {"word": "automobile", "phonetic": "", "meaning": "汽车", "pos": ""},
            {"word": "biology", "phonetic": "", "meaning": "生物学", "pos": ""},
            {"word": "calculate", "phonetic": "", "meaning": "计算", "pos": ""},
            {"word": "dish", "phonetic": "", "meaning": "碟子", "pos": ""},
            {"word": "distract", "phonetic": "", "meaning": "使转向、使分心", "pos": ""},
            {"word": "enemy", "phonetic": "", "meaning": "敌人", "pos": ""},
            {"word": "faith", "phonetic": "", "meaning": "信心、信仰", "pos": ""},
            {"word": "grasp", "phonetic": "", "meaning": "抓住", "pos": ""},
            {"word": "lane", "phonetic": "", "meaning": "小路、泳道", "pos": ""},
            {"word": "lift", "phonetic": "", "meaning": "提起", "pos": ""},
            {"word": "map", "phonetic": "", "meaning": "地图", "pos": ""},
            {"word": "motivate", "phonetic": "", "meaning": "激发", "pos": ""},
            {"word": "parliament", "phonetic": "", "meaning": "原谅、国会", "pos": ""},
        ]
    },
    "unit_100": {
        "name": "CET4词汇 第100单元",
        "words": [
            {"word": "passion", "phonetic": "", "meaning": "热情", "pos": ""},
            {"word": "penalty", "phonetic": "", "meaning": "处罚", "pos": ""},
            {"word": "pet", "phonetic": "", "meaning": "宠物", "pos": ""},
            {"word": "rescue", "phonetic": "", "meaning": "拯救", "pos": ""},
            {"word": "rid", "phonetic": "", "meaning": "摆脱", "pos": ""},
            {"word": "shock", "phonetic": "", "meaning": "震惊", "pos": ""},
            {"word": "strive", "phonetic": "", "meaning": "努力、斗争", "pos": ""},
            {"word": "sudden", "phonetic": "", "meaning": "突然的", "pos": ""},
            {"word": "tooth", "phonetic": "", "meaning": "牙齿", "pos": ""},
            {"word": "upper", "phonetic": "", "meaning": "上面的", "pos": ""},
            {"word": "yesterday", "phonetic": "", "meaning": "昨天", "pos": ""},
            {"word": "alike", "phonetic": "", "meaning": "与…相似", "pos": ""},
            {"word": "alive", "phonetic": "", "meaning": "活着的", "pos": ""},
            {"word": "bomb", "phonetic": "", "meaning": "炸弹", "pos": ""},
            {"word": "bore", "phonetic": "", "meaning": "使厌烦、钻孔", "pos": ""},
            {"word": "chart", "phonetic": "", "meaning": "图表", "pos": ""},
            {"word": "cloud", "phonetic": "", "meaning": "云", "pos": ""},
            {"word": "compose", "phonetic": "", "meaning": "组成、作曲、撰写", "pos": ""},
            {"word": "cream", "phonetic": "", "meaning": "奶油", "pos": ""},
            {"word": "endanger", "phonetic": "", "meaning": "危及", "pos": ""},
        ]
    },
}

# ============================================================
# 伪装输出引擎（CamouflageEngine）
# 让框框在背单词时看起来像在干正事
# ============================================================
class CamouflageEngine:
    """
    伪装输出引擎 - 生成看起来像系统运维的假日志
    使用暗淡绿色输出，不影响主要学习内容
    """
    
    def __init__(self):
        self.last_type = None
        self._pid_pool = list(range(1000, 9999))
        random.shuffle(self._pid_pool)
        self._pid_idx = 0
    
    def _timestamp(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def _random_pid(self) -> int:
        self._pid_idx = (self._pid_idx + 1) % len(self._pid_pool)
        return self._pid_pool[self._pid_idx]
    
    def _random_ip(self) -> str:
        return f"10.157.{random.randint(200, 230)}.{random.randint(1, 254)}"
    
    def _print_dim(self, text: str):
        print(f"{Colors.HACKER_DIM}{text}{ANSI.RESET}")
    
    def generate(self):
        """随机生成一段伪装输出"""
        output_types = [
            self._gen_system_log,
            self._gen_database,
            self._gen_network,
            self._gen_deployment,
            self._gen_monitoring,
            self._gen_energy_system,
        ]
        # 避免连续重复
        available = [t for t in output_types if t != self.last_type]
        chosen = random.choice(available)
        self.last_type = chosen
        chosen()
    
    def _gen_system_log(self):
        templates = [
            [
                f"[{self._timestamp()}] GET /api/v2/sensor/boiler_03 200 12ms",
                f"[{self._timestamp()}] POST /api/energy/data/sync 200 45ms",
                f"[{self._timestamp()}] daemon[{self._random_pid()}]: gas_flow_rate=234.5m³/h threshold_check=OK",
            ],
            [
                f"[{self._timestamp()}] systemd[1]: energy-monitor.service: Reloaded",
                f"[{self._timestamp()}] systemd[{self._random_pid()}]: Started EMS Data Collector.",
                f"[{self._timestamp()}] energy-collector: Batch sync completed, 128 records",
            ],
            [
                f"[{self._timestamp()}] nginx[{self._random_pid()}]: {self._random_ip()} - - [GET] /health 200",
                f"[{self._timestamp()}] postgres[{self._random_pid()}]: checkpoint starting: time",
                f"[{self._timestamp()}] redis[{self._random_pid()}]: DB saved on disk with RDB",
            ],
            [
                f"[{self._timestamp()}] kernel: [UFW BLOCK] IN=eth0 SRC={self._random_ip()} DST=10.157.220.166",
                f"[{self._timestamp()}] kernel: EXT4-fs: mounted filesystem with ordered data mode",
            ],
            [
                f"[{self._timestamp()}] sshd[{self._random_pid()}]: Accepted publickey for admin",
                f"[{self._timestamp()}] sudo: pam_unix(sudo:session): session opened for user root",
            ],
        ]
        for line in random.choice(templates):
            self._print_dim(line)
    
    def _gen_database(self):
        templates = [
            [
                f"$ psql -h {self._random_ip()} -U ems_user -d energy_db",
                f"ems_db=# SELECT * FROM sensor_data WHERE timestamp > NOW() - INTERVAL '1 hour';",
                f"50 rows in set (0.034 sec)",
            ],
            [
                f"$ mysql -h {self._random_ip()} -u ems_monitor ems_db",
                f"mysql> SELECT device_id, AVG(value) FROM power_readings GROUP BY device_id;",
                f"10 rows in set (0.021 sec)",
            ],
            [
                f"$ pg_dump -h {self._random_ip()} -U ems_user -Fc ems_db > backup_{time.strftime('%Y%m%d')}.dump",
                f"[{self._timestamp()}] Backup completed: 2.3GB compressed",
            ],
            [
                f"ems_db=# ANALYZE VERBOSE sensor_data;",
                f'INFO: analyzing "public"."sensor_data"',
                f"INFO: ANALYZE complete",
            ],
            [
                f"$ redis-cli -h {self._random_ip()} -p 6379",
                f"redis> KEYS *sensor*",
                f'1) "cache:boiler_03:data"',
                f'2) "cache:power:realtime"',
            ],
        ]
        for line in random.choice(templates):
            self._print_dim(line)
    
    def _gen_network(self):
        templates = [
            [
                f"$ ping -c 3 10.157.220.166",
                f"64 bytes from 10.157.220.166: icmp_seq=1 ttl=64 time=0.342 ms",
                f"3 packets transmitted, 3 received, 0% packet loss",
            ],
            [
                f"$ netstat -tuln | grep LISTEN",
                f"tcp  0  0 0.0.0.0:22    0.0.0.0:*  LISTEN",
                f"tcp  0  0 0.0.0.0:80    0.0.0.0:*  LISTEN",
                f"tcp  0  0 0.0.0.0:3306  0.0.0.0:*  LISTEN",
            ],
            [
                f"$ nmap -sV -p 22,80,443 10.157.220.166",
                f"PORT    STATE  SERVICE  VERSION",
                f"22/tcp  open   ssh      OpenSSH 8.9",
                f"80/tcp  open   http     nginx 1.22",
            ],
            [
                f"$ sudo iptables -L -n -v",
                f"Chain INPUT (policy ACCEPT 0 packets, 0 bytes)",
                f" 234  12345 ACCEPT  all  --  *  *  10.157.220.0/24  0.0.0.0/0",
            ],
            [
                f"$ curl -s http://10.157.220.166:8080/health",
                f'{{"status":"UP","components":{{"db":"UP","redis":"UP"}}}}',
            ],
        ]
        for line in random.choice(templates):
            self._print_dim(line)
    
    def _gen_deployment(self):
        templates = [
            [
                f"$ docker ps --format 'table {{{{.Names}}}}\\t{{{{.Status}}}}'",
                f"NAMES              STATUS",
                f"ems-collector      Up 2 days",
                f"nginx-proxy        Up 5 days",
                f"postgres-emis      Up 1 week",
            ],
            [
                f"$ git status",
                f"On branch main",
                f"  modified:   src/monitor.py",
                f"$ git add . && git commit -m 'fix: sensor polling interval'",
                f"[main abc1234] fix: sensor polling interval",
            ],
            [
                f"$ pip install -r requirements.txt",
                f"Requirement already satisfied: requests==2.31.0",
                f"Collecting pymongo==4.6.0",
                f"Successfully installed pymongo-4.6.0",
            ],
            [
                f"$ kubectl get pods -n ems-prod",
                f"NAME                       READY   STATUS    RESTARTS   AGE",
                f"collector-7d8f9b-xk2p9    1/1     Running   0          3d",
                f"api-server-5c4d6e-f8h7k   1/1     Running   0          5d",
            ],
        ]
        for line in random.choice(templates):
            self._print_dim(line)
    
    def _gen_monitoring(self):
        cpu = random.randint(5, 45)
        mem = random.randint(200, 800)
        disk = random.randint(40, 85)
        templates = [
            [
                f"$ top -bn1 | head -5",
                f"top - {time.strftime('%H:%M:%S')} up 127 days, load average: 0.{random.randint(10,99)}, 0.{random.randint(10,50)}, 0.{random.randint(10,30)}",
                f"Tasks: {random.randint(80,150)} total, {random.randint(1,3)} running, {random.randint(70,140)} sleeping",
                f"%Cpu(s): {cpu}% us, {random.randint(1,5)}% sy, 0.0% ni, {100-cpu-random.randint(1,5)}% id",
                f"MiB Mem:  {random.randint(3000,8000)}.0 total, {random.randint(500,3000)}.0 free, {mem}.0 used",
            ],
            [
                f"$ df -h /dev/sda1",
                f"Filesystem  Size  Used  Avail  Use%  Mounted on",
                f"/dev/sda1   50G   {disk*50//100}G   {50-disk*50//100}G   {disk}%  /",
            ],
            [
                f"$ free -h",
                f"              total    used    free    shared  buff/cache   available",
                f"Mem:          7.8Gi   {mem/1024:.1f}Gi   {(8000-mem)/1024:.1f}Gi   256Mi     1.2Gi        4.5Gi",
            ],
            [
                f"[{self._timestamp()}] monitor: CPU={cpu}% MEM={mem}MB DISK={disk}% STATUS=OK",
                f"[{self._timestamp()}] alert: threshold check passed for all services",
            ],
        ]
        for line in random.choice(templates):
            self._print_dim(line)
    
    def _gen_energy_system(self):
        """能管系统专属伪装 - 最贴合框框工作"""
        gas_flow = round(random.uniform(100, 500), 1)
        boiler_temp = random.randint(150, 350)
        power_kw = round(random.uniform(500, 2000), 1)
        pressure = round(random.uniform(0.5, 2.5), 2)
        templates = [
            [
                f"[{self._timestamp()}] EMS[{self._random_pid()}]: gas_flow={gas_flow}m³/h status=NORMAL",
                f"[{self._timestamp()}] EMS[{self._random_pid()}]: boiler_temp={boiler_temp}°C threshold={350}°C OK",
                f"[{self._timestamp()}] EMS[{self._random_pid()}]: power_load={power_kw}kW peak_ratio={round(power_kw/2000*100,1)}%",
            ],
            [
                f"[{self._timestamp()}] sensor_collect: 10.157.220.166/api/data -> 200 OK (128ms)",
                f"[{self._timestamp()}] sensor_collect: boiler_03 temp={boiler_temp}°C pressure={pressure}MPa",
                f"[{self._timestamp()}] sensor_collect: power_meter_07 reading={power_kw}kW status=ONLINE",
            ],
            [
                f"$ curl -s http://10.157.220.166/DLNGEMS/api/realtime",
                f'{{"gas_flow":{gas_flow},"boiler_temp":{boiler_temp},"power":{power_kw},"status":"normal"}}',
            ],
            [
                f"[{self._timestamp()}] EMS巡检: 天然气流量={gas_flow}m³/h 锅炉温度={boiler_temp}°C",
                f"[{self._timestamp()}] EMS巡检: 电力负荷={power_kw}kW 压力={pressure}MPa",
                f"[{self._timestamp()}] EMS巡检: 所有传感器在线，数据正常",
            ],
            [
                f"[{self._timestamp()}] cron[{self._random_pid()}]: EMS每日巡检任务启动",
                f"[{self._timestamp()}] cron: 检查 {random.randint(30,60)} 个传感器节点...",
                f"[{self._timestamp()}] cron: 巡检完成，{random.randint(28,60)}/{random.randint(30,60)} 在线",
            ],
        ]
        for line in random.choice(templates):
            self._print_dim(line)

# ============================================================
# 数据文件管理
# ============================================================
class DataManager:
    """管理错题本和学习进度"""
    
    def __init__(self):
        self.error_file = ".vocab_errors.json"
        self.progress_file = ".vocab_progress.json"
    
    def load_errors(self) -> List[Dict]:
        """加载错题本"""
        try:
            if os.path.exists(self.error_file):
                with open(self.error_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def save_errors(self, errors: List[Dict]):
        """保存错题本"""
        try:
            with open(self.error_file, 'w', encoding='utf-8') as f:
                json.dump(errors, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def add_error(self, word_data: Dict, user_answer: str):
        """添加错题"""
        errors = self.load_errors()
        # 检查是否已存在
        for item in errors:
            if item['word'] == word_data['word']:
                item['wrong_count'] = item.get('wrong_count', 0) + 1
                item['last_wrong'] = time.strftime("%Y-%m-%d %H:%M")
                break
        else:
            errors.append({
                'word': word_data['word'],
                'phonetic': word_data['phonetic'],
                'meaning': word_data['meaning'],
                'pos': word_data['pos'],
                'user_answer': user_answer,
                'wrong_count': 1,
                'last_wrong': time.strftime("%Y-%m-%d %H:%M")
            })
        self.save_errors(errors)
    
    def remove_error(self, word: str):
        """移除错题（答对后）"""
        errors = self.load_errors()
        errors = [e for e in errors if e['word'] != word]
        self.save_errors(errors)
    
    def load_progress(self) -> Dict:
        """加载学习进度"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            'total_score': 0,
            'learned_words': [],
            'mastered_words': [],
            'total_correct': 0,
            'total_wrong': 0,
            'streak_record': 0
        }
    
    def save_progress(self, progress: Dict):
        """保存学习进度"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

# ============================================================
# 终端界面
# ============================================================
class Terminal:
    """终端界面控制"""
    
    @staticmethod
    def clear():
        """跨平台清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_hacker(text: str, bold: bool = True):
        """打印黑客风格文字"""
        style = Colors.HACKER_GREEN if bold else Colors.HACKER_DIM
        print(f"{style}{text}{ANSI.RESET}")
    
    @staticmethod
    def print_error(text: str):
        """打印错误信息"""
        print(f"{Colors.ERROR_RED}{text}{ANSI.RESET}")
    
    @staticmethod
    def print_success(text: str):
        """打印成功信息"""
        print(f"{Colors.SUCCESS_GREEN}{text}{ANSI.RESET}")
    
    @staticmethod
    def print_warning(text: str):
        """打印警告信息"""
        print(f"{Colors.WARNING_YELLOW}{text}{ANSI.RESET}")
    
    @staticmethod
    def print_info(text: str):
        """打印提示信息"""
        print(f"{Colors.INFO_CYAN}{text}{ANSI.RESET}")
    
    @staticmethod
    def print_prompt():
        """打印提示符"""
        print(f"{Colors.PROMPT_MAGENTA}root@vocab:~${ANSI.RESET} ", end='')
    
    @staticmethod
    def loading_animation(duration: float = 2.0, steps: int = 20):
        """启动加载动画"""
        Terminal.clear()
        print(f"{Colors.HACKER_GREEN}{ASCII_TITLE}{ANSI.RESET}")
        print(f"{Colors.HACKER_DIM}[系统启动中...]{ANSI.RESET}")
        print()
        
        # 模拟加载进度
        chars = '█'
        for i in range(steps + 1):
            progress = i / steps
            bar_len = int(40 * progress)
            bar = chars * bar_len + '░' * (40 - bar_len)
            percent = int(100 * progress)
            
            # 模拟加载日志
            logs = [
                "[加载词库...]",
                "[初始化系统...]",
                "[加载错题本...]",
                "[校验数据完整性...]",
                "[系统就绪]"
            ]
            log_idx = min(int(progress * len(logs)), len(logs) - 1)
            
            # \r 回到行首，不换行
            print(f"\r{Colors.HACKER_GREEN}[{bar}]{ANSI.RESET} {percent}% {Colors.HACKER_DIM}{logs[log_idx]}{ANSI.RESET}", end='', flush=True)
            time.sleep(duration / steps)
        
        print()
        print()
        input(f"{Colors.HACKER_DIM}[按 Enter 键继续...]{ANSI.RESET}")
    
    @staticmethod
    def print_divider(char: str = "=", length: int = 60):
        """打印分隔线"""
        print(f"{Colors.HACKER_GREEN}{char * length}{ANSI.RESET}")
    
    @staticmethod
    def print_header(title: str):
        """打印标题"""
        Terminal.print_divider()
        print(f"{Colors.HACKER_GREEN}{Colors.BOLD}{title.center(58)}{ANSI.RESET}")
        Terminal.print_divider()

# ============================================================
# 答题匹配逻辑
# ============================================================
class AnswerMatcher:
    """答案匹配器"""
    
    @staticmethod
    def normalize(text: str) -> str:
        """标准化文本：转小写，去除标点空格"""
        text = text.lower().strip()
        # 去除标点符号
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        return text
    
    @staticmethod
    def check_spelling(user_answer: str, correct_word: str) -> bool:
        """检查拼写是否正确（严格匹配）"""
        return AnswerMatcher.normalize(user_answer) == AnswerMatcher.normalize(correct_word)
    
    @staticmethod
    def check_meaning(user_answer: str, correct_meaning: str) -> bool:
        """检查中文释义（模糊匹配：关键词匹配）"""
        user_norm = AnswerMatcher.normalize(user_answer)
        correct_norm = AnswerMatcher.normalize(correct_meaning)
        
        # 完全匹配
        if user_norm == correct_norm:
            return True
        
        # 检查用户输入是否包含正确答案的所有关键词
        # 或者正确答案是否包含用户输入
        correct_words = set(correct_norm.replace('，', ',').split(','))
        correct_words = {w.strip() for w in correct_words if w.strip()}
        
        user_words = set(user_norm.split())
        
        # 如果用户输入过短（少于2个字），不匹配
        if len(user_norm) < 2:
            return False
        
        # 计算交集
        matched = 0
        for cw in correct_words:
            for uw in user_words:
                if cw in uw or uw in cw:
                    matched += 1
                    break
        
        # 至少匹配一个关键词
        if matched >= 1 and matched >= len(correct_words) * 0.5:
            return True
        
        # 简单包含检查
        if user_norm in correct_norm or correct_norm in user_norm:
            return True
        
        return False

# ============================================================
# 积分系统
# ============================================================
class ScoreSystem:
    """积分管理系统"""
    
    def __init__(self):
        self.base_score = 10
        self.streak_bonus = {
            3: 5,    # 3连击 +5
            5: 10,   # 5连击 +10
            10: 20,  # 10连击 +20
            20: 50,  # 20连击 +50
            50: 100  # 50连击 +100
        }
    
    def calculate_score(self, streak: int) -> int:
        """计算本次得分"""
        score = self.base_score
        
        # 查找连击奖励
        for threshold, bonus in sorted(self.streak_bonus.items(), reverse=True):
            if streak >= threshold:
                score += bonus
                break
        
        return score
    
    def get_streak_bonus_info(self, streak: int) -> str:
        """获取连击奖励提示"""
        for threshold, bonus in sorted(self.streak_bonus.items(), reverse=True):
            if streak >= threshold:
                if streak == threshold:
                    return f" 🎯 {threshold}连击奖励 +{bonus}!"
                elif streak > threshold:
                    return f" 🔥 当前{streak}连击!"
        return ""

# ============================================================
# 学习引擎
# ============================================================
class LearningEngine:
    """学习引擎"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.score_system = ScoreSystem()
        self.camouflage = CamouflageEngine()
        self.progress = self.data_manager.load_progress()
    
    def get_all_words(self) -> List[Dict]:
        """获取所有词汇"""
        all_words = []
        for unit in VOCABULARY.values():
            all_words.extend(unit['words'])
        return all_words
    
    def get_unit_words(self, unit_key: str) -> List[Dict]:
        """获取指定单元词汇"""
        if unit_key in VOCABULARY:
            return VOCABULARY[unit_key]['words']
        return []
    
    def get_random_words(self, count: int = 20, exclude: List[str] = None) -> List[Dict]:
        """获取随机词汇"""
        all_words = self.get_all_words()
        if exclude:
            all_words = [w for w in all_words if w['word'] not in exclude]
        return random.sample(all_words, min(count, len(all_words)))
    
    def get_error_words(self) -> List[Dict]:
        """获取错题词汇"""
        return self.data_manager.load_errors()
    
    def update_progress(self, correct: bool, word: str = None):
        """更新学习进度"""
        if correct:
            self.progress['total_correct'] += 1
            if word and word not in self.progress['learned_words']:
                self.progress['learned_words'].append(word)
        else:
            self.progress['total_wrong'] += 1
        
        self.data_manager.save_progress(self.progress)
    
    def add_score(self, score: int):
        """添加积分"""
        self.progress['total_score'] += score
        if score > 0:
            self.progress['streak_record'] = max(
                self.progress.get('streak_record', 0),
                self.progress.get('current_streak', 0)
            )
        self.data_manager.save_progress(self.progress)
    
    def show_stats(self):
        """显示统计面板"""
        Terminal.print_header("📊 学习统计")
        
        total = self.progress['total_correct'] + self.progress['total_wrong']
        accuracy = (self.progress['total_correct'] / total * 100) if total > 0 else 0
        
        errors = self.data_manager.load_errors()
        
        print(f"""
{Colors.HACKER_GREEN}┌──────────────────────────────────────┐
│  📈 累计正确率: {accuracy:5.1f}%                 │
│  ✅ 答对题数:   {self.progress['total_correct']:>5}                    │
│  ❌ 答错题数:   {self.progress['total_wrong']:>5}                    │
│  📚 已学词汇:   {len(self.progress['learned_words']):>5}                    │
│  💰 当前积分:   {self.progress['total_score']:>5}                    │
│  📝 错题本:     {len(errors):>5} 道错题待复习            │
└──────────────────────────────────────┘{ANSI.RESET}
""")
        
        if errors:
            print(f"{Colors.WARNING_YELLOW}⚠️  错题本中有 {len(errors)} 道错题，建议使用复习模式{ANSI.RESET}")
        print()

# ============================================================
# 学习模式
# ============================================================
class LearnMode:
    """认词模式：显示英文单词，用户输入中文释义"""
    
    def __init__(self, engine: LearningEngine):
        self.engine = engine
        self.score_system = engine.score_system
        self.streak = 0
        self.unit_correct = 0
        self.unit_total = 0
    
    def run(self, unit_key: str = None):
        """运行认词模式"""
        # 选择词汇
        if unit_key and unit_key in VOCABULARY:
            words = VOCABULARY[unit_key]['words'].copy()
            unit_name = VOCABULARY[unit_key]['name']
        else:
            words = self.engine.get_random_words(20)
            unit_name = "随机练习"
        
        random.shuffle(words)
        
        Terminal.clear()
        Terminal.print_header(f"📖 认词模式 - {unit_name}")
        print(f"{Colors.HACKER_DIM}显示英文单词，输入中文释义。按 quit 返回菜单。{ANSI.RESET}\n")
        
        for word_data in words:
            self.show_question(word_data)
            
            user_input = input().strip()
            
            # 处理命令
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'skip':
                self.engine.update_progress(False)
                continue
            elif user_input.lower() == 'stats':
                self.engine.show_stats()
                print(f"{Colors.HACKER_DIM}继续当前练习...{ANSI.RESET}\n")
                continue
            
            # 检查答案
            correct = AnswerMatcher.check_meaning(user_input, word_data['meaning'])
            self.process_answer(correct, word_data, user_input)
            
            self.unit_total += 1
        
        self.show_unit_summary()
    
    def show_question(self, word_data: Dict):
        """显示题目"""
        print(f"{Colors.HACKER_GREEN}{Colors.BOLD}")
        print(f"┌────────────────────────────────────────┐")
        print(f"│  {word_data['word']:^20}  {word_data['phonetic']:<20}│")
        print(f"│  [{word_data['pos']:<6}]                              │")
        print(f"└────────────────────────────────────────┘")
        print(f"{ANSI.RESET}")
        Terminal.print_prompt()
    
    def process_answer(self, correct: bool, word_data: Dict, user_input: str):
        """处理答案"""
        self.streak = self.streak + 1 if correct else 0
        self.engine.progress['current_streak'] = self.streak
        
        if correct:
            self.unit_correct += 1
            score = self.score_system.calculate_score(self.streak)
            self.engine.add_score(score)
            self.engine.update_progress(True, word_data['word'])
            self.engine.data_manager.remove_error(word_data['word'])
            
            bonus_info = self.score_system.get_streak_bonus_info(self.streak)
            print()
            print(f"{Colors.SUCCESS_GREEN}✓ 正确! {bonus_info} +{score}分{ANSI.RESET}")
        else:
            self.engine.update_progress(False)
            self.engine.data_manager.add_error(word_data, user_input)
            
            print()
            print(f"{Colors.ERROR_RED}✗ 错误!{ANSI.RESET}")
            print(f"{Colors.WARNING_YELLOW}正确答案: {word_data['meaning']}{ANSI.RESET}")
        
        print()
        # v5.0: 伪装输出
        self.engine.camouflage.generate()
        print()
    
    def show_unit_summary(self):
        """显示单元成绩"""
        accuracy = (self.unit_correct / self.unit_total * 100) if self.unit_total > 0 else 0
        
        Terminal.print_header("📋 本轮成绩")
        print(f"""
{Colors.HACKER_GREEN}┌──────────────────────────────────────┐
│  本轮正确率: {accuracy:5.1f}%                   │
│  答对题数:   {self.unit_correct:>5}/{self.unit_total:<5}                    │
│  连击记录:   {self.streak:>5}                    │
└──────────────────────────────────────┘{ANSI.RESET}
""")
        
        if accuracy >= 90:
            print(f"{Colors.SUCCESS_GREEN}🎉 太棒了！继续保持！{ANSI.RESET}")
        elif accuracy >= 70:
            print(f"{Colors.INFO_CYAN}👍 不错，再接再厉！{ANSI.RESET}")
        else:
            print(f"{Colors.WARNING_YELLOW}💪 多复习错题，会有进步的！{ANSI.RESET}")
        
        print()


class SpellMode:
    """拼写模式：显示中文释义，用户拼写英文"""
    
    def __init__(self, engine: LearningEngine):
        self.engine = engine
        self.score_system = engine.score_system
        self.streak = 0
        self.unit_correct = 0
        self.unit_total = 0
    
    def run(self, unit_key: str = None):
        """运行拼写模式"""
        # 选择词汇
        if unit_key and unit_key in VOCABULARY:
            words = VOCABULARY[unit_key]['words'].copy()
            unit_name = VOCABULARY[unit_key]['name']
        else:
            words = self.engine.get_random_words(20)
            unit_name = "随机练习"
        
        random.shuffle(words)
        
        Terminal.clear()
        Terminal.print_header(f"⌨️  拼写模式 - {unit_name}")
        print(f"{Colors.HACKER_DIM}显示中文释义，输入英文单词拼写。按 quit 返回菜单。{ANSI.RESET}\n")
        
        for word_data in words:
            self.show_question(word_data)
            
            user_input = input().strip()
            
            # 处理命令
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'skip':
                self.engine.update_progress(False)
                continue
            elif user_input.lower() == 'stats':
                self.engine.show_stats()
                print(f"{Colors.HACKER_DIM}继续当前练习...{ANSI.RESET}\n")
                continue
            
            # 检查答案
            correct = AnswerMatcher.check_spelling(user_input, word_data['word'])
            self.process_answer(correct, word_data, user_input)
            
            self.unit_total += 1
        
        self.show_unit_summary()
    
    def show_question(self, word_data: Dict):
        """显示题目"""
        print(f"{Colors.HACKER_GREEN}{Colors.BOLD}")
        print(f"┌────────────────────────────────────────┐")
        print(f"│  {word_data['meaning']:<36}│")
        print(f"│  [{word_data['pos']:<6}]                              │")
        print(f"└────────────────────────────────────────┘")
        print(f"{ANSI.RESET}")
        Terminal.print_prompt()
    
    def process_answer(self, correct: bool, word_data: Dict, user_input: str):
        """处理答案"""
        self.streak = self.streak + 1 if correct else 0
        self.engine.progress['current_streak'] = self.streak
        
        if correct:
            self.unit_correct += 1
            score = self.score_system.calculate_score(self.streak)
            self.engine.add_score(score)
            self.engine.update_progress(True, word_data['word'])
            self.engine.data_manager.remove_error(word_data['word'])
            
            bonus_info = self.score_system.get_streak_bonus_info(self.streak)
            print()
            print(f"{Colors.SUCCESS_GREEN}✓ 正确! {bonus_info} +{score}分{ANSI.RESET}")
        else:
            self.engine.update_progress(False)
            self.engine.data_manager.add_error(word_data, user_input)
            
            print()
            print(f"{Colors.ERROR_RED}✗ 错误!{ANSI.RESET}")
            print(f"{Colors.WARNING_YELLOW}正确答案: {word_data['word']} {word_data['phonetic']}{ANSI.RESET}")
        
        print()
        # v5.0: 伪装输出
        self.engine.camouflage.generate()
        print()
    
    def show_unit_summary(self):
        """显示单元成绩"""
        accuracy = (self.unit_correct / self.unit_total * 100) if self.unit_total > 0 else 0
        
        Terminal.print_header("📋 本轮成绩")
        print(f"""
{Colors.HACKER_GREEN}┌──────────────────────────────────────┐
│  本轮正确率: {accuracy:5.1f}%                   │
│  答对题数:   {self.unit_correct:>5}/{self.unit_total:<5}                    │
│  连击记录:   {self.streak:>5}                    │
└──────────────────────────────────────┘{ANSI.RESET}
""")
        
        if accuracy >= 90:
            print(f"{Colors.SUCCESS_GREEN}🎉 拼写达人！继续保持！{ANSI.RESET}")
        elif accuracy >= 70:
            print(f"{Colors.INFO_CYAN}👍 不错，继续加油！{ANSI.RESET}")
        else:
            print(f"{Colors.WARNING_YELLOW}💪 多背单词，拼写会越来越好！{ANSI.RESET}")
        
        print()


class ReviewMode:
    """复习模式：从错题本中抽题"""
    
    def __init__(self, engine: LearningEngine):
        self.engine = engine
        self.score_system = engine.score_system
        self.streak = 0
        self.unit_correct = 0
        self.unit_total = 0
    
    def run(self):
        """运行复习模式"""
        error_words = self.engine.get_error_words()
        
        if not error_words:
            Terminal.clear()
            Terminal.print_header("📝 复习模式")
            print(f"""
{Colors.INFO_CYAN}✨ 太棒了！错题本已经是空的了！{ANSI.RESET}
{Colors.HACKER_DIM}继续保持，养成复习的好习惯。{ANSI.RESET}
""")
            input(f"{Colors.HACKER_DIM}[按 Enter 返回菜单...]{ANSI.RESET}")
            return
        
        # 随机选择复习题目
        review_count = min(len(error_words), 20)
        words = random.sample(error_words, review_count)
        
        Terminal.clear()
        Terminal.print_header(f"📝 复习模式 - {len(error_words)}道错题")
        print(f"{Colors.HACKER_DIM}从错题本中随机抽取 {review_count} 道进行复习。{ANSI.RESET}\n")
        
        for i, word_data in enumerate(words, 1):
            # 随机决定是认词还是拼写
            mode = random.choice(['learn', 'spell'])
            
            print(f"{Colors.HACKER_GREEN}--- 题目 {i}/{review_count} ---{ANSI.RESET}\n")
            
            if mode == 'learn':
                self.show_learn_question(word_data)
                user_input = input().strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'skip':
                    continue
                elif user_input.lower() == 'stats':
                    self.engine.show_stats()
                    print(f"{Colors.HACKER_DIM}继续当前复习...{ANSI.RESET}\n")
                    continue
                
                correct = AnswerMatcher.check_meaning(user_input, word_data['meaning'])
                self.process_answer(correct, word_data, user_input, mode)
            else:
                self.show_spell_question(word_data)
                user_input = input().strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'skip':
                    continue
                elif user_input.lower() == 'stats':
                    self.engine.show_stats()
                    print(f"{Colors.HACKER_DIM}继续当前复习...{ANSI.RESET}\n")
                    continue
                
                correct = AnswerMatcher.check_spelling(user_input, word_data['word'])
                self.process_answer(correct, word_data, user_input, mode)
            
            self.unit_total += 1
        
        self.show_unit_summary()
    
    def show_learn_question(self, word_data: Dict):
        """显示认词题目"""
        print(f"{Colors.HACKER_GREEN}{Colors.BOLD}")
        print(f"┌────────────────────────────────────────┐")
        print(f"│  {word_data['word']:^20}  {word_data['phonetic']:<20}│")
        print(f"│  [复习]                                │")
        print(f"└────────────────────────────────────────┘")
        print(f"{ANSI.RESET}")
        Terminal.print_prompt()
    
    def show_spell_question(self, word_data: Dict):
        """显示拼写题目"""
        print(f"{Colors.HACKER_GREEN}{Colors.BOLD}")
        print(f"┌────────────────────────────────────────┐")
        print(f"│  {word_data['meaning']:<36}│")
        print(f"│  [复习-拼写]                          │")
        print(f"└────────────────────────────────────────┘")
        print(f"{ANSI.RESET}")
        Terminal.print_prompt()
    
    def process_answer(self, correct: bool, word_data: Dict, user_input: str, mode: str):
        """处理答案"""
        self.streak = self.streak + 1 if correct else 0
        self.engine.progress['current_streak'] = self.streak
        
        if correct:
            self.unit_correct += 1
            score = self.score_system.calculate_score(self.streak) * 2  # 复习双倍积分
            self.engine.add_score(score)
            self.engine.update_progress(True, word_data['word'])
            self.engine.data_manager.remove_error(word_data['word'])
            
            bonus_info = self.score_system.get_streak_bonus_info(self.streak)
            print()
            print(f"{Colors.SUCCESS_GREEN}✓ 正确! {bonus_info} +{score}分 (复习双倍){ANSI.RESET}")
        else:
            self.engine.update_progress(False)
            self.engine.data_manager.add_error(word_data, user_input)
            
            print()
            print(f"{Colors.ERROR_RED}✗ 错误!{ANSI.RESET}")
            if mode == 'learn':
                print(f"{Colors.WARNING_YELLOW}正确答案: {word_data['meaning']}{ANSI.RESET}")
            else:
                print(f"{Colors.WARNING_YELLOW}正确答案: {word_data['word']} {word_data['phonetic']}{ANSI.RESET}")
        
        print()
        # v5.0: 伪装输出
        self.engine.camouflage.generate()
        print()
    
    def show_unit_summary(self):
        """显示复习成绩"""
        accuracy = (self.unit_correct / self.unit_total * 100) if self.unit_total > 0 else 0
        remaining_errors = len(self.engine.get_error_words())
        
        Terminal.print_header("📋 复习报告")
        print(f"""
{Colors.HACKER_GREEN}┌──────────────────────────────────────┐
│  本轮正确率: {accuracy:5.1f}%                   │
│  答对题数:   {self.unit_correct:>5}/{self.unit_total:<5}                    │
│  剩余错题:   {remaining_errors:>5} 道                   │
│  连击记录:   {self.streak:>5}                    │
└──────────────────────────────────────┘{ANSI.RESET}
""")
        
        if remaining_errors == 0:
            print(f"{Colors.SUCCESS_GREEN}🎉 太棒了！错题本已清空！{ANSI.RESET}")
        else:
            print(f"{Colors.WARNING_YELLOW}💪 还有 {remaining_errors} 道错题，继续加油！{ANSI.RESET}")
        
        print()


# ============================================================
# 主程序
# ============================================================
class VocabHacker:
    """主程序"""
    
    def __init__(self):
        self.engine = LearningEngine()
        self.learn_mode = LearnMode(self.engine)
        self.spell_mode = SpellMode(self.engine)
        self.review_mode = ReviewMode(self.engine)
    
    def show_menu(self):
        """显示主菜单"""
        Terminal.clear()
        Terminal.print_header("主菜单")
        
        errors = self.engine.get_error_words()
        error_count = len(errors)
        
        # 显示欢迎信息
        print(f"""
{Colors.HACKER_GREEN}
    ╔════════════════════════════════════════╗
    ║   VOCAB_HACKER - 终端背单词工具          ║
    ║   备战 CET-4  ·  黑客风格               ║
    ╚════════════════════════════════════════╝
{ANSI.RESET}
""")
        
        # 显示积分
        print(f"    {Colors.HACKER_GREEN}💰 积分: {self.engine.progress.get('total_score', 0)}{ANSI.RESET}")
        if error_count > 0:
            print(f"    {Colors.WARNING_YELLOW}⚠️  错题: {error_count} 道{ANSI.RESET}")
        print()
        
        # 菜单选项
        print(f"""    {Colors.INFO_CYAN}[1]{ANSI.RESET} 📖 认词模式 - 看英文，选中文
    {Colors.INFO_CYAN}[2]{ANSI.RESET} ⌨️  拼写模式 - 看中文，拼英文
    {Colors.INFO_CYAN}[3]{ANSI.RESET} 📝 复习模式 - 复习错题本 ({error_count}道)
    {Colors.INFO_CYAN}[4]{ANSI.RESET} 📊 查看统计
    {Colors.INFO_CYAN}[5]{ANSI.RESET} 📚 选择单元学习
    {Colors.INFO_CYAN}[0]{ANSI.RESET} 🚪 退出程序
""")
        
        Terminal.print_divider()
        print()
    
    def show_unit_menu(self):
        """显示单元选择菜单"""
        Terminal.clear()
        Terminal.print_header("选择学习单元")
        
        print(f"""    {Colors.INFO_CYAN}[0]{ANSI.RESET} 🚪 返回主菜单
""")
        
        for i, (key, unit) in enumerate(VOCABULARY.items(), 1):
            word_count = len(unit['words'])
            print(f"    {Colors.INFO_CYAN}[{i}]{ANSI.RESET} {unit['name']} ({word_count}词)")
        
        print()
        Terminal.print_divider()
        print()
        print(f"{Colors.HACKER_DIM}提示: 选择单元后可选择学习模式(认词/拼写){ANSI.RESET}\n")
    
    def show_unit_learning_menu(self, unit_key: str, unit_name: str):
        """显示单元学习模式选择"""
        Terminal.clear()
        Terminal.print_header(f"学习: {unit_name}")
        
        print(f"""
    {Colors.INFO_CYAN}[1]{ANSI.RESET} 📖 认词模式
    {Colors.INFO_CYAN}[2]{ANSI.RESET} ⌨️  拼写模式
    {Colors.INFO_CYAN}[0]{ANSI.RESET} 🚪 返回
""")
        Terminal.print_divider()
        print()
    
    def run(self):
        """运行主程序"""
        # 显示加载动画
        Terminal.loading_animation(2.0)
        
        while True:
            self.show_menu()
            Terminal.print_prompt()
            
            choice = input().strip()
            
            if choice == '0':
                self.exit_program()
                break
            elif choice == '1':
                self.learn_mode.run()
            elif choice == '2':
                self.spell_mode.run()
            elif choice == '3':
                self.review_mode.run()
            elif choice == '4':
                self.engine.show_stats()
                input(f"{Colors.HACKER_DIM}[按 Enter 返回菜单...]{ANSI.RESET}")
            elif choice == '5':
                self.run_unit_selection()
    
    def run_unit_selection(self):
        """运行单元选择"""
        while True:
            self.show_unit_menu()
            Terminal.print_prompt()
            
            choice = input().strip()
            
            if choice == '0':
                break
            
            # 转换为单元索引
            try:
                idx = int(choice) - 1
                unit_keys = list(VOCABULARY.keys())
                if 0 <= idx < len(unit_keys):
                    unit_key = unit_keys[idx]
                    unit_name = VOCABULARY[unit_key]['name']
                    
                    # 选择学习模式
                    self.show_unit_learning_menu(unit_key, unit_name)
                    Terminal.print_prompt()
                    mode_choice = input().strip()
                    
                    if mode_choice == '1':
                        self.learn_mode.run(unit_key)
                    elif mode_choice == '2':
                        self.spell_mode.run(unit_key)
                    # 0 或其他返回
            except ValueError:
                pass
    
    def exit_program(self):
        """退出程序"""
        Terminal.clear()
        print(f"""
{Colors.HACKER_GREEN}
    ╔════════════════════════════════════════╗
    ║                                        ║
    ║     感谢使用 VOCAB_HACKER!             ║
    ║                                        ║
    ║     📚 持续学习，天天进步              ║
    ║                                        ║
    ║     祝 CET-4 考试顺利! 🎓              ║
    ║                                        ║
    ╚════════════════════════════════════════╝
{ANSI.RESET}
""")
        
        # 显示最终统计
        progress = self.engine.progress
        if progress.get('total_score', 0) > 0:
            print(f"    {Colors.INFO_CYAN}本次学习获得积分: {progress['total_score']}{ANSI.RESET}\n")
        
        print(f"{Colors.HACKER_DIM}再见，框框！加油备考！💪{ANSI.RESET}\n")


# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    try:
        # 确保UTF-8编码
        if sys.platform == 'win32':
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        
        # 启动程序
        app = VocabHacker()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.ERROR_RED}\n程序被中断。再见！{ANSI.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.ERROR_RED}程序出错: {e}{ANSI.RESET}")
        import traceback
        traceback.print_exc()
