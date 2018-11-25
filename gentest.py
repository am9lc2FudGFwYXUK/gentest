#!/usr/bin/env python36 

import json
import sys
import getopt
import os

from random import shuffle 



def testdata():

    rc="""

{
     "form": {
          "course_number": "Course Number: EE-101",
          "course_name": "Course Title: I'd like to have an argument",
          "test_title": "Test Name: Quiz #1",
          "first_name": "First Name: ________________________________",
          "last_name": "Last Name: _________________________________",
          "instructor_name": "Instructor: Mr. Creosote",
          "date": "Todays Date: ________ "
     },
     "questions": [
          {
               "type": "true_false",
               "question": "Is this true or false ? ",
               "selections": [
                    true,
                    false
               ], 
               "answer":true
          },
          {
               "type": "multiple_choice",
               "question": "This is a multiple choice question",
               "selections": [
                    "Selection 1",
                    "Selection 2",
                    "Selection 3"
               ],
               "answer":"Selection 1"
          },
                    {
               "type": "matching",
               "question": "This a matching question",
               "key_values": {
                    "Something Red":"Fire Truck",
                    "Something New":"Shoes",
                    "Something Borrowed":"Money",
                    "Something Blue":"Ocean"
               }
          },
          {
               "type": "fill_in_the_blank",
               "question": "This is a fill in the {blank} question",
               "blank":"________", 
               "answer": "Blank"
          }
     ]
}
"""

    return rc





class TestGen():

    data = None


    def __init__(self):

        self.data = dict() 

        return

    def Load(self, filename):


        for i in filename:
            f = open(i, "r")

            if not f:
               return

            rc = json.load(f)
            f.close()

            self.data.update(rc)

        return self.data 
 

    def ProcessFormData(self):

            f = ['first_name','last_name','date', 'course_name', 'course_number', 'test_title', 'instructor_name']

            if not self.data:

                return

            if 'form' in self.data:

                for i in f:
                    if i in self.data['form']:
                        print("{}".format(self.data['form'][i]))

            print("")
            print("")

            return

    def ProcessTestQuestions(self, randomize=False, answerkey=False, r_just=3, l_just=20, **options):


        if not self.data:
            return

        if 'questions' not in self.data.keys():
            print("Here") 
            return

        if randomize:
            shuffle(self.data['questions'])

        if 'number_of_questions' in options.keys():
            del self.data['questions'][options['number_of_questions']:]

        for i,j in zip(self.data['questions'], range(1, len(self.data['questions']) + 1)):

            if i['type'] == "true_false":

                if i['answer'] not in i['selections']:
                     print(" Error: an \"answer\" exact match must be found within the \"selections\"")
                     sys.exit(1)
                print("{}. {}\n".format(j, i['question']))
                for k, l in zip('abcdefghijklmonpqrstuvwxyz', i['selections']):
                    print("{}. {}".format(str.rjust(k, 3), l))
                if answerkey:
                    print("\nANSWER={}\n".format(i['answer']))

            elif i['type'] == "multiple_choice":
                print("{}. {}\n".format(j, i['question']))
                for k, l in zip('abcdefghijklmonpqrstuvwxyz', i['selections']):
                    print("{}. {}".format(str.rjust(k, 3),  l))
                if answerkey:
                    print("\nANSWER={}\n".format(i['answer']))
                    
            elif i['type'] == 'fill_in_the_blank':
                q = i['question'].format(**i)
                print("{}. {}\n".format(j, q))
                if answerkey:
                    print("\nANSWER={}\n".format(i['answer']))

            elif i['type'] == 'essay':
                q = i['question'].format(**i)
                print("{}. {}\n".format(j, q))
                if 'lines' in i:
                    for j in range(i['lines']):
                        print("")

                if answerkey and 'answer' in i.items():
                    print("\nANSWER={}\n".format(i['answer']))
                
            elif i['type'] == 'matching':
                ## print(dir(i)) 
                q = i['question'].format(**i)
                print("{}. {}\n".format(j, q))

                x = list(i['key_values'].keys())
                y = list(i['key_values'].values())

                shuffle(y)
                shuffle(x) 

                letters = (i for i in "abcdefghijklmnopqrstuvwxyz")
                
                for k,l in zip(x, y):
                    print(" ___ {} {}. {}".format(str.ljust(k, 20), next(letters), str.rjust(l,0)))
                if answerkey:
                    print("")
                    for i, j, in i['key_values'].items():
                            print("ANSWER {} = {}".format(i, j))
                            
                    
                
            print("")



def Usage(progname):

    progname = os.path.basename(progname)
    
    print("")
    print("\t{}: Formats and creates tests from JSON description file".format(progname))
    print("")
    print("\tOptions:")
    print("")
    print("\t\t-h --help Print Help (this text)")
    print("\t\t-k --key  Produce Answer Key")
    print("\t\t-R --randomize Randomize the sequence of the questions")
    print("\t\t-J --json-files <filename1,filename2,filename3> Read details from the named JSON file, or chain load")
    print("\t\t-P --print-json Print Sample JSON test definitions (and then exit)")
    print("\t\t-n --number <Number> only produce a test with number questions...")
    print("")


    return         


if __name__ == "__main__":

    if len(sys.argv) < 2:
            Usage(sys.argv[0])
            sys.exit(1)
            
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hkRJ:Pn:", ["help", "key", "randomize", "json-file", "print-json", "number"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        Usage(sys.argv[0])
        sys.exit(2)

    options = dict() 

    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            Usage(sys.argv[0])
            sys.exit(1)
        elif o in ("-k", "--key"):
            options["answerkey"] = True
        elif o in ("-R", "--randomize"):
            options["randomize"] = True
        elif o in ("-J", "--json-file"):
            options["json_file"] = a.split(',')
        elif o in ("-P", "--print-json"):
            print(testdata()) 
            sys.exit(0)             
        elif o in ("-n", "--number"):
            options["number_of_questions"] = int(a)
        else:
            assert False, "unhandled option"

    if 'json_file' not in options.keys():
            print("You need to pass in a JSON file for processing... ")
            Usage(sys.argv[0])
            sys.exit(1) 
            

            
    c = TestGen()
    c.Load(options['json_file'])
    c.ProcessFormData()
    c.ProcessTestQuestions(**options)

    





