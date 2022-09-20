import heapq
from importlib.resources import path
import os
import json
class HuffmanEncoding:
    def __init__(self,path):
        self.path =path 
        self.heap = []
        self.codes = {} 
        self.reverse_mapping = {}

    
    def create_codes(self,node1, val=''):
    # huffman code for current node
      newVal = val + str(node1.huff)
 
    # if node is not an edge node
    # then traverse inside it
      if(node1.left):
           self.create_codes(node1.left, newVal)
      if(node1.right):
           self.create_codes(node1.right, newVal)
    
        # if node is edge node then
        # display its huffman code
      if(not node1.left and not node1.right):
         self.codes[node1.char] = newVal
         self.reverse_mapping[newVal] = node1.char
             
            
    class node :
        def __init__(self, char, freq,left = None,right= None):
            self.char = char 
            self.freq = freq 
            self.left = left 
            self.right = right 
            self.huff = ''

        def __lt__(self, other):
            return self.freq<other.freq
            
        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, node)):
                return False
            return self.freq == other.freq      
            
         

    def cal_freq(self,text):
        freq = {}
        for character in text :
            if not(character in freq):
                freq[character] = 0 
            freq[character]+=1
        return freq              

    def make_padding(self,encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text = encoded_text+('0'*extra_padding)
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info+encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b    


        
   

    def add_to_heap(self,frequency):
         for key in frequency:
                one_node = self.node(key,frequency[key])
               
                heapq.heappush(self.heap,one_node)


    def make_huffman_tree(self):
        while(len(self.heap)>1):
                node1 = heapq.heappop(self.heap)
                node2 = heapq.heappop(self.heap)
                node1.huff = 0
                node2.huff= 1
                merged = self.node(None,node1.freq+node2.freq)
                merged.left = node1
                merged.right = node2
                heapq.heappush(self.heap,merged)

    def compress(self):
        tail_head = os.path.split(self.path)
        tail_head = list(tail_head)

        extension_position = tail_head[1].index('.')
        filenme = tail_head[1][:extension_position]

        if(len(tail_head[0])!=0):
            tail_head[0]=tail_head[0]+'/'



        output_path = tail_head[0]+filenme+'.bin'
        outputHeader_path = tail_head[0]+filenme+'_Header.json'

        #print(output_path)
        with open(self.path,'r+') as file , open(output_path,'wb') as output,open(outputHeader_path,'w') as outputHeader:
            text = file.read().rstrip()
            frequency = self.cal_freq(text)

          #adding elements into heap
          
            self.add_to_heap(frequency)
            

            #MAKING HUFFMAN TREEE
            self.make_huffman_tree()

           
            

            #  making encoded text 
            if(len(text)==1):
                self.create_codes(heapq.heappop(self.heap),'1')
            else:
                self.create_codes(heapq.heappop(self.heap))  
             
            
            
            encoded_text = ""
            for character in text:
              encoded_text += self.codes[character]


            padded_text = self.make_padding(encoded_text)
            b = self.get_byte_array(padded_text)
            output.write(bytes(b))
            print('output file created in ',output_path)
            json.dump(frequency, outputHeader) 
            print('json file created in',outputHeader_path)    

   
'''
ob = HuffmanEncoding('mytest.text')
ob.compress()'''



