"""
Copyright(c) 2020 Andy Zhou
This is a spammer program to crash your disk and RAM.
------------------------------
Test Result

8G 128G i5-8250U Surface Pro 6
Highest Writing Speed: 27.9 MB/s
Highest RAM Use: 1.9G

16G 512G R5-3500U ThinkPad T495
Highest Writing Speed: 28.2MB/s
Highest RAM Use: 4.2G
"""
import threading
import click
filen = "x.txt"
fileo = open(filen, "a")

@click.command()
def spam_disk_ram():
    try:
        while True:
            fileo.write("Hello World!\n"*(2**5))
    except KeyboardInterrupt:
        pass
    except:
        fileo.close()


for j in range(0, 10000000001):
    threading.Thread(target=spam_disk_ram).start()

fileo.close()
