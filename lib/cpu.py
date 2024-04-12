
import psutil

print("Number of CPU : ",psutil.cpu_count())

try:
        
            while True:
                        print("\rCPU Percentage : -----------",psutil.cpu_percent(1),'%-----------', end="")
except KeyboardInterrupt:
        pass