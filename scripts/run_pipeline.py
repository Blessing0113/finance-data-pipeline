import subprocess

print("Starting Finance Pipeline...")

scripts = ['extract.py', 'transform.py', 'load.py', 'visualize.py']

for script in scripts:
    print(f"\nRunning {script}...")
    subprocess.run(['python', script], check=True)

print("\nPipeline Complete! Database and dashboard updated.")