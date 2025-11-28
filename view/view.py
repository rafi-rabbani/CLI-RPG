from models import creatures
import os

def status(creature):
    print(creature)

def init():
    print(f"{'-' * 100}\n{' ROLE PLAYING GAME ':=^100}\n{' by Fizz ':-^100}")
    karakter = int(input(
        f"\nKarakter yang tersedia:" +
        f"\n1. Fighter" +
        f"\n2. Archer" +
        f"\n3. Tank" +
        f"\nSilahkan pilih berdasarkan angka (1-3) : "
        ))
    
    return karakter