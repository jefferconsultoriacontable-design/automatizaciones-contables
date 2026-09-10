import subprocess

try:
    resultado = subprocess.run(
        ["git", "--version"], 
        capture_output=True, 
        text=True, 
        check=True
    )
    print("Git está instalado:")
    print(resultado.stdout.strip())
except FileNotFoundError:
    print("Git NO está instalado o no se encuentra en el PATH del sistema.")

    