import os
os.system('title PyP decompressor')
print('PyP Decompressor - make sure you want to decompress into this directory')
input('If so, press enter')
print('Decompressing...')

#Auto generated code:
os.mkdir("To compress//1")
os.mkdir("To compress/2")
file = open("To compress//1/testa.txt", 'w')
file.write("""some random text""")
file.close()
file = open("To compress//2/testb.py", 'w')
file.write("""print('and some more')""")
file.close()
input("Done!")