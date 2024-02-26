!/usr/bin/env python3
 import os
 from pyresparser import ResumeParser
 # from resume_parser import ResumeParser
 from typing import Dict
 from docx2pdf import convert
 import shutil


 best_experience = ['health and nutrition', 'health nutrition', 'nutrition health', 'health', 'nutrition']
 good_experience = ['project managment', 'project', 'managment']
 skills = {}


 def save_to_folder(file, dest_path):

     if not isinstance(file, str):
         raise TypeError('file name is not string')
     if not isinstance(dest_path, str):
         raise TypeError('file path is not string')

     source_path = 'template_cv/' + file

     try:
         shutil.move(source_path, dest_path)
         print(f"file {file} copied to the path {dest_path}")
     except IOError as e:
         print(e)
         print(f"file {file} not copied to path {dest_path}")
         return False
     return True



 def main():
     folderpath = "template_cv/"
     files = [file for file in os.listdir(folderpath) if os.path.isfile(folderpath + '/' + file)]
     # print(len(files))
     total_best = 0
     total_good = 0
     for cv in files:
         cv_path = folderpath + cv
         extract = ResumeParser(cv_path).get_extracted_data()
         # print(extract['experience'])
         # if extract.get('experience', None) is None or extract.get('experience', None) == []:
             # save_to_folder(cv, 'exp_none')
         try:
             for b in best_experience:
                 if b in extract.get('experience'):
                     total_best += 10

             for g in good_experience:
                 if g in good_experience:
                     total_good += 10
         except Exception:
             pass
         try:
             for s in skills.keys():
                 if s in extract.get('skills'):
                     if skills[s] == 1:
                         total_best += 1
                     elif skills[s] == 0:
                         total_good += 1
         except Exception:
             pass 
         if total_best >= total_good:
             save_to_folder(cv, 'best_resume')
         else:
             save_to_folder(cv, 'good_resume')
         total_good = 0
         total_best = 0          


 if name == 'main':
     main()