# coding:utf-8
# Author: Darj Lin
import argparse
import fengyun

parser = argparse.ArgumentParser()
parser.add_argument('-f',
                    help='files to store username/passwd,default=None',
                    default=None)
parser.add_argument('-u', help='username,ignore when f is valid',
                    default=None)
parser.add_argument('-p', help='passwd,ignore when f is valid',
                    default=None)

args = parser.parse_args()
[filename, username, passwd] = list(args.__dict__.values())

if filename:
    with open(filename, 'r') as f:
        [username, passwd] = f.readlines()
        print('username: {}\npasswd: {}\n'.format(username.strip(),
                                                  passwd.strip()))
else:
    name = input('username \n>  ')
    pswd = input('password \n>  ')
    
fy = fengyun.fengyun(username, passwd)
fy.printInfo()
sess = fy.saveSession()
print('Finished')


