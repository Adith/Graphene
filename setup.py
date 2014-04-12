#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup
import sys, os

# ███████╗███████╗████████╗██╗   ██╗██████╗ 
# ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
# ███████╗█████╗     ██║   ██║   ██║██████╔╝
# ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
# ███████║███████╗   ██║   ╚██████╔╝██║     
# ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
# Uncomment
                                                                                     
# setup(name='Graphene',
#       version='1.0',
#       description='Social Network Graph Language Compiler',
#       author='Adith Tekur, Pooja Prakash, Sumiran Shah, Sarah Panda, Neha Rastogi',
#       url='https://github.com/Adith/Graphene',
#       # packages=['ply']
#      )	        

# ████████╗ ██████╗     ██████╗  ██████╗ 
# ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗
#    ██║   ██║   ██║    ██║  ██║██║   ██║
#    ██║   ██║   ██║    ██║  ██║██║   ██║
#    ██║   ╚██████╔╝    ██████╔╝╚██████╔╝
#    ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝ 
                                       
# Setup PATH
# Compile into an executable

if len(sys.argv) > 1:
    if sys.argv[1] in ['install']:
        sys.path.append(os.path.dirname(os.path.realpath(__file__)))
