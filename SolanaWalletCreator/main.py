import subprocess
from mnemonic import Mnemonic
import os
import json

# Renkli yazı için terminal ANSI escape kodlarını ekliyoruz
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def install_solana():
    install_command = 'sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"'
    result = subprocess.run(install_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(bcolors.FAIL + "Solana kurulumunda hata oluştu:" + bcolors.ENDC, result.stderr)
        return False
    return True

def create_solana_wallet():
    if not install_solana():
        return

    os.environ["PATH"] = "/home/kali/.local/share/solana/install/active_release/bin/:" + os.environ["PATH"]
    solana_path = os.path.expanduser('~/.local/share/solana/install/active_release/bin/solana-keygen')

    if not os.path.exists(solana_path):
        print(bcolors.FAIL + f"Solana keygen dosyası bulunamadı: {solana_path}" + bcolors.ENDC)
        return

    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength=128)

    try:
        # Solana cüzdanı oluşturuluyor
        result = subprocess.run([solana_path, 'new', '--no-bip39-passphrase', '--force'], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Çıktıdan cüzdan adresini ayıkla
            wallet_output = result.stdout.splitlines()
            # Public Key (Cüzdan Adresi)
            wallet_address = [line for line in wallet_output if line.startswith("pubkey:")][0].split(" ")[1].strip()
            print(bcolors.OKCYAN + "Solana wallet created successfully!" + bcolors.ENDC)
            print("\n" + bcolors.OKBLUE + f"Cüzdan Adresi: {wallet_address}" + bcolors.ENDC)

            # Burada özel anahtar dosyasını okuma ve yazma işlemi kaldırıldı, sadece çıktıyı ekrana yazdırıyoruz
            print(bcolors.WARNING + "\nMnemonic şifrenizi güvenli bir yerde saklayın:" + bcolors.ENDC)
            print(bcolors.OKGREEN + mnemonic_phrase + bcolors.ENDC)

        else:
            print(bcolors.FAIL + "Cüzdan oluşturulurken hata oluştu:" + bcolors.ENDC, result.stderr)
    except Exception as e:
        print(bcolors.FAIL + f"Hata: {e}" + bcolors.ENDC)

create_solana_wallet()
