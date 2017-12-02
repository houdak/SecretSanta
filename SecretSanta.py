"""
Secret Santa Generator
Created: November 26, 2017
Last Updated: December 2, 2017
Author: Houda Khaled
"""

import os
from itertools import permutations
from random import choice
import smtplib
from email.mime.text import MIMEText

os.getcwd()

def LoadFile(filename):
    """Loads file from same directory, given name of file"""
    wd = os.getcwd()
    pathway = wd + '\\' + filename
    with open(pathway) as file:
        data = file.read()
    return data

def ExportToFile(filename,data):
    """Exports results to same directory folder"""
    wd = os.getcwd()
    pathway = wd +'\\' + filename
    with open(pathway,'w') as file:
        file.write(data)
    return

""" Because the previous website I used to generate secret santa listings now
appears to be defunct, and I would like to avoid risking putting in my friends'
emails into a potentially-shady website (and also for good practice!), I decided
to make my own secret santa generator. By inputing the names and emails of
each participant, as well as people they should *not* be assigned, this
code should assign a recepient to each person, and send them an email
notifying them of their recipient! """

""" Main file should have one line per participant in the following format:
name,email, {exclude1,exclude2} """
mainfile = 'secretsanta_names.txt'
subjectfile = 'secretsanta_subject.txt'
emailbodyfile = 'secretsanta_message.txt'


def ParseEmails(filename):
    """ Match email with each person """
    input = LoadFile(filename).split('\n')
    email_dict = {}
    for line in input:
        line = line.split(',')
        email_dict[line[0]] = line[1]
    return email_dict


def AssignmentGenerator(filename):
    """ Creates two coordinating lists of 'givers' and 'receivers'
    of gifts randomly, accounting for exclusions """
    input = LoadFile(filename).split('\n')

    # Create name: exclusion dictionary
    participants = [] # also collect names of participants
    exclusion_dict = {}
    for line in input:
        # get part in brackets
        exclusions = line[line.find('{')+1 : line.find('}')]
        exclusions = exclusions.split(', ')
        # get name
        name = line.split(',')[0]
        participants.append(name) # for later use...
        # add to dict!
        exclusion_dict[name] = exclusions
    
    # Generate all possible combinations with itertools
    """ To do this, we can generate all possible permutations of the list
        Then, just partition neighbors as pairs! """
    # 1. Make all possible permutations:
    perms = list(permutations(participants))
    # 2. Pick two random permutations and "align"
    while True:
        givers = choice(perms)
        receivers = choice(perms)
        if Valid(givers,receivers,exclusion_dict):
            break
     
    return [givers,receivers]


def Valid(giver,receiver,exclusion_dict):
    """ Checks if any exclusions were violated.
    Does this by seeing if any pairs are in dict"""
    for i in range(len(giver)):
        if giver[i] == receiver[i]:
            return False
        elif receiver[i] in exclusion_dict[giver[i]]:
            return False
    return True


def CreateMessage(giver,receiver,subjectfile,messagefile):
    """ Uses the template to personalize message to proper
    giver and receiver of gifts """
    subject = LoadFile(subjectfile)
    body = LoadFile(messagefile)
    body = body.replace('GIVER',giver)
    body = body.replace('RECEIVER',receiver)
    return [subject,body]


def SendEmail(giver,receiver,email_dict,subject,emailbody):
    """ Sends individual email based on list of givers & receivers """
    # set up server and login
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('username','password')
    
    # send email
    [subject,body] = CreateMessage(giver,receiver,subject,emailbody)
    to = email_dict[giver]
    fromx = 'youremail@gmail.com'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = fromx
    msg['To'] = to
   
    server.sendmail(fromx,to,msg.as_string())
    server.quit()
    return


def SecretSantaSendOut():
    """ Puts all other fxns together!! """
    email_dict = ParseEmails(mainfile)
    [givers,receivers] = AssignmentGenerator(mainfile)
    
    for i in range(len(givers)):
        SendEmail(givers[i],receivers[i],email_dict,subjectfile,emailbodyfile)
    print("Secret Santa assignment send out was successful.")
    return
    

SecretSantaSendOut()