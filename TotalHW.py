#=============================================#
#                 Total HW                    #
#=============================================#
#                                             #
#       Author: Vincenzo Mucciante            #
#       Release Date: 14/09/2018              #
#       Version: 1.2.0                        #
#                                             #
#=============================================#
#                                             #
#   What you need:                            #
#   1) a bag inside your backpack             #
#   2) a bag inside the bank                  #
#   3) a runebook with runes for bank and hw  #
#   4) a beetle                               #
#   Info:                                     #
#   - don't use a bag with the shape          #
#     of a backpack                           #
#=============================================#

import clr, time
clr.AddReference("System.Collections")
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Diagnostics import Process
from datetime import datetime
from System.IO import Directory, Path, File
from System.Collections import *
from System.Drawing import Point, Color, Size, Font, FontStyle
from System.Windows.Forms import (LinkLabel, CheckBox, Application, Button, Timer, Form, ComboBox, 
    BorderStyle, GroupBox, Label, TextBox, ListBox, Panel, RadioButton,
    FlatStyle)
from System.ComponentModel import Container

    
###User settings
TrashDelay = 700
DragDelay = 700
TimeoutOnWaitAction = 500
###

#General settings
QuestGiverSerial = 0x00006AC1
ContextQuestToggleID = 5
TrashCan = 0x4013FA9E
BoltID = 0x1BFB
##

