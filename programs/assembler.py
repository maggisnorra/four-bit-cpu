import argparse

parser = argparse.ArgumentParser()
parser.parse_args()

f = open("D:\\myfiles\welcome.txt")
print(f.read()) 

with open("demofile.txt") as f:
  print(f.read()) 