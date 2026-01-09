import os
import struct

def utf8(s):
    b = s.encode('utf-8')
    return bytes([1]) + struct.pack('>H', len(b)) + b

def class_entry(name_index):
    return bytes([7]) + struct.pack('>H', name_index)

def name_and_type(name_index, descriptor_index):
    return bytes([12]) + struct.pack('>HH', name_index, descriptor_index)

def method_ref(class_index, name_and_type_index):
    return bytes([10]) + struct.pack('>HH', class_index, name_and_type_index)

cp_entries = []
cp_entries.append(utf8('Test'))        #1
cp_entries.append(class_entry(1))       #2
cp_entries.append(utf8('java/lang/Object'))  #3
cp_entries.append(class_entry(3))       #4
cp_entries.append(utf8('<init>'))       #5
cp_entries.append(utf8('()V'))          #6
cp_entries.append(name_and_type(5, 6))  #7
cp_entries.append(method_ref(4, 7))     #8
cp_entries.append(utf8('Code'))         #9
cp_entries.append(utf8('ScalaSig'))     #10
cp_entries.append(utf8('Test.java'))    #11

data = bytearray()
data += b'\xCA\xFE\xBA\xBE'
data += struct.pack('>HH', 0, 52)
cp_count = len(cp_entries) + 1
data += struct.pack('>H', cp_count)
for entry in cp_entries:
    data += entry

# access_flags, this, super
data += struct.pack('>H', 0x0021)
data += struct.pack('>H', 2)
data += struct.pack('>H', 4)
# interfaces
data += struct.pack('>H', 0)
# fields
data += struct.pack('>H', 0)
# methods_count=1
data += struct.pack('>H', 1)
# method <init>
data += struct.pack('>H', 0x0001)
data += struct.pack('>H', 5)
data += struct.pack('>H', 6)
data += struct.pack('>H', 1)
# Code attribute
code_length = 5
data += struct.pack('>H', 9)
data += struct.pack('>I', 2 + 2 + 4 + code_length + 2 + 2)
data += struct.pack('>H', 1)
data += struct.pack('>H', 1)
data += struct.pack('>I', code_length)
data += bytes([0x2a, 0xb7, 0x00, 0x08, 0xb1])
data += struct.pack('>H', 0)
data += struct.pack('>H', 0)
# class attributes_count
data += struct.pack('>H', 1)
data += struct.pack('>H', 10)
data += struct.pack('>I', 2048)
# attribute_info: minimal
data += b'\x00\x00'

os.makedirs('bad', exist_ok=True)

with open('bad/Test.class', 'wb') as f:
    f.write(data)
