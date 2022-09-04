import subprocess


process1 = subprocess.Popen(["python", "server.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "detectbutton.py"])
process3 = subprocess.Popen(["python", "pop2.py"])

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()