class KeepForm(Form):
    ScriptName = 'TotalHW by Rosikcool'
    
    var = {'magery': "True", 'chivalry' : "False",'posX' : 0, 'posY': 0,'home' : "True", 'innkeeper': "False", 'number' : 1, 'checked' : False, 'start' : datetime.now(), 'recallBank' : 0, 'restockBolt' : 0, 
    'recallHW' : 0, 'enterHW' : 0, 'goingToNPC' : 0, 'deliver' : 0, 'reloadBeetle' : 0,
    'goBack' : 0, 'checkReward' : 0, 'completedQuest' : 0, 'kitHwFound' : 0, 'kitYewFound' : 0,
    'oldTime' : "0001-01-01 00:00:00", 'actualTime' : "0001-01-01 00:00:00", 'beetleSerial' : 0, 'containerBackpack' : 0, 'containerBank' : 0,
    'runebook' : 0, 'minBonus' : 0, 'exBonus' : 0, 'moveAmount' : 0 }
    
    props = {'Jdamageincrease' : 0 , 'Jdefensechanceincrease' : 0, 'Jdexteritybonus' : 0, 'Jenhancepotions' : 0,
    'Jfastercastrecovery' : 0, 'Jfastercasting' : 0, 'Jhitchanceincrease' : 0, 'Jintelligencebonus' : 0, 
    'Jlowermanacost' : 0, 'Jlowerreagentcost' : 0, 'Jluck' : 0, 'Jspelldamageincrease' : 0, 'Jstrengthbonus' : 0}
    
    def __init__(self):
        elements = []
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(231,231,231)
        self.Size = Size(340, 355)
        self.Text = '{0}'.format(self.ScriptName)
        self.CenterToScreen()
        self.TopMost = True
        self.LoadFile()
        self.jf = Form()
        
        #SettingsBox
        self.settingsBox = GroupBox()
        self.settingsBox.BackColor = Color.FromArgb(35,35,35)
        self.settingsBox.Size = Size(310, 310)
        self.settingsBox.Location = Point(5, 2)
        self.settingsBox.ForeColor = Color.FromArgb(231,231,231)
        self.settingsBox.Text = 'Settings'
        
        #InfoLabel
        self.Info = Label()
        self.Info.Size = Size(295,15)
        self.Info.Location = Point(10,15)
        self.Info.Text = "Script settings, if u want to change delays, check the code."
        elements.append(self.Info)
        
        #BeetleLabel
        self.Pet = Label()
        self.Pet.Size = Size(200,15)
        self.Pet.Location = Point(10,35)
        self.Pet.Text = "Beetle serial: {0}".format(self.var['beetleSerial'])
        elements.append(self.Pet)
        
        #BeetleText
        self.PetT = Button()
        self.PetT.Text = "Set"
        self.PetT.Size = Size(80,20)
        self.PetT.Location = Point(210,30)
        self.PetT.Click += self.setBeetle
        elements.append(self.PetT)
        
        #ContainerBackpack
        self.ContainerB = Label()
        self.ContainerB.Size = Size(200,15)
        self.ContainerB.Location = Point(10,55)
        self.ContainerB.Text = "Container backpack serial: {0}".format(self.var['containerBackpack'])
        elements.append(self.ContainerB)
        
        #ContainerBackpackText
        self.ContainerBT = Button()
        self.ContainerBT.Text = "Set"
        self.ContainerBT.Size = Size(80,20)
        self.ContainerBT.Location = Point(210,50)
        self.ContainerBT.Click += self.setContainerBackpack
        elements.append(self.ContainerBT)
        
        #ContainerBank
        self.ContainerBank = Label()
        self.ContainerBank.Size = Size(200,15)
        self.ContainerBank.Location = Point(10,75)
        self.ContainerBank.Text = "Container inside bank serial: {0}".format(self.var['containerBank'])
        elements.append(self.ContainerBank)
        
        #ContainerBankT
        self.ContainerBankT = Button()
        self.ContainerBankT.Text = "Set"
        self.ContainerBankT.Size = Size(80,20)
        self.ContainerBankT.Location = Point(210,70)
        self.ContainerBankT.Click += self.setContainerBankT
        elements.append(self.ContainerBankT)
        
        #Runebook
        self.Runebook = Label()
        self.Runebook.Size = Size(200,15)
        self.Runebook.Location = Point(10,95)
        self.Runebook.Text = "Runebook serial: {0}".format(self.var['runebook'])
        elements.append(self.Runebook)
        
        #RunebookT
        self.RunebookT = Button()
        self.RunebookT.Text = "Set"
        self.RunebookT.Size = Size(80,20)
        self.RunebookT.Location = Point(210,90)
        self.RunebookT.Click += self.setRunebook
        elements.append(self.RunebookT)
        
        #Hints
        self.Hint = Label()
        self.Hint.Size = Size(270,12)
        self.Hint.Location = Point(20,115)
        self.Hint.Text = "Runes: 1°- Bank, 2°- HW Entrance, 3°- Home/Inn"
        elements.append(self.Hint)
        
        #BonusTalismansN
        self.BonusN = Label()
        self.BonusN.Size = Size(150,15)
        self.BonusN.Location = Point(10,135)
        self.BonusN.Text = "Talisman min normal bonus: "
        elements.append(self.BonusN)
        
        #BonusTalismansNB
        self.BonusNB = TextBox()
        self.BonusNB.Size = Size(30,15)
        self.BonusNB.Location = Point(161,130)
        self.BonusNB.Text = "{0}".format(self.var['minBonus'])
        elements.append(self.BonusNB)
        
        #BonusTalismanNBB
        self.BonusNBB = Button()
        self.BonusNBB.Text = "Set"
        self.BonusNBB.Size = Size(80,20)
        self.BonusNBB.Location = Point(210,130)
        self.BonusNBB.Click += self.setNormalBonus
        elements.append(self.BonusNBB)
        
        #BonusTalismansE
        self.BonusE = Label()
        self.BonusE.Size = Size(150,15)
        self.BonusE.Location = Point(10,155)
        self.BonusE.Text = "Talisman: min except bonus: "
        elements.append(self.BonusE)
        
        #BonusTalismansEB
        self.BonusEB = TextBox()
        self.BonusEB.Size = Size(30,15)
        self.BonusEB.Location = Point(161,150)
        self.BonusEB.Text = "{0}".format(self.var['exBonus'])
        elements.append(self.BonusEB)
        
        #BonusTalismanEBB
        self.BonusEBB = Button()
        self.BonusEBB.Text = "Set"
        self.BonusEBB.Size = Size(80,20)
        self.BonusEBB.Location = Point(210,150)
        self.BonusEBB.Click += self.setExecBonus
        elements.append(self.BonusEBB)
        
        #HomeB
        self.homeB = Button()
        self.homeB.Text = "Recall Settings"
        self.homeB.Size = Size(100,20)
        self.homeB.Location = Point(190,185)
        self.homeB.Click += self.setHome
        elements.append(self.homeB)
        
        #TrashDelay
        self.Trash = Label()
        self.Trash.Size = Size(150,15)
        self.Trash.Location = Point(10,175)
        self.Trash.Text = "Trash delay: {0} ms".format(TrashDelay)
        elements.append(self.Trash)
        
        #DragDelay
        self.Drag = Label()
        self.Drag.Size = Size(150,15)
        self.Drag.Location = Point(10,195)
        self.Drag.Text = "Drag delay: {0} ms".format(DragDelay)
        elements.append(self.Drag)
        
        #Timeout
        self.Timeout = Label()
        self.Timeout.Size = Size(270,15)
        self.Timeout.Location = Point(10,215)
        self.Timeout.Text = "Timeout on wait action delay: {0} ms".format(TimeoutOnWaitAction)
        elements.append(self.Timeout)
        
        #MoveAmount
        self.MoveAmount = Label()
        self.MoveAmount.Size = Size(155,15)
        self.MoveAmount.Location = Point(10,235)
        self.MoveAmount.Text = "Bolts from beetle to backpack: "
        elements.append(self.MoveAmount)
        
        #MoveAmountT
        self.MoveAmountT = TextBox()
        self.MoveAmountT.Size = Size(40,15)
        self.MoveAmountT.Location = Point(166,230)
        self.MoveAmountT.Text = "{0} ".format(int(self.var['moveAmount']))
        elements.append(self.MoveAmountT)
        
        #MoveAmountB
        self.MoveAmountB = Button()
        self.MoveAmountB.Text = "Set"
        self.MoveAmountB.Size = Size(80,20)
        self.MoveAmountB.Location = Point(210,230)
        self.MoveAmountB.Click += self.setMoveAmount
        elements.append(self.MoveAmountB)
        
        #StartButton
        self.btnStart = Button()
        self.btnStart.Text = 'Start'
        self.btnStart.BackColor = Color.FromArgb(50,50,50)
        self.btnStart.Size = Size(50, 30)
        self.btnStart.Location = Point(140, 260)
        self.btnStart.FlatStyle = FlatStyle.Flat
        self.btnStart.FlatAppearance.BorderSize = 1
        self.btnStart.Click += self.btnStartPressed
        elements.append(self.btnStart)
        
        #DonateLink
        self.btnDonate = Button()
        self.btnDonate.Text = 'Donate'
        self.btnDonate.BackColor = Color.FromArgb(50,50,50)
        self.btnDonate.Size = Size(50, 30)
        self.btnDonate.Location = Point(20, 260)
        self.btnStart.FlatStyle = FlatStyle.Flat
        self.btnStart.FlatAppearance.BorderSize = 1
        self.btnDonate.Click += self.linkDonatePressed
        elements.append(self.btnDonate)
        
        #JewelButton
        self.btnJewel = Button()
        self.btnJewel.Text = 'Jewels'
        self.btnJewel.BackColor = Color.FromArgb(50,50,50)
        self.btnJewel.Size = Size(50, 30)
        self.btnJewel.Location = Point(80, 260)
        self.btnJewel.FlatStyle = FlatStyle.Flat
        self.btnJewel.FlatAppearance.BorderSize = 1
        self.btnJewel.Click += self.jewelPressed
        elements.append(self.btnJewel)
        
        #ResetButton
        self.btnReset = Button()
        self.btnReset.Text = 'Reset Stats'
        self.btnReset.BackColor = Color.FromArgb(50,50,50)
        self.btnReset.Size = Size(90, 30)
        self.btnReset.Location = Point(200, 260)
        self.btnReset.FlatStyle = FlatStyle.Flat
        self.btnReset.FlatAppearance.BorderSize = 1
        self.btnReset.Click += self.btnResetPressed
        elements.append(self.btnReset)
        
        #Adding Elements
        for elem in elements:
            self.settingsBox.Controls.Add(elem) 
        self.Controls.Add(self.settingsBox)
        
    def btnStartPressed(self, send, args):
        elements = []
        self.var["beetleSerial"] = self.PetT.Text
        self.var["containerBank"] = self.ContainerBT.Text
        self.var["containerBackpack"] = self.ContainerBankT.Text
        self.var["minBonus"] = self.BonusNB.Text
        self.var["exBonus"] = self.BonusEB.Text
        self.var["runebook"] = self.RunebookT.Text
        
        self.Flags()
       
        while len(self.Controls) > 0:
            for ctr in self.Controls:
                self.Controls.Remove(ctr)

        self.LoadFile()
        #self.var["oldTime"] = datetime.strptime(str(self.var["oldTime"]),"%Y-%m-%d %H:%M:%S")
        
        #TimePassed
        #self.TimePassed = Label()
        #self.TimePassed.Size = Size(380,15)
        #self.TimePassed.Location = Point(0,15)
        #self.var["actualTime"] = datetime.now() - self.var["start"]
        #self.TimePassed.Text = "Time " + str((self.var["actualTime"] + self.var["oldTime"]).time())
        #elements.append(self.TimePassed)
        
        #Step
        self.Step = Label()
        self.Step.Size = Size(380,15)
        self.Step.Location = Point(0,30)
        self.Step.Text = "Step: ..."
        elements.append(self.Step)
        
        #CompletedQuests
        self.CompletedQuests = Label()
        self.CompletedQuests.Size = Size(380,15)
        self.CompletedQuests.Location = Point(0,45)
        self.CompletedQuests.Text = "Completed quests: {0}".format(self.var["completedQuest"])
        elements.append(self.CompletedQuests)
        
        #KitYewFound
        self.KitYewFound = Label()
        self.KitYewFound.Size = Size(380,15)
        self.KitYewFound.Location = Point(0,60)
        self.KitYewFound.Text = "Kit yew found: {0}".format(self.var["kitYewFound"])
        elements.append(self.KitYewFound)
        
        #KitHwFound
        self.KitHwFound = Label()
        self.KitHwFound.Size = Size(380,15)
        self.KitHwFound.Location = Point(0,75)
        self.KitHwFound.Text = "Kit hw found: {0}".format(self.var["kitHwFound"])
        elements.append(self.KitHwFound)
        
        #StopButton
        self.btnStop = Button()
        self.btnStop.Text = 'Stop'
        self.btnStop.BackColor = Color.FromArgb(50,50,50)
        self.btnStop.Size = Size(50, 30)
        self.btnStop.Location = Point(30, 260)
        self.btnStop.FlatStyle = FlatStyle.Flat
        self.btnStop.FlatAppearance.BorderSize = 1
        self.btnStop.Click += self.btnStopPressed
        elements.append(self.btnStop)
        
        #PauseButton
        self.btnPause = Button()
        self.btnPause.Text = 'Pause'
        self.btnPause.BackColor = Color.FromArgb(50,50,50)
        self.btnPause.Size = Size(50, 30)
        self.btnPause.Location = Point(230, 260)
        self.btnPause.FlatStyle = FlatStyle.Flat
        self.btnPause.FlatAppearance.BorderSize = 1
        self.btnPause.Click += self.btnPausePressed
        elements.append(self.btnPause)
        
        #Timer
        self.time = Timer(Container())
        self.time.Enabled = True
        self.time.Interval = 20
        self.time.Tick += self.OnTick
        
        #Timer2
        #self.time2 = Timer(Container())
        #self.time2.Enabled = False
        #self.time2.Interval = 999
        #self.time2.Tick += self.OnTick2
        
        #Adding Elements
        for elem in elements:
            self.Controls.Add(elem) 

    def linkDonatePressed(self, send, args):
        Process.Start("IExplore", 'paypal.me/vincenzomucciante')
        
    def setHome(self, send, args): 
        elements = []
        
        self.h = Form()
        self.h.BackColor = Color.FromArgb(25,25,25)
        self.h.ForeColor = Color.FromArgb(231,231,231)
        self.h.Size = Size(322, 200)
        self.h.Text = '{0}'.format(self.ScriptName)
        self.h.TopMost = True
        
        #ControlHome
        self.controlH = GroupBox()
        self.controlH.Size = Size(150, 60)
        self.controlH.Location = Point(2, 0)
        self.controlH.ForeColor = Color.FromArgb(231,231,231)
        self.controlH.Text = 'Spot'
        elements.append(self.controlH)
        
        #Home
        self.home = RadioButton()
        self.home.Text = 'Home'
        self.home.Checked = eval(self.var['home'])
        self.home.Location = Point(10, 15)
        self.home.BackColor = Color.FromArgb(25,25,25)
        self.home.ForeColor = Color.FromArgb(231,231,231)
        self.home.Size = Size(60, 30)
        self.home.CheckedChanged += self.checkHome
        self.controlH.Controls.Add(self.home)
        
        #Innkeeper
        self.inn = RadioButton()
        self.inn.Text = 'Innkeeper'
        self.inn.Checked = eval(self.var['innkeeper'])
        self.inn.Location = Point(71, 15)
        self.inn.BackColor = Color.FromArgb(25,25,25)
        self.inn.ForeColor = Color.FromArgb(231,231,231)
        self.inn.Size = Size(75, 30)
        self.inn.CheckedChanged += self.checkHome
        self.controlH.Controls.Add(self.inn)
        
        #Skill
        self.skillH = GroupBox()
        self.skillH.Size = Size(150, 60)
        self.skillH.Location = Point(151, 0)
        self.skillH.ForeColor = Color.FromArgb(231,231,231)
        self.skillH.Text = 'Skill'
        elements.append(self.skillH)
        
        #Magery
        self.magery = RadioButton()
        self.magery.Text = 'Magery'
        self.magery.Checked = eval(self.var['magery'])
        self.magery.Location = Point(10, 15)
        self.magery.BackColor = Color.FromArgb(25,25,25)
        self.magery.ForeColor = Color.FromArgb(231,231,231)
        self.magery.Size = Size(60, 30)
        self.skillH.Controls.Add(self.magery)
        
        #Chivalry
        self.chivalry = RadioButton()
        self.chivalry.Text = 'Chivalry'
        self.chivalry.Checked = eval(self.var['chivalry'])
        self.chivalry.Location = Point(71, 15)
        self.chivalry.BackColor = Color.FromArgb(25,25,25)
        self.chivalry.ForeColor = Color.FromArgb(231,231,231)
        self.chivalry.Size = Size(75, 30)
        self.skillH.Controls.Add(self.chivalry)

        #PositionX
        self.positionX = Label()
        self.positionX.Size = Size(100,15)
        self.positionX.Location = Point(80,75)
        self.positionX.Text = "X position home: "
        elements.append(self.positionX)
        
        #PositionXV
        self.positionXV = TextBox()
        self.positionXV.Size = Size(30,15)
        self.positionXV.Location = Point(181,74)
        self.positionXV.Text = "{0}".format(self.var['posX'])
        elements.append(self.positionXV)
        
        #PositionY
        self.positionY = Label()
        self.positionY.Size = Size(100,15)
        self.positionY.Location = Point(80,100)
        self.positionY.Text = "Y position home: "
        elements.append(self.positionY)
        
        #PositionYV
        self.positionYV = TextBox()
        self.positionYV.Size = Size(30,15)
        self.positionYV.Location = Point(181,99)
        self.positionYV.Text = "{0}".format(self.var['posY'])
        elements.append(self.positionYV)
     
        #CloseButton
        self.btnCloseH = Button()
        self.btnCloseH.Text = 'Close'
        self.btnCloseH.BackColor = Color.FromArgb(50,50,50)
        self.btnCloseH.Size = Size(50, 30)
        self.btnCloseH.Location = Point(120, 130)
        self.btnCloseH.FlatStyle = FlatStyle.Flat
        self.btnCloseH.FlatAppearance.BorderSize = 1
        self.btnCloseH.Click += self.btnClosePressedH
        elements.append(self.btnCloseH)
          
        self.checkHome(send,args)
        
        for elem in elements:
            self.h.Controls.Add(elem)
                
        self.h.ShowDialog() 
     
    def checkHome(self, send, args):   
        if self.home.Checked:
            self.positionXV.ReadOnly = False
            self.positionXV.BorderStyle = BorderStyle.Fixed3D
            self.positionXV.ResetBackColor()
            self.positionXV.ResetForeColor()
            self.positionYV.ReadOnly = False
            self.positionYV.BorderStyle = BorderStyle.Fixed3D
            self.positionYV.ResetBackColor()
            self.positionYV.ResetForeColor()
        else:
            self.positionXV.ReadOnly = True
            self.positionXV.BorderStyle = BorderStyle.None
            self.positionXV.BackColor = Color.FromArgb(25,25,25)
            self.positionXV.ForeColor = Color.FromArgb(231,231,231)
            self.positionYV.ReadOnly = True
            self.positionYV.BorderStyle = BorderStyle.None
            self.positionYV.BackColor = Color.FromArgb(25,25,25)
            self.positionYV.ForeColor = Color.FromArgb(231,231,231)
    
    def btnClosePressedH(self,send,args):
        while len(self.h.Controls) > 0:
            for ctr in self.h.Controls:
                self.h.Controls.Remove(ctr)
                
        self.var['magery'] = str(self.magery.Checked)
        self.var['chivalry'] = str(self.chivalry.Checked)
        self.var['home'] = str(self.home.Checked)
        self.var['innkeeper'] = str(self.inn.Checked)
        self.var['posX'] = str(self.positionXV.Text)
        self.var['posY'] = int(self.positionYV.Text)
        self.Update()
        
        self.h.Close()    
        
            
    def btnPausePressed(self, send, args):
        self.Step.Text = "Paused."
        self.time.Enabled = False
        #self.time2.Enabled = False
        self.Controls.Remove(self.btnPause)
        self.Controls.Remove(self.btnStop)
        
        #ResumeButton
        self.btnResume = Button()
        self.btnResume.Text = 'Resume'
        self.btnResume.BackColor = Color.FromArgb(50,50,50)
        self.btnResume.Size = Size(70, 30)
        self.btnResume.Location = Point(120, 260)
        self.btnResume.FlatStyle = FlatStyle.Flat
        self.btnResume.FlatAppearance.BorderSize = 1
        self.btnResume.Click += self.btnResumePressed
        
        self.Controls.Add(self.btnResume)
        
    def btnResumePressed(self, send, args):
        self.Controls.Remove(self.btnResume)
        self.Controls.Add(self.btnPause)
        self.Controls.Add(self.btnStop)
        self.time.Enabled = True
        #self.time2.Enabled = False
        
    def btnStopPressed(self, send, args):
        self.Flags()
        self.Update()
        
        #self.time2.Enabled = False
        self.time.Enabled = False
        self.Update()
        self.Controls.Remove(self.btnStop)
        self.Controls.Remove(self.btnPause)
        
        
        if eval(self.var['home']):
            self.Step.Text = "Going Home."
        else:
            self.Step.Text = "Going Innkeeper."
            
        self.GoBack()
        playerx = Player.Position.X
        playery = Player.Position.Y    
        while Player.Position.X == playerx and Player.Position.Y == playery:
            Items.UseItem(int(self.var['runebook'],16))
            Gumps.WaitForGump(1593994358, 10000)
            if eval(self.var['magery']):
                Gumps.SendAction(1593994358, 17)
            else:
                Gumps.SendAction(1593994358, 19)
            Misc.Pause(300)    
        if eval(self.var['home']):
            while Player.Position.X != int(self.var['posX']) or Player.Position.Y != int(self.var['posY']):
                Player.PathFindTo(int(self.var['posX']),int(self.var['posY']),Player.Position.Z)
                Misc.Pause(50)
            
            
    def btnResetPressed(self, send, args):
        self.var["completedQuest"] = 0
        Misc.SendMessage(self.var["completedQuest"])
        self.var["actualTime"] = "0001-01-01 00:00:00"
        self.var["oldTime"] = "0001-01-01 00:00:00"
        self.var["kitHwFound"] = 0
        self.var["kitYewFound"] = 0
        self.Update()
    
    def setBeetle(self, send, args):
        self.var["beetleSerial"] = hex(Target.PromptTarget())
        self.Update()
        self.Pet.Text = "Beetle serial: {0}".format(self.var['beetleSerial'])
      
    def setContainerBackpack(self, send, args):
        self.var['containerBackpack'] = hex(Target.PromptTarget())
        self.Update()
        self.ContainerB.Text = "Container backpack serial: {0}".format(self.var['containerBackpack'])
    
    def setContainerBankT(self, send, args):
        self.var["containerBank"] = hex(Target.PromptTarget())
        self.Update()
        self.ContainerBank.Text = "Container inside bank serial: {0}".format(self.var['containerBank'])
        
    def setRunebook(self, send, args):
        self.var["runebook"] = hex(Target.PromptTarget())
        self.Update()
        self.Runebook.Text = "Runebook serial: {0}".format(self.var['runebook'])
    
    def setNormalBonus(self, send, args):
        self.var['minBonus'] = int(self.BonusNB.Text)
        self.Update()
        self.BonusNB.Text = "{0}".format(self.var['minBonus'])
        self.BonusNB.ReadOnly = True
        self.BonusNB.BorderStyle = BorderStyle.None
        self.BonusNB.BackColor = Color.FromArgb(25,25,25)
        self.BonusNB.ForeColor = Color.FromArgb(231,231,231)
    
    def setExecBonus(self, send, args):
        self.var['exBonus'] = int(self.BonusEB.Text)
        self.Update()
        self.BonusEB.Text = "{0}".format(self.var['exBonus'])
        self.BonusEB.ReadOnly = True
        self.BonusEB.BorderStyle = BorderStyle.None
        self.BonusEB.BackColor = Color.FromArgb(25,25,25)
        self.BonusEB.ForeColor = Color.FromArgb(231,231,231)
    
    def setMoveAmount(self, send, args):
        self.var['moveAmount'] = int(self.MoveAmountT.Text)
        self.Update()
        self.MoveAmountT.Text = "{0} ".format(self.var['moveAmount'])
        self.MoveAmountT.ReadOnly = True
        self.MoveAmountT.BorderStyle = BorderStyle.None
        self.MoveAmountT.BackColor = Color.FromArgb(25,25,25)
        self.MoveAmountT.ForeColor = Color.FromArgb(231,231,231)
    
    def jewelPressed(self, send, args):
        elements = []
        
        self.jf = Form()
        self.jf.BackColor = Color.FromArgb(25,25,25)
        self.jf.ForeColor = Color.FromArgb(231,231,231)
        self.jf.Size = Size(270, 370)
        self.jf.Text = '{0}'.format(self.ScriptName)
        self.jf.TopMost = True
        
        #InfoLabel
        self.Info = Label()
        self.Info.Size = Size(170,15)
        self.Info.Location = Point(0,0)
        self.Info.Text = "Jewel Settings.         Take jewels "
        elements.append(self.Info)
        
        #CheckBox
        self.check = CheckBox()
        self.check.Width = 90
        self.check.Location = Point(171,-5)
        self.check.Checked = eval(self.var['checked'])
        self.check.CheckedChanged += self.checkedBox
        elements.append(self.check)
        
        #DamageIncrease
        self.damageIncrease = Label()
        self.damageIncrease.Size = Size(140,15)
        self.damageIncrease.Location = Point(0,20)
        self.damageIncrease.Text = "Damage Increase: "
        elements.append(self.damageIncrease)
        
        #DamageIncreaseV
        self.damageIncreaseV = TextBox()
        self.damageIncreaseV.Size = Size(30,15)
        self.damageIncreaseV.Location = Point(150,19)
        self.damageIncreaseV.Text = "{0}".format(self.props['Jdamageincrease'])
        self.damageIncreaseV.ReadOnly = True
        elements.append(self.damageIncreaseV)
        
        #DefenseChanceIncrease
        self.defenseChanceIncrease = Label()
        self.defenseChanceIncrease.Size = Size(140,15)
        self.defenseChanceIncrease.Location = Point(0,40)
        self.defenseChanceIncrease.Text = "Defense Chance Increase: "
        elements.append(self.defenseChanceIncrease)
        
        #DefenseChanceIncreaseV
        self.defenseChanceIncreaseV = TextBox()
        self.defenseChanceIncreaseV.Size = Size(30,15)
        self.defenseChanceIncreaseV.Location = Point(150,39)
        self.defenseChanceIncreaseV.Text = "{0}".format(self.props['Jdefensechanceincrease'])
        elements.append(self.defenseChanceIncreaseV)
        
        #DexterityBonus
        self.dexterityBonus = Label()
        self.dexterityBonus.Size = Size(140,15)
        self.dexterityBonus.Location = Point(0,60)
        self.dexterityBonus.Text = "Dexterity Bonus: "
        elements.append(self.dexterityBonus)
        
        #DexterityBonusV
        self.dexterityBonusV = TextBox()
        self.dexterityBonusV.Size = Size(30,15)
        self.dexterityBonusV.Location = Point(150,59)
        self.dexterityBonusV.Text = "{0}".format(self.props['Jdexteritybonus'])
        elements.append(self.dexterityBonusV)
        
        #EnhancePotions
        self.enhancePotions = Label()
        self.enhancePotions.Size = Size(140,15)
        self.enhancePotions.Location = Point(0,80)
        self.enhancePotions.Text = "Enhance Potions: "
        elements.append(self.enhancePotions)
        
        #EnhancePotionsV
        self.enhancePotionsV = TextBox()
        self.enhancePotionsV.Size = Size(30,15)
        self.enhancePotionsV.Location = Point(150,79)
        self.enhancePotionsV.Text = "{0}".format(self.props['Jenhancepotions'])
        elements.append(self.enhancePotionsV)
        
        #FasterCastRecovery
        self.fasterCastRecovery = Label()
        self.fasterCastRecovery.Size = Size(140,15)
        self.fasterCastRecovery.Location = Point(0,100)
        self.fasterCastRecovery.Text = "Faster Cast Recovery: "
        elements.append(self.fasterCastRecovery)
        
        #FasterCastRecoveryV
        self.fasterCastRecoveryV = TextBox()
        self.fasterCastRecoveryV.Size = Size(30,15)
        self.fasterCastRecoveryV.Location = Point(150,99)
        self.fasterCastRecoveryV.Text = "{0}".format(self.props['Jfastercastrecovery'])
        elements.append(self.fasterCastRecoveryV)
        
        #FasterCasting
        self.fasterCasting = Label()
        self.fasterCasting.Size = Size(140,15)
        self.fasterCasting.Location = Point(0,120)
        self.fasterCasting.Text = "Faster Casting: "
        elements.append(self.fasterCasting)
        
        #FasterCastingV
        self.fasterCastingV = TextBox()
        self.fasterCastingV.Size = Size(30,15)
        self.fasterCastingV.Location = Point(150,119)
        self.fasterCastingV.Text = "{0}".format(self.props['Jfastercasting'])
        elements.append(self.fasterCastingV)
        
        #HitChanceIncrease
        self.hitChanceIncrease = Label()
        self.hitChanceIncrease.Size = Size(140,15)
        self.hitChanceIncrease.Location = Point(0,140)
        self.hitChanceIncrease.Text = "Hit Chance Increase: "
        elements.append(self.hitChanceIncrease)
        
        #HitChanceIncreaseV
        self.hitChanceIncreaseV = TextBox()
        self.hitChanceIncreaseV.Size = Size(30,15)
        self.hitChanceIncreaseV.Location = Point(150,139)
        self.hitChanceIncreaseV.Text = "{0}".format(self.props['Jhitchanceincrease'])
        elements.append(self.hitChanceIncreaseV)
        
        #IntelligenceBonus
        self.intelligenceBonus = Label()
        self.intelligenceBonus.Size = Size(140,15)
        self.intelligenceBonus.Location = Point(0,160)
        self.intelligenceBonus.Text = "Intelligence Bonus: "
        elements.append(self.intelligenceBonus)
        
        #IntelligenceBonusV
        self.intelligenceBonusV = TextBox()
        self.intelligenceBonusV.Size = Size(30,15)
        self.intelligenceBonusV.Location = Point(150,159)
        self.intelligenceBonusV.Text = "{0}".format(self.props['Jintelligencebonus'])
        elements.append(self.intelligenceBonusV)
        
        #LowerManaCost
        self.lowerManaCost = Label()
        self.lowerManaCost.Size = Size(140,15)
        self.lowerManaCost.Location = Point(0,180)
        self.lowerManaCost.Text = "Lower Mana Cost: "
        elements.append(self.lowerManaCost)
        
        #LowerManaCostV
        self.lowerManaCostV = TextBox()
        self.lowerManaCostV.Size = Size(30,15)
        self.lowerManaCostV.Location = Point(150,179)
        self.lowerManaCostV.Text = "{0}".format(self.props['Jlowermanacost'])
        elements.append(self.lowerManaCostV)
        
        #LowerReagentCost
        self.lowerReagentCost = Label()
        self.lowerReagentCost.Size = Size(140,15)
        self.lowerReagentCost.Location = Point(0,200)
        self.lowerReagentCost.Text = "Lower Reagent Cost: "
        elements.append(self.lowerReagentCost)
        
        #LowerReagentCostV
        self.lowerReagentCostV = TextBox()
        self.lowerReagentCostV.Size = Size(30,15)
        self.lowerReagentCostV.Location = Point(150,199)
        self.lowerReagentCostV.Text = "{0}".format(self.props['Jlowerreagentcost'])
        elements.append(self.lowerReagentCostV)
        
        #Luck
        self.luck = Label()
        self.luck.Size = Size(140,15)
        self.luck.Location = Point(0,220)
        self.luck.Text = "Luck: "
        elements.append(self.luck)
        
        #LuckV
        self.luckV = TextBox()
        self.luckV.Size = Size(30,15)
        self.luckV.Location = Point(150,219)
        self.luckV.Text = "{0}".format(self.props['Jluck'])
        elements.append(self.luckV)
        
        #SpellDamageIncrease
        self.spellDamageIncrease = Label()
        self.spellDamageIncrease.Size = Size(140,15)
        self.spellDamageIncrease.Location = Point(0,240)
        self.spellDamageIncrease.Text = "Spell Damage Increase: "
        elements.append(self.spellDamageIncrease)
        
        #SpellDamageIncreaseV
        self.spellDamageIncreaseV = TextBox()
        self.spellDamageIncreaseV.Size = Size(30,15)
        self.spellDamageIncreaseV.Location = Point(150,239)
        self.spellDamageIncreaseV.Text = "{0}".format(self.props['Jspelldamageincrease'])
        elements.append(self.spellDamageIncreaseV)
        
        #StrengthBonus
        self.strengthBonus = Label()
        self.strengthBonus.Size = Size(140,15)
        self.strengthBonus.Location = Point(0,260)
        self.strengthBonus.Text = "Strength Bonus: "
        elements.append(self.strengthBonus)
        
        #StrengthBonusV
        self.strengthBonusV = TextBox()
        self.strengthBonusV.Size = Size(30,15)
        self.strengthBonusV.Location = Point(150,259)
        self.strengthBonusV.Text = "{0}".format(self.props['Jstrengthbonus'])
        elements.append(self.strengthBonusV)
        
        #Number
        self.number = Label()
        self.number.Size = Size(140,15)
        self.number.Location = Point(0,280)
        self.number.Text = "How much of them at least: "
        elements.append(self.number)
        
        #NumberV
        self.numberV = TextBox()
        self.numberV.Size = Size(30,15)
        self.numberV.Location = Point(150,279)
        self.numberV.Text = "{0}".format(self.var['number'])
        elements.append(self.numberV)
        
        #CloseButton
        self.btnClose = Button()
        self.btnClose.Text = 'Close'
        self.btnClose.BackColor = Color.FromArgb(50,50,50)
        self.btnClose.Size = Size(50, 30)
        self.btnClose.Location = Point(80, 300)
        self.btnClose.FlatStyle = FlatStyle.Flat
        self.btnClose.FlatAppearance.BorderSize = 1
        self.btnClose.Click += self.btnClosePressed
        elements.append(self.btnClose)
        
        for elem in elements:
            self.jf.Controls.Add(elem)
        
        self.checkedBox(send,args)
        
        self.jf.ShowDialog() 
   
    def btnClosePressed(self,send,args):
        while len(self.jf.Controls) > 0:
            for ctr in self.jf.Controls:
                self.jf.Controls.Remove(ctr)
        self.var['number'] = int(self.numberV.Text)
        self.var['checked'] = str(self.check.Checked)
        self.props['Jdamageincrease'] = int(self.damageIncreaseV.Text)
        self.props['Jdefensechanceincrease'] = int(self.defenseChanceIncreaseV.Text)
        self.props['Jenhancepotions'] = int(self.enhancePotionsV.Text)
        self.props['Jfastercastrecovery'] = int(self.fasterCastRecoveryV.Text)
        self.props['Jfastercasting'] = int(self.fasterCastingV.Text)
        self.props['Jhitchanceincrease'] = int(self.hitChanceIncreaseV.Text)
        self.props['Jintelligencebonus'] = int(self.intelligenceBonusV.Text)
        self.props['Jlowermanacost'] = int(self.lowerManaCostV.Text)
        self.props['Jlowerreagentcost'] = int(self.lowerReagentCostV.Text)
        self.props['Jluck'] = int(self.luckV.Text)
        self.props['Jspelldamageincrease'] = int(self.spellDamageIncreaseV.Text)
        self.props['Jstrengthbonus'] = int(self.strengthBonusV.Text)
        self.props['Jdexteritybonus'] = int(self.dexterityBonusV.Text)
        self.Update()
        
        self.jf.Close()
        
    def checkedBox(self,send,args):
        if self.check.Checked:
            for ctl in self.jf.Controls:
                if ctl.GetType() == TextBox:
                    ctl.ReadOnly = False
                    ctl.BorderStyle = BorderStyle.Fixed3D
                    ctl.ResetBackColor()
                    ctl.ResetForeColor()
                    
        else:
            for ctl in self.jf.Controls:
                if ctl.GetType() == TextBox:
                    ctl.ReadOnly = True
                    ctl.BorderStyle = BorderStyle.None
                    ctl.BackColor = Color.FromArgb(25,25,25)
                    ctl.ForeColor = Color.FromArgb(231,231,231) 
        
    def OnTick2(self, send, args):
        self.var["actualTime"] = datetime.now() - self.var["start"]
        self.TimePassed.Text = "Time " + str((self.var["actualTime"] + self.var["oldTime"]).time())
        
    def OnTick(self, send, args):
        self.CompletedQuests.Text = "Completed quests: {0}".format(str(self.var["completedQuest"]))
        self.KitYewFound.Text = "Kit yew found: {0}".format(str(self.var["kitYewFound"]))
        self.KitHwFound.Text = "Kit hw found: {0}".format(str(self.var["kitHwFound"]))
        if int(self.var["recallBank"]) == 0:
            if not "Checking" in self.Step.Text:
                self.Step.Text = "Checking if need to restock."
            self.Bank()
        elif int(self.var["restockBolt"]) == 0:
            if not "Restocking" in self.Step.Text:
                self.Step.Text = "Restocking bolt."
            self.RestockBolt()
        elif int(self.var["recallHW"]) == 0:
            if not "Going" in self.Step.Text:
                self.Step.Text = "Going back HW."
            self.RecallHW()
        elif int(self.var["enterHW"]) == 0:
            if not "Entering" in self.Step.Text:
                self.Step.Text = "Entering HW."
            self.EnterHW()
        elif int(self.var["goingToNPC"]) == 0:
            if not "Finding" in self.Step.Text:
                self.Step.Text = "Finding NPC."
            self.GoNPC()
        elif int(self.var["deliver"]) == 0:
            if not "Delivering" in self.Step.Text:
                self.Step.Text = "Delivering."
            self.Deliver()
        elif int(self.var["reloadBeetle"]) == 0:
            if not "Realoading" in self.Step.Text:
                self.Step.Text = "Reloading from beetle."
            self.ReloadBeetle()
        elif int(self.var["goBack"]) == 0:
            if not "Going" in self.Step.Text:
                self.Step.Text = "Going back."
            self.GoBack()
        elif int(self.var["checkReward"]) == 0:
            self.CheckReward()
        else:
            Misc.NoOperation()

    def RecallBank(self):
        Items.UseItem(int(self.var['runebook'],16))   
        Gumps.WaitForGump(1593994358, 10000)
        if eval(self.var['magery']):
            Gumps.SendAction(1593994358, 5)
        else:
            Gumps.SendAction(1593994358, 7)
        Misc.Pause(500)
        
    def Bank(self):
        self.var["reloadBeetle"] = 1
        self.var["goBack"] = 1
        if Items.ContainerCount(Player.Backpack, BoltID, 0) > 9:
            self.var["recallBank"] = 1
            self.var["restockBolt"] = 1
        else:
            fil = Mobiles.Filter()
            fil.Enabled = True
            fil.RangeMax = 12
            found = 0
            vendors = Mobiles.ApplyFilter(fil)
            if len(vendors) > 0:
                for vendor in vendors:
                    if "banker" in vendor.Name:
                        found = found +1
                if found == 0:
                    self.RecallBank()
                else:
                    self.var["recallBank"] = 1
                    self.var["restockBolt"] = 0
                    self.var["goBack"] = 1
            else:
                self.RecallBank()
        
    def RestockBolt(self):
        Misc.Pause(150)
        Player.ChatSay(52, "bank")
        while not Items.FindBySerial(int(self.var['containerBank'],16)):
            Misc.Pause(50)
        Items.UseItem(int(self.var['containerBank'],16))
        Misc.Pause(150)
        Mobiles.UseMobile(Player.Serial)
        while Player.Mount:
            Misc.Pause(100)
        beetle = Mobiles.FindBySerial(int(self.var['beetleSerial'],16))
        Items.WaitForContents(beetle.Backpack, TimeoutOnWaitAction)
        if Items.ContainerCount(beetle.Backpack, BoltID, 0) < 10:
            if Items.ContainerCount(Items.FindBySerial(int(self.var['containerBank'],16)), BoltID, 0) > 0:
                for numbolt in Items.FindBySerial(int(self.var['containerBank'],16)).Contains:
                    if numbolt.ItemID == BoltID:
                        Items.Move(numbolt, beetle.Backpack, 16000)
                        break
                Misc.Pause(DragDelay)
                for numbolt in Items.FindBySerial(int(self.var['containerBank'],16)).Contains:
                    if numbolt.ItemID == BoltID:       
                        Items.Move(numbolt, Player.Backpack, int(self.var['moveAmount']))
                        break
                Misc.Pause(DragDelay)
            else:
                self.Step.Text = "No more bolts."
                self.Step.Font = Font("Arial", 10, FontStyle.Bold);
                self.time.Enabled = False
                self.Controls.Remove(self.btnStop)
                self.Controls.Remove(self.btnPause)
        Mobiles.UseMobile(beetle)
        for items in Items.FindBySerial(int(self.var['containerBackpack'],16)).Contains:
            if items.ItemID == 0x1022 and (items.Hue == 0x04A9 or items.Hue == 0x04A8) :
                Items.Move(items, Items.FindBySerial(int(self.var['containerBank'],16)), 0)
                Misc.Pause(DragDelay)
        self.var["restockBolt"] = 1
        self.var["recallHW"] = 0
        
    def RecallHW(self):
        if not Items.FindBySerial(0x403203A5):
            Items.UseItem(int(self.var['runebook'],16))
            Gumps.WaitForGump(1593994358, 10000)
            if eval(self.var['magery']):
                Gumps.SendAction(1593994358, 11)
            else:
                Gumps.SendAction(1593994358, 13)
            
            Misc.Pause(500)
        else:
            self.var["recallHW"] = 1
            self.var["enterHW"] = 0
    
    def EnterHW(self):
        if not Items.FindBySerial(0x403240AC):
            Gate = Items.FindBySerial(0x403203A5)
            Player.PathFindTo(Gate.Position.X,Gate.Position.Y,Gate.Position.Z)
        else:
            self.var["enterHW"] = 1
            self.var["goingToNPC"] = 0
    
    def GoNPC(self):
        if not Mobiles.FindBySerial(QuestGiverSerial):
            while Player.Position.X != 6986 or Player.Position.Y != 339:
                Player.PathFindTo(535,992,0)
                Misc.Pause(200)
            while Player.Position.X != 6994 or Player.Position.Y != 349:
                Player.PathFindTo(6994,349,0)
                Misc.Pause(50)
            while Player.Position.X != 7005 or Player.Position.Y != 361:
                Player.PathFindTo(7005,361,0)
                Misc.Pause(50)
            while Player.Position.X != 7015 or Player.Position.Y != 370:    
                Player.PathFindTo(7015,370,0)
                Misc.Pause(50)
            while Player.Position.X != 7024 or Player.Position.Y != 378:    
                Player.PathFindTo(7024,378,0)
                Misc.Pause(50)
            while Player.Position.X != 7037 or Player.Position.Y != 378:        
                Player.PathFindTo(7037,378,0)
                Misc.Pause(50)
            Misc.Pause(50)
            Items.UseItem(int(self.var['containerBackpack'],16))
            Misc.Pause(50)
        else:
            self.var["goingToNPC"] = 1
            self.var["deliver"] = 0
   
    def Deliver(self):
        if Items.BackpackCount(BoltID, 0) < 10:      
            self.var["deliver"] = 1
            self.var["reloadBeetle"] = 0
        else:
            Gumps.ResetGump()
            Mobiles.UseMobile(QuestGiverSerial)
            Gumps.WaitForGump(107079709, TimeoutOnWaitAction)
            if Gumps.LastGumpTextExist("Lethal Darts"):
                quests = int(self.var["completedQuest"]) +1
                self.var["completedQuest"] = quests
                Gumps.WaitForGump(107079709, TimeoutOnWaitAction)
                Gumps.SendAction(107079709, 1)  
                Misc.WaitForContext(Player.Serial, TimeoutOnWaitAction)
                Misc.ContextReply(Player.Serial, ContextQuestToggleID)
                Target.WaitForTarget(TimeoutOnWaitAction)
                for itemcontenuti in Player.Backpack.Contains:
                    if itemcontenuti.ItemID == BoltID:
                        bolt = itemcontenuti.Serial
                Target.TargetExecute(bolt)  
                Target.WaitForTarget(TimeoutOnWaitAction)
                Target.Cancel()
                Mobiles.UseMobile(QuestGiverSerial)
                Gumps.WaitForGump(3072716675, TimeoutOnWaitAction)
                Gumps.SendAction(3072716675, 1)
                self.var["deliver"] = 1
                self.var["checkReward"] = 0
                
    def CheckReward(self):
        self.var["checkReward"] = 1
        for backpackItems in Player.Backpack.Contains:
            if backpackItems.ItemID == 0x0E75:
                Items.WaitForContents(backpackItems, TimeoutOnWaitAction)
                for rewcontain in backpackItems.Contains:
                    if rewcontain.ItemID == 0x1022 and (rewcontain.Hue == 0x04A9 or rewcontain.Hue == 0x04A8) :
                        Items.Move(rewcontain, Items.FindBySerial(int(self.var["containerBackpack"],16)), 0)
                        if rewcontain.Hue == 0x4A8:
                            self.var["kitYewFound"] = int(self.var["kitYewFound"]) +1
                        else:
                            self.var["kitHwFound"] = int(self.var["kitHwFound"]) +1
                        Misc.Pause(DragDelay)
                    elif rewcontain.ItemID == 0x108A or rewcontain.ItemID == 0x1F09 or rewcontain.ItemID == 0x1F06 or rewcontain.ItemID == 0x1086:
                        if eval(self.var['checked']):
                            self.CheckJewels(rewcontain)  
                    elif "Talisman" in rewcontain.Name:
                        self.CheckTalisman(rewcontain)
                Items.Move(backpackItems, Items.FindBySerial(TrashCan), 0) 
                Misc.Pause(TrashDelay)
        self.var["deliver"] = 0
         
    def CheckJewels(self,jewel):
        ContainerBackpack = int(self.var['containerBackpack'],16)
        Items.WaitForProps(jewel, TimeoutOnWaitAction)
        if len(Items.GetPropStringList(jewel)) >= (int(self.var['number'])+2):
            found = 0
            for jewelProp in Items.GetPropStringList(jewel):
                for prop in self.props:
                    if (prop.replace("J","").lower() in jewelProp.replace(" ","").lower()) and int(self.props[prop]) > 0:
                        if Items.GetPropValue(jewel,jewelProp) >= int(self.props[prop]):
                            found = found+1
                if found >= int(self.var['number']):
                    break
            if found >= int(self.var['number']):
                Items.Move(jewel, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)      
        
    def CheckTalisman(self, tal):
        ContainerBackpack = int(self.var['containerBackpack'],16)
        Items.WaitForProps(tal, TimeoutOnWaitAction)
        MinNormalBonus = int(self.var['minBonus'])
        MinExBonus = int(self.var['exBonus'])
        if Items.GetPropValue(tal.Serial," Exceptional") > MinExBonus:
            if Items.GetPropValue(tal.Serial, "Tinkering Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)   
            elif Items.GetPropValue(tal.Serial, "Fletching Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)           
            elif Items.GetPropValue(tal.Serial, "Tailoring Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)       
            elif Items.GetPropValue(tal.Serial, "Blacksmithing Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)           
            elif Items.GetPropValue(tal.Serial, "Inscription Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)      
            elif Items.GetPropValue(tal.Serial, "Cooking Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)         
            elif Items.GetPropValue(tal.Serial, "Alchemy Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)       
            elif Items.GetPropValue(tal.Serial, "Carpentry Bonus") >= MinNormalBonus:
                Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)                  
        
    def ReloadBeetle(self):
        Mobiles.UseMobile(Player.Serial)
        while Player.Mount:
            Misc.Pause(100)
        beetle = Mobiles.FindBySerial(int(self.var['beetleSerial'],16))
        Items.WaitForContents(beetle.Backpack, TimeoutOnWaitAction)
        if Items.ContainerCount(beetle.Backpack, BoltID, 0) > 10:
            if Items.ContainerCount(Player.Backpack, BoltID, 0) < 10:
                for itemcontenuti in beetle.Backpack.Contains:
                    found = 0
                    if itemcontenuti.ItemID == BoltID and found == 0:       
                        Items.Move(itemcontenuti, Player.Backpack, int(self.var['moveAmount'])) 
                        Misc.Pause(DragDelay)
                        found = 1
            else:
                Mobiles.UseMobile(beetle)
                while not Player.Mount:
                    Misc.Pause(100)
                self.var["reloadBeetle"] = 1
                self.var["deliver"] = 0
        else:
            Mobiles.UseMobile(beetle)
            while not Player.Mount:
                Misc.Pause(100)
            self.var["reloadBeetle"] = 1
            if Items.ContainerCount(Player.Backpack, BoltID, 0) < 10:
                self.var["goBack"] = 0
            else:
                self.var["deliver"] = 0
            
    def GoBack(self):
        if not Items.FindBySerial(0x403203A5):
            while Player.Position.X != 7021 and Player.Position.Y != 372:
                Player.PathFindTo(7021,372,0)
                Misc.Pause(50)
            while Player.Position.X != 7005 and Player.Position.Y != 361:    
                Player.PathFindTo(7005,361,0)
                Misc.Pause(50)
            while Player.Position.X != 6994 and Player.Position.Y != 349:      
                Player.PathFindTo(6994,349,0)
                Misc.Pause(50)
            while Player.Position.X != 538 and Player.Position.Y != 992:   
                Player.PathFindTo(6984,338,0)
                Misc.Pause(200)    
        else:
            self.var["goBack"] = 1
            self.var["recallBank"] = 0
           
    def LoadFile(self):
        f = ""
        if not File.Exists("HW.txt"):
            f = open("HW.txt","w+")
            for item in self.var:
                f.write(item + "=" + str(self.var.get(item))+"\n")
            for item in self.props:
                f.write(item + "=" + str(self.props.get(item))+"\n")    
            f.close()
        with open("HW.txt") as myfile:
            for line in myfile:
                name,value = line.partition("=")[::2]
                if name.startswith("J"):
                    self.props[name.strip()] = value.rstrip()
                else:
                    if not "start" in name.strip():
                        self.var[name.strip()] = value.rstrip()
     
    def Update(self):
        file = open("HW.txt","w")
        file.seek(0,0)
        for item in self.var:
            file.write(item + "=" + str(self.var.get(item))+"\n")
        for item in self.props:
            file.write(item + "=" + str(self.props.get(item))+"\n")
        file.close()
            
    def Flags(self):
        self.var["recallBank"] = self.var["restockBolt"] = self.var["recallHW"] = 0
        self.var["enterHW"] = self.var["deliver"] = self.var["reloadBeetle"] = 0
        self.var["goingToNPC"] = self.var["goBack"] = self.var["checkReward"] = 0
              
form = KeepForm()
Application.Run(form)        