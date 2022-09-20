import heapq
import os
import json
class HuffmanDecoding:
    def __init__(self,bin_path,json_path,dc_path):
        self.bin_path = bin_path
        self.json_path = json_path
        self.dc_path = dc_path
        self.rev_dic= None

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text
    def decode_text(self, encoded_text,):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.rev_dic):
                character = self.rev_dic[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text
    

    

    def decompression(self):
        with open(self.json_path,'r') as jsonfile :
              #EXTRACTING THE DICTIONARY FROM JASON FILE
            frequency = json.load(jsonfile) 
         
        
        with open(self.dc_path  ,  'w') as output, open(self.bin_path,'rb') as file :
            from EncodingHuffman import HuffmanEncoding as hc 
            if(len(frequency)==1):
                 ls = list(frequency.keys())
                 output.write(ls[0]*frequency[ls[0]])
                 print('Decompressed')
                 exit(0)


            object = hc(self.bin_path)

            object.add_to_heap(frequency)
            object.make_huffman_tree()
            object.create_codes(heapq.heappop(object.heap))  
            self.rev_dic = object.reverse_mapping

            bit_string = ""

            byte = file.read(1)
            while(len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)
            
            output.write(decompressed_text)

        print("Decompressed \nFile Path = ",self.dc_path)






        
         


#EXTRACTING BIN AND JSON FILE FOR DECOMPRESSION
binFile_path = input('enter the path of bin file to be decoded\n\n')
tail_head = os.path.split(binFile_path)
tail_head = list(tail_head)

if(len(tail_head[0])!=0):
    tail_head[0]=tail_head[0]+'/'


extension_position = tail_head[1].index('.')
filenme = tail_head[1][:extension_position]
jsonFile_path = tail_head[0]+filenme+'_Header.json'
decompressFile_path = tail_head[0]+filenme+'_dc.text'

ob = HuffmanDecoding(binFile_path,jsonFile_path,decompressFile_path)
ob.decompression()
