#@Author: Carl
#@Date: 2014/3/21
#@description: LRU Algorithm

LRU_NODE_LEN = 10
LRU_QUEUE_LEN_DEFUALT = 10

class LRU_Node(object):
	"""LRU Node infomation"""
	def __init__(self, item=None, num=0):
		self.item = item
		self.num = num

	def update(self):
		self.num += 1

class LRU_Entry(object):
	"""LRU Node List"""
	def __init__(self, max_item_num):
		self.max_item_num = max_item_num
		self.lru_nodes = []

	def insertNodeInEntry(self, item):
		if len(self.lru_nodes) <= self.max_item_num:
			pos = self.findNodeInEntry(item)
			if (pos < 0):
				self.lru_nodes.append(LRU_Node(item=item))
			else:
				self.lru_nodes[pos].update()

			""" sort Lru Node List to make sure that the minimum node on the top of list"""	
			self.lru_nodes = sorted(self.lru_nodes, key=lambda x: x.num )
		else:
			self.deleteNodeInEntry()

	def deleteNodeInEntry(self):
		self.lru_nodes.pop(0)
		
	def findNodeInEntry(self, item):
		pos = 0
		for li in self.lru_nodes:
			if item == li.item:
				return (pos)
			else:
				pos += 1
		return (-1)

class LRU_Queue(object):
	def __init__(self, maxlen):
		self.max_bucket_len = maxlen
		self.LRU_Queue_Bucket = [ n for n in range(self.max_bucket_len) ] #initialize bucket

	def insertNode(self, item):
		key = self.lruHash(item)
		if self.findNode(key):
			self.LRU_Queue_Bucket[key].insertNodeInEntry(item)
		else:
			self.LRU_Queue_Bucket[key] = LRU_Entry(LRU_NODE_LEN)
			self.LRU_Queue_Bucket[key].insertNodeInEntry(item)
	
	def findNode(self, key):
		if isinstance(self.LRU_Queue_Bucket[key], LRU_Entry):
			return True	
		else:
			return False

	def lruHash(self, item):
		return (hash(item) / self.max_bucket_len) % self.max_bucket_len
		
	def showALL(self):
		for le in self.LRU_Queue_Bucket:
			if isinstance(le, LRU_Entry):
				for ln in le.lru_nodes:
					print "%s  %d" % (ln.item, ln.num)	
