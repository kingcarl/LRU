#-*- coding:UTF-8 -*-
#=============================================================================
#     FileName: LRU.py
#         Desc: LRU Algorithm
#       Author: guannipishi
#        Email: kingcarl725@163.com
#      Version: 0.1
#   LastChange: 2014-03-21 15:44:25
#      History:
#=============================================================================

import time

LRU_NODE_NUM_DEFAULT = 10
LRU_QUEUE_LEN_DEFUALT = 10

class LruNode:
    """LRU Node infomation"""
    def __init__(self, item=None, num=1):
        self.item = item
        self.num = num
        self.ltime = time.time()

    def update(self):
        self.ltime = time.time()
        self.num += 1

class LruEntry:
    """LRU Node List"""
    def __init__(self, max_item_num, lock):
        self.max_item_num = max_item_num
        self.lru_nodes = []
        if lock:
            from threading import Lock
            self.lru_lock = Lock()
        else:
            from multiprocessing import Lock
            self.lru_lock = Lock()

    def _insert_node_in_entry(self, item, full=False):
        pos = self.find_node_in_entry(item)
        self.lru_lock.acquire()
        if pos < 0:
            if not full:
                self.lru_nodes.append(LruNode(item=item))
            else:
                self.lru_nodes.pop(0)
                self.lru_nodes.append(LruNode(item=item))
        else:
            self.lru_nodes[pos].update()
        self.lru_lock.release()

    def insert_node_in_entry(self, item):
        if len(self.lru_nodes) <= self.max_item_num:
            self._insert_node_in_entry(item)

            """ 
            [1]sort Lru Node List to make sure that the minimum item at the top of list
            [2]based on step 1, sort Lru Node List to make sure nearest item at the bottom of list
            """
            self.lru_lock.acquire()
            self.lru_nodes = sorted(self.lru_nodes, key=lambda x: x.num)
            self.lru_nodes = sorted(self.lru_nodes, key=lambda x: x.ltime)
            self.lru_lock.release()
        else:
            self._insert_node_in_entry(item, True)
            self.delete_node_in_entry()

    def delete_node_in_entry(self):
        self.lru_lock.acquire()
        self.lru_nodes.pop(0)
        self.lru_lock.release()

    def find_node_in_entry(self, item):
        pos = 0
        self.lru_lock.acquire()
        for li in self.lru_nodes:
            if item == li.item:
                self.lru_lock.release()
                return pos
            else:
                pos += 1
        self.lru_lock.release()

        return -1

class LruQueue:
    """
    `max_queue_len`: the maximum length of lru queue
    `max_item_num`: the maximum number of lru queue entry
    `tlock`: True (thread lock), False (process lock), default value is False
    """
    def __init__(self, max_queue_len=LRU_QUEUE_LEN_DEFUALT, max_item_num=LRU_NODE_NUM_DEFAULT, tlock=False):
        self.max_queue_len = max_queue_len
        self.max_item_num = max_item_num
        self.tlock = tlock
        self.LRU_QUEUE_BUCKET = [ n for n in range(self.max_queue_len) ] 

    def insert_node(self, item):
        key = self.lru_hash(item)
        if self.find_node(key):
            self.LRU_QUEUE_BUCKET[key].insert_node_in_entry(item)
        else:
            self.LRU_QUEUE_BUCKET[key] = LruEntry(self.max_item_num, self.tlock)
            self.LRU_QUEUE_BUCKET[key].insert_node_in_entry(item)

    def find_node(self, item):
        key = self.lru_hash(item)
        if isinstance(self.LRU_QUEUE_BUCKET[key], LruEntry):
            return True
        else:
            return False

    def lru_hash(self, item):
        return (hash(item) / self.max_queue_len) % self.max_queue_len

    def get_data(self):
        return self.LRU_QUEUE_BUCKET

    def print_queue_info(self):
        for le in self.LRU_QUEUE_BUCKET:
            if isinstance(le, LruEntry):
                for ln in le.lru_nodes:
                    print "item[{0}], num[{1}]".format(ln.item, ln.num